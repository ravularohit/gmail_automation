# Gmail Email Processor
 
This project is a standalone Python script that integrates with the Gmail API to fetch emails and apply rule-based processing. The rules are defined in a JSON file and actions like marking emails as read/unread or moving them to a specific folder are supported.
 
## Features
 
- Fetch emails from Gmail using the Gmail API.
- Store email data in an SQLite database.
- Apply custom rule-based actions based on JSON rules.
- Mark emails as read/unread.
- Move emails to a specific Gmail label.
 
## Requirements
 
- Python 3.7+
- Gmail API enabled and credentials file (`credentials.json`).
 
## Installation
 
1. **Enable Gmail API:**
   - Follow Google's [Gmail API Quickstart Guide](https://developers.google.com/gmail/api/quickstart/python) to enable the API.
   - Download your `credentials.json` file.
 
2. **Install Dependencies:**
   - Install the necessary Python packages using pip:
     ```bash
     pip install -r requirements.txt
     ```
     
 
3. **Configure Database:**
   - The email data will be stored in an SQLite database file (`emails.db`).
 
4. **Create Rules File:**
   - Define the email rules in a JSON file (`rules.json`).
 
### Example Rules File (`rules.json`)
 
Here's an example `rules.json` file:
 
```json
{
  "rules": [
    {
      "conditions": [
        {
          "field": "from",
          "predicate": "contains",
          "value": "[email address removed]"
        },
        {
          "field": "subject",
          "predicate": "notcontains",
          "value": "marketing"
        }
      ],
      "predicate": "any",
      "actions": [
        {
          "type": "mark as read"
        },
        {
          "type": "move message",
          "value": "spam"
        }
      ]
    }
    
  ]
}
```

5. **Run src.main as module**
   ```bash
     python -m src.main
     ```