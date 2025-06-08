
from datetime import datetime
from .storage import EmailStorage
from .email_classifier import EmailClassifier

class JobTracker:
    def __init__(self, storage=None, classifier=None):
        self.storage = storage or EmailStorage()
        self.classifier = classifier or EmailClassifier()

    def update_job_tracker(self):
        try:
            job_emails = self.storage.get_recent_job_related_emails()
            updates = []
            
            for email_id, subject, sender, classification, content in job_emails:
                company = self.classifier.extract_company_name(sender, subject, content)
                position = self.classifier.extract_position(subject, content)
                
                if company and position:
                    status = self.classifier.map_classification_to_status(classification)
                    self.storage.save_job_application(company, position, status, email_id)
                    updates.append(f"{company} - {position}: {status}")
            
            return {
                "updates_count": len(updates),
                "updates": updates[:10]
            }
            
        except Exception as e:
            return {"error": f"Job tracker update failed: {str(e)}"}

    def generate_weekly_report(self):
        try:
            classifications = self.storage.get_emails_by_classification(days=7)
            job_stats = self.storage.get_job_applications_stats(days=7)
            
            total_emails = sum(classifications.values())
            positive_rate = (classifications.get('Positive', 0) / total_emails * 100) if total_emails > 0 else 0
            
            report = {
                "week_summary": {
                    "total_emails_processed": total_emails,
                    "positive_responses": classifications.get('Positive', 0),
                    "rejections": classifications.get('Rejection', 0),
                    "applications_confirmed": classifications.get('Applied-Confirmation', 0),
                    "positive_response_rate": round(positive_rate, 1)
                },
                "job_applications": job_stats,
                "recommendations": self.generate_recommendations(classifications, job_stats)
            }
            
            return report
            
        except Exception as e:
            return {"error": f"Report generation failed: {str(e)}"}

    def generate_recommendations(self, classifications, job_stats):
        recommendations = []
        
        positive_count = classifications.get('Positive', 0)
        rejection_count = classifications.get('Rejection', 0)
        
        if positive_count == 0 and rejection_count > 5:
            recommendations.append("Consider revising your resume or application strategy")
        
        if positive_count > 2:
            recommendations.append("Great job! You're getting positive responses")
        
        if classifications.get('Applied-Confirmation', 0) > 10:
            recommendations.append("You're applying frequently - focus on quality applications")
        
        return recommendations
