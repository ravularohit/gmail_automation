
import os
from src.database import  fetch_and_store_emails, setup_database
from src.gmail_api import get_gmail_service
from src.process_mails import process_emails



if __name__=='__main__':
    DB_FILE=os.getenv("DB_FILE")
    service=get_gmail_service() #intitate service
    setup_database(DB_FILE=DB_FILE) #create DB
    fetch_and_store_emails(service,DB_FILE=DB_FILE) #fetch and store emails
    process_emails(service)    #process the emails
    
    
    