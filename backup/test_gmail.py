from gmail_api import GmailAPI
import json

def test_gmail_connection():
    print("Testing Gmail API connection...")
    
    try:
        gmail = GmailAPI()
        print("✅ Gmail API authentication successful!")
        
        print("\nFetching recent emails...")
        recent_emails = gmail.get_recent_emails(days=3, max_results=5)
        
        print(f"✅ Found {len(recent_emails)} recent emails")
        
        for i, email in enumerate(recent_emails[:3], 1):
            print(f"\n--- Email {i} ---")
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")
            print(f"Snippet: {email['snippet'][:100]}...")
        
        print("\nTesting job-related email search...")
        job_emails = gmail.get_job_related_emails(days=7, max_results=5)
        print(f"✅ Found {len(job_emails)} job-related emails")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gmail_connection()
