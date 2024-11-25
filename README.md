MailToCalendar is a smart tool that schedules meeting reminders by extracting crucial details such as location, time, date, and purpose directly from email content. This project leverages machine learning and modern APIs to automate the process of scheduling meetings in Google Calendar.

Fetches emails using the Gmail API. Focuses on the latest email exchange between specified sender and receiver email IDs.
Utilizes deepset/roberta-base-squad2 to identify the reason or description for the meeting.
Utilizes en_core_web_sm (spaCy) to extract the date, location, and time of the meeting.
Passes all extracted details (sender and receiver email IDs, date, time, location, and description) to the Google Calendar API.
Schedules the meeting with a reminder on the specified date and time in the calendar.

Technology Stack:
  Machine Learning Models:
    deepset/roberta-base-squad2 for extracting meeting purposes.
    spaCy's en_core_web_sm for date, location, and time extraction.
  APIs:
    Gmail API: For reading and parsing emails.
    Google Calendar API: For scheduling and managing meeting events.
  Programming Language: Python
  Libraries: spaCy, Hugging Face Transformers, Google API Client Libraries

How It Works:
  Fetches the latest email from the specified sender and receiver.
  Runs the email text through machine learning models to extract meeting details.
  Sends the extracted information to the Google Calendar API to schedule a reminder.
