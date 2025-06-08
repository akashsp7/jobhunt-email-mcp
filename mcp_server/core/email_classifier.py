
class EmailClassifier:
    def __init__(self):
        self.positive_keywords = [
            "interview", "congratulations", "move forward", "next step",
            "offer", "pleased to inform", "selected", "invitation"
        ]
        
        self.rejection_keywords = [
            "unfortunately", "not selected", "declined", "regret",
            "not moving forward", "other candidates", "rejected"
        ]
        
        self.confirmation_keywords = [
            "application received", "thank you for applying",
            "submitted successfully", "confirmation"
        ]

    def classify_single_email(self, email, tags=None):
        if tags is None:
            tags = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
        
        subject = email.get("subject", "").lower()
        content = email.get("body", "").lower()
        sender = email.get("from", "").lower()
        text = f"{subject} {content} {sender}"
        
        # Check if email is job-related at all
        job_related_keywords = [
            "job", "position", "career", "hiring", "recruitment", "recruiter", 
            "application", "resume", "cv", "interview", "opportunity", "role",
            "employment", "work", "company", "team", "candidate"
        ]
        
        is_job_related = any(keyword in text for keyword in job_related_keywords)
        
        # Only classify as job categories if it's actually job-related
        if is_job_related:
            if "Positive" in tags and any(keyword in text for keyword in self.positive_keywords):
                return "Positive"
            elif "Rejection" in tags and any(keyword in text for keyword in self.rejection_keywords):
                return "Rejection"
            elif "Applied-Confirmation" in tags and any(keyword in text for keyword in self.confirmation_keywords):
                return "Applied-Confirmation"
            elif "Spam" in tags:
                return "Spam"
            else:
                # Job-related but no specific classification - default to least specific job category
                if "Applied-Confirmation" in tags:
                    return "Applied-Confirmation"
                elif "Spam" in tags:
                    return "Spam"
                else:
                    return tags[0] if tags else "Unknown"
        else:
            # Not job-related at all
            if "Spam" in tags:
                return "Spam"
            else:
                # If user only wants job categories but email isn't job-related, 
                # put in the least specific available category
                if "Applied-Confirmation" in tags:
                    return "Applied-Confirmation"  # Most neutral job category
                else:
                    return tags[-1] if tags else "Unknown"  # Use last tag as fallback

    def calculate_importance(self, email):
        subject = email.get("subject", "").lower()
        content = email.get("body", "").lower()
        sender = email.get("from", "").lower()
        
        score = 0
        
        high_priority_keywords = [
            "urgent", "asap", "immediate", "interview", "offer",
            "deadline", "expires", "final", "last chance"
        ]
        
        medium_priority_keywords = [
            "application", "position", "opportunity", "recruiter"
        ]
        
        for keyword in high_priority_keywords:
            if keyword in subject:
                score += 3
            if keyword in content:
                score += 2
        
        for keyword in medium_priority_keywords:
            if keyword in subject:
                score += 2
            if keyword in content:
                score += 1
        
        if "noreply" in sender or "donotreply" in sender:
            score -= 2
        
        return score

    def extract_company_name(self, sender, subject, content):
        common_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
        
        if "@" in sender:
            domain = sender.split("@")[-1].replace(">", "")
            if not any(common in domain for common in common_domains):
                return domain.split(".")[0].title()
        
        return "Unknown Company"

    def extract_position(self, subject, content):
        position_keywords = ["engineer", "developer", "manager", "analyst", "intern"]
        
        for keyword in position_keywords:
            if keyword in subject.lower():
                return keyword.title()
        
        return "Unknown Position"

    def map_classification_to_status(self, classification):
        mapping = {
            "Applied-Confirmation": "Applied",
            "Positive": "Interview Scheduled",
            "Rejection": "Rejected"
        }
        return mapping.get(classification, "Unknown")

    def classify_emails_batch(self, emails, tags=None):
        if tags is None:
            tags = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
        
        classified = {tag: [] for tag in tags}
        
        for email in emails:
            classification = self.classify_single_email(email, tags)
            classified[classification].append({
                "id": email["id"],
                "subject": email["subject"],
                "from": email["from"],
                "date": email["date"],
                "snippet": email["snippet"]
            })
        
        return classified
