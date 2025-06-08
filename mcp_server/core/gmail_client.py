import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:
    def __init__(self, credentials_file='client_secret_530571396736-jh5id4kn03ej7s1m5krca8di91m0iua4.apps.googleusercontent.com.json'):
        self.credentials_file = credentials_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    os.remove('token.pickle')
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(
                    port=8080, prompt='select_account', access_type='offline'
                )
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)

    def get_messages(self, query='', max_results=100):
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []

    def get_message_detail(self, message_id):
        try:
            message = self.service.users().messages().get(
                userId='me', id=message_id, format='full').execute()
            return self.parse_message(message)
        except Exception as e:
            print(f"Error fetching message detail: {e}")
            return None

    def parse_message(self, message):
        payload = message['payload']
        headers = payload.get('headers', [])
        
        result = {
            'id': message['id'],
            'thread_id': message['threadId'],
            'date': None,
            'subject': '',
            'from': '',
            'to': '',
            'body': '',
            'snippet': message.get('snippet', '')
        }
        
        for header in headers:
            name = header['name'].lower()
            if name == 'date':
                result['date'] = header['value']
            elif name == 'subject':
                result['subject'] = header['value']
            elif name == 'from':
                result['from'] = header['value']
            elif name == 'to':
                result['to'] = header['value']
        
        result['body'] = self.extract_body(payload)
        return result

    def extract_body(self, payload):
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                elif 'parts' in part:
                    body = self.extract_body(part)
                    if body:
                        break
        else:
            if payload['mimeType'] == 'text/plain':
                if 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(
                        payload['body']['data']).decode('utf-8')
        return body

    def get_recent_emails(self, days=7, max_results=50):
        date_filter = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query = f'after:{date_filter}'
        
        messages = self.get_messages(query=query, max_results=max_results)
        detailed_messages = []
        
        for msg in messages:
            detail = self.get_message_detail(msg['id'])
            if detail:
                detailed_messages.append(detail)
        
        return detailed_messages
