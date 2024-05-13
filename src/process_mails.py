from datetime import datetime, timezone
import json
from src.logger_util import logging
from datetime import timedelta
from src.database import get_emails
from src.models import Email

RULES_FILE='./src/rules.json'

def apply_rule(rule, email:Email):
    try:
        field_name = rule['field']
        predicate = rule['predicate']
        value = rule['value']
        email_value = None
    
        if field_name == 'from':
            email_value = email.sender
        elif field_name == 'subject':
            email_value = email.subject
        elif field_name == 'labels':
            email_value = email.labels
        elif field_name == 'date_received':
            email_value = email.date_received
            try:
                email_value = datetime.strptime(email_value, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                email_value = datetime.strptime(email_value, '%a, %d %b %Y %H:%M:%S')
        if field_name == 'date_received':
            if predicate == 'lt':
                return email_value < datetime.now(timezone.utc) - timedelta(days=int(value))
            elif predicate == 'gt':
                return email_value > datetime.now(timezone.utc) - timedelta(days=int(value))
        if predicate == 'contains':
            return value in email_value
        elif predicate == 'notcontains':
            return value not in email_value
        elif predicate == 'eq':
            return value == email_value
        elif predicate == 'neq':
            return value != email_value
    except Exception:
        logging.exception("exception occured",exc_info=True)
    return False

def load_rules():
    with open(RULES_FILE, 'r') as file:
        return json.load(file)
def process_emails(service):
    try:
        rules = load_rules()
        emails = get_emails('emails.db')
        for email in emails:
            for rule in rules['rules']:
                predicate = rule['predicate']
    
                rule_matches = [apply_rule(cond, email) for cond in rule['conditions']]
                matched = all(rule_matches) if predicate == 'all' else any(rule_matches)
    
                if matched:
                    for action in rule['actions']:
                        perform_action(action, email, service)
    except Exception:
        logging.exception("exception occured",exc_info=True)
 
def perform_action(action, email:Email, service):
    try:
        message_id = email.id
        action_type=action.get("type")
        if action_type == 'Mark as read'.lower():
            service.users().messages().modify(userId='me', id=message_id,
                                            body={'removeLabelIds': ['UNREAD']}).execute()
            logging.info(f"Message {message_id} marked as read.")
        elif action_type == 'Mark as unread'.lower():
            service.users().messages().modify(userId='me', id=message_id,
                                            body={'addLabelIds': ['UNREAD']}).execute()
            logging.info(f"Message {message_id} marked as unread.")
        elif action_type == 'Move Message'.lower():
            label_name = action.get('value')
            labels = service.users().labels().list(userId='me').execute()
            label_id = [label['name']  for label in labels['labels'] if label['name'].lower() == label_name ] 
            if label_id:
                service.users().messages().modify(userId='me', id=message_id,
                                                body={'addLabelIds': [label_id[0]]}).execute()
                logging.info(f"Message {message_id} moved to {label_name}.")
            else:
                logging.info(f"Label '{label_name}' not found.")
    except Exception:
        logging.exception("exception occured",exc_info=True)


