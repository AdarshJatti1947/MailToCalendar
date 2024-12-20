# -*- coding: utf-8 -*-
"""MailToCalendar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Doot7KuOokFYxrFS_oD-uArqKdVa1JpA
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

# Define the scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate and initialize the Gmail API
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    # Initialize the flow using client_secrets.json
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

    # Set redirect URI for out-of-band (OOB) flow
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    # Generates an authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')

    # Show the authorization URL and ask the user to paste the code
    print("Please go to this URL and authorize the application:", auth_url)
    code = input("Paste the authorization code here: ")

    # Exchange code for credentials
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Save the credentials for future use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Connect to the Gmail API
try:
    service = build('gmail', 'v1', credentials=creds)
    print("Successfully connected to Gmail API.")
except Exception as e:
    print(f"An error occurred: {e}")

from googleapiclient.discovery import build
import pickle
import os

# Load credentials from the token.pickle file
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# Connect to the Gmail API
service = build('gmail', 'v1', credentials=creds)

# Function to read emails from a specific sender and to a specific receiver
def read_emails_from_sender_to_receiver(sender_email, receiver_email):
    email_snippets = []  # Initialize an empty list to store snippets
    try:
        # Create a query to filter by both sender and receiver email
        query = f"from:{sender_email} to:{receiver_email}"
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f"No messages found from {sender_email} to {receiver_email}.")
            return email_snippets

        # Iterate over messages and add each snippet to the list
        for msg in messages:
            msg_id = msg['id']
            msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
            email_snippets.append(msg_data['snippet'])  # Add each snippet to the list

        return email_snippets  # Return the list of email snippets

    except Exception as e:
        print(f"An error occurred: {e}")
        return email_snippets

# Call the function with the sender and receiver's email IDs
sender_email="sender@gmail.com" # sender email address
receiver_email="receiver@gmail.com" # receiver email address
email_list = read_emails_from_sender_to_receiver(sender_email, receiver_email)
#print(email_list[0])

from transformers import pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
import spacy
import pickle
import random
nlp = spacy.load('en_core_web_sm')

def answer_question_description(context, question):
    # Get the answer
    result = qa_pipeline({
        'question': question,
        'context': context
    })



    return result['answer']

def extract_details(sentence):
    doc = nlp(sentence)

    # Initialize placeholders for details
    details = {"date": "No date mentioned", "time": "No time mentioned", "location": "No location mentioned"}

    # Iterate through detected entities
    for ent in doc.ents:
        if ent.label_ == "DATE":
            details["date"] = ent.text
        elif ent.label_ == "TIME":
            details["time"] = ent.text
        elif ent.label_ == "GPE" or ent.label_ == "LOC":  # Geopolitical entity or location
            details["location"] = ent.text

    return details

!pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate and initialize the Google Calendar API
creds = None
if os.path.exists('token_calendar.pickle'):
    with open('token_calendar.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    # Get the authorization URL and show it
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("Please go to this URL and authorize the application:", auth_url)

    # Get the authorization code from the user
    code = input("Paste the authorization code here: ")
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Save the credentials for future use
    with open('token_calendar.pickle', 'wb') as token:
        pickle.dump(creds, token)

def connect_google_API(location, description, sender_email,receiver_email,startdateTime,enddateTime):
  # Connect to the Google Calendar API
  try:
    service = build('calendar', 'v3', credentials=creds)
    # Define event details
    event = {
        'summary': 'Meeting',
        'location': location,
        'description': description,
        'start':
         {
             'dateTime': startdateTime,
             'timeZone': 'Asia/Kolkata',
        },
        'end':
         {
             'dateTime': enddateTime,
             'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': sender_email},
            {'email': receiver_email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 10},       # 10 minutes before
            ],
        },
    }

    # Insert the event into the calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created:', event.get('htmlLink'))

  except HttpError as error:
    print(f"An error occurred: {error}")

from datetime import datetime

def parse_date(date_str):
    current_year = datetime.now().year

    try:
        date_obj = datetime.strptime(date_str, "%d %B")
        date_obj = date_obj.replace(year=current_year)
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            return "Invalid date format"

    return date_obj.strftime("%Y-%m-%d")



def convert_to_24_hour_format(time_str):
    try:
        # Try parsing as 12-hour format with AM/PM
        time_obj = datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        try:
            # If it fails, try parsing as 24-hour format
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
        except ValueError:
            return "Invalid time format"  # Handle invalid inputs

    return time_obj.strftime("%H:%M:%S")


def add_one_hour(time_str):
  str1=convert_to_24_hour_format(time_str)[0:2]
  val=int(str1)+1
  new_text = str1.replace(str1[0:2], str(val))+convert_to_24_hour_format(time_str)[2:len(convert_to_24_hour_format("9:00 AM"))]
  return new_text

for email in email_list:
  context=email
  print(context)
  description=answer_question_description(context,"what is the main reason for the meeting in the text, I just need the reason for the meeting")



  result = extract_details(context)

  extracted_values = []

  for value in result.values():
    extracted_values.append(value)
  extracted_values.append(description)

  break # break statement ends the loop and adds the last email detais to the calendar only

date=extracted_values[0]
time=extracted_values[1]
location=extracted_values[2]
description=extracted_values[3]
startdateTime=parse_date(date)+"T"+convert_to_24_hour_format(time)+"+05:30"
enddateTime=parse_date(date)+"T"+add_one_hour(time)+"+05:30"

sender_email="sender@gmail.com" # sender email address
receiver_email="receiver@gmail.com" # receiver email address

connect_google_API(location, description, sender_email,receiver_email,startdateTime,enddateTime)
  # Connect to the Google Calendar API