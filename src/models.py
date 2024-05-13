

from datetime import datetime
from pydantic import BaseModel, field_validator

from typing import Union

class Email(BaseModel):
    id: str
    sender: str
    subject: str
    labels: str
    date_received: str