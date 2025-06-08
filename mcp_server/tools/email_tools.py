
import json
from ..core import GmailClient, EmailClassifier, EmailStorage, JobTracker

class EmailTools:
    def __init__(self):
        self.gmail_client = None
        self.classifier = EmailClassifier()
        self.storage = EmailStorage()
        self.job_tracker = JobTracker(self.storage, self.classifier)
        
    def _ensure_gmail_auth(self):
        if not self.gmail_client:
            try:
                self.gmail_client = GmailClient()
                return True
            except Exception as e:
                return f"Gmail authentication failed: {str(e)}"
        return True

    def classify_emails(self, count=50, tags=None):
        auth_result = self._ensure_gmail_auth()
        if auth_result != True:
            return {"error": auth_result}
        
        if tags is None:
            tags = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
        
        try:
            emails = self.gmail_client.get_recent_emails(days=7, max_results=count)
            classified = self.classifier.classify_emails_batch(emails, tags)
            
            self.storage.save_classified_emails(emails, classified)
            
            return {
                "total_processed": len(emails),
                "classifications": {tag: len(emails) for tag, emails in classified.items()},
                "emails": classified
            }
            
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}

    def get_important_emails(self, days=3):
        auth_result = self._ensure_gmail_auth()
        if auth_result != True:
            return {"error": auth_result}
        
        try:
            emails = self.gmail_client.get_recent_emails(days=days, max_results=50)
            important_emails = []
            
            for email in emails:
                importance_score = self.classifier.calculate_importance(email)
                if importance_score > 7:
                    email["importance_score"] = importance_score
                    important_emails.append(email)
            
            important_emails.sort(key=lambda x: x["importance_score"], reverse=True)
            
            return {
                "count": len(important_emails),
                "emails": important_emails[:10]
            }
            
        except Exception as e:
            return {"error": f"Failed to get important emails: {str(e)}"}

    def update_job_tracker(self):
        return self.job_tracker.update_job_tracker()

    def generate_weekly_report(self):
        return self.job_tracker.generate_weekly_report()

    def extract_email_info(self, email_id):
        auth_result = self._ensure_gmail_auth()
        if auth_result != True:
            return {"error": auth_result}
        
        try:
            email_detail = self.gmail_client.get_message_detail(email_id)
            if not email_detail:
                return {"error": "Email not found"}
            
            classification = self.classifier.classify_single_email(email_detail)
            importance = self.classifier.calculate_importance(email_detail)
            company = self.classifier.extract_company_name(
                email_detail["from"], email_detail["subject"], email_detail["body"]
            )
            position = self.classifier.extract_position(
                email_detail["subject"], email_detail["body"]
            )
            
            return {
                "email_id": email_id,
                "subject": email_detail["subject"],
                "from": email_detail["from"],
                "date": email_detail["date"],
                "classification": classification,
                "importance_score": importance,
                "extracted_company": company,
                "extracted_position": position,
                "snippet": email_detail["snippet"]
            }
            
        except Exception as e:
            return {"error": f"Email info extraction failed: {str(e)}"}
