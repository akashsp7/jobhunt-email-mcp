import gradio as gr
import json
from gmail_api import GmailAPI
from datetime import datetime
import sqlite3
import os

class JobHuntMCPServer:
    def __init__(self):
        self.gmail = None
        self.db_path = "jobhunt.db"
        self.init_database()
        
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                subject TEXT,
                sender TEXT,
                date TEXT,
                classification TEXT,
                importance INTEGER,
                content TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                position TEXT,
                status TEXT,
                applied_date TEXT,
                last_update TEXT,
                email_id TEXT,
                FOREIGN KEY (email_id) REFERENCES emails (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def authenticate_gmail(self):
        try:
            self.gmail = GmailAPI()
            return "✅ Gmail authentication successful!"
        except Exception as e:
            return f"❌ Authentication failed: {str(e)}"

    def classify_emails(self, count=50, tags=None):
        if not self.gmail:
            auth_result = self.authenticate_gmail()
            if "failed" in auth_result:
                return {"error": auth_result}
        
        if tags is None:
            tags = ["Positive", "Rejection", "Applied-Confirmation", "Spam"]
        
        try:
            emails = self.gmail.get_recent_emails(days=7, max_results=count)
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
            
            self.save_classified_emails(emails, classified)
            
            return {
                "total_processed": len(emails),
                "classifications": {tag: len(emails) for tag, emails in classified.items()},
                "emails": classified
            }
            
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}

    def classify_single_email(self, email, tags):
        subject = email.get("subject", "").lower()
        content = email.get("body", "").lower()
        sender = email.get("from", "").lower()
        text = f"{subject} {content} {sender}"
        
        positive_keywords = [
            "interview", "congratulations", "move forward", "next step",
            "offer", "pleased to inform", "selected", "invitation"
        ]
        
        rejection_keywords = [
            "unfortunately", "not selected", "declined", "regret",
            "not moving forward", "other candidates", "rejected"
        ]
        
        confirmation_keywords = [
            "application received", "thank you for applying",
            "submitted successfully", "confirmation"
        ]
        
        if any(keyword in text for keyword in positive_keywords):
            return "Positive"
        elif any(keyword in text for keyword in rejection_keywords):
            return "Rejection"
        elif any(keyword in text for keyword in confirmation_keywords):
            return "Applied-Confirmation"
        else:
            return "Spam"

    def get_important_emails(self, days=3):
        if not self.gmail:
            auth_result = self.authenticate_gmail()
            if "failed" in auth_result:
                return {"error": auth_result}
        
        try:
            emails = self.gmail.get_recent_emails(days=days, max_results=50)
            important_emails = []
            
            for email in emails:
                importance_score = self.calculate_importance(email)
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

    def save_classified_emails(self, emails, classified):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for email in emails:
            classification = "Unknown"
            for tag, tag_emails in classified.items():
                if any(e["id"] == email["id"] for e in tag_emails):
                    classification = tag
                    break
            
            cursor.execute('''
                INSERT OR REPLACE INTO emails 
                (id, subject, sender, date, classification, content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                email["id"], email["subject"], email["from"],
                email["date"], classification, email["body"]
            ))
        
        conn.commit()
        conn.close()

    def update_job_tracker(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, subject, sender, classification, content 
                FROM emails 
                WHERE classification IN ('Positive', 'Rejection', 'Applied-Confirmation')
                ORDER BY processed_at DESC
            ''')
            
            emails = cursor.fetchall()
            updates = []
            
            for email_id, subject, sender, classification, content in emails:
                company = self.extract_company_name(sender, subject, content)
                position = self.extract_position(subject, content)
                
                if company and position:
                    status = self.map_classification_to_status(classification)
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO job_applications 
                        (company, position, status, last_update, email_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (company, position, status, datetime.now().isoformat(), email_id))
                    
                    updates.append(f"{company} - {position}: {status}")
            
            conn.commit()
            conn.close()
            
            return {
                "updates_count": len(updates),
                "updates": updates[:10]
            }
            
        except Exception as e:
            return {"error": f"Job tracker update failed: {str(e)}"}

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

    def generate_weekly_report(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT classification, COUNT(*) 
                FROM emails 
                WHERE date(processed_at) >= date('now', '-7 days')
                GROUP BY classification
            ''')
            
            classifications = dict(cursor.fetchall())
            
            cursor.execute('''
                SELECT status, COUNT(*) 
                FROM job_applications 
                WHERE date(last_update) >= date('now', '-7 days')
                GROUP BY status
            ''')
            
            job_stats = dict(cursor.fetchall())
            
            total_emails = sum(classifications.values())
            positive_rate = (classifications.get('Positive', 0) / total_emails * 100) if total_emails > 0 else 0
            
            conn.close()
            
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

def create_mcp_interface():
    server = JobHuntMCPServer()
    
    def handle_classify_emails(count, tags_str):
        tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else None
        result = server.classify_emails(int(count), tags)
        return json.dumps(result, indent=2)
    
    def handle_important_emails(days):
        result = server.get_important_emails(int(days))
        return json.dumps(result, indent=2)
    
    def handle_job_tracker():
        result = server.update_job_tracker()
        return json.dumps(result, indent=2)
    
    def handle_weekly_report():
        result = server.generate_weekly_report()
        return json.dumps(result, indent=2)
    
    with gr.Blocks(title="JobHunt Email Intelligence MCP Server") as interface:
        gr.Markdown("# 🎯 JobHunt Email Intelligence MCP Server")
        gr.Markdown("MCP Server for intelligent job hunting email management")
        
        with gr.Tab("Classify Emails"):
            with gr.Row():
                count_input = gr.Number(value=50, label="Email Count")
                tags_input = gr.Textbox(value="Positive,Rejection,Applied-Confirmation,Spam", label="Tags (comma-separated)")
            classify_btn = gr.Button("Classify Emails")
            classify_output = gr.Textbox(label="Classification Results", lines=20)
            classify_btn.click(handle_classify_emails, inputs=[count_input, tags_input], outputs=classify_output)
        
        with gr.Tab("Important Emails"):
            days_input = gr.Number(value=3, label="Days to Check")
            important_btn = gr.Button("Get Important Emails")
            important_output = gr.Textbox(label="Important Emails", lines=20)
            important_btn.click(handle_important_emails, inputs=[days_input], outputs=important_output)
        
        with gr.Tab("Job Tracker"):
            tracker_btn = gr.Button("Update Job Tracker")
            tracker_output = gr.Textbox(label="Job Tracker Updates", lines=20)
            tracker_btn.click(handle_job_tracker, outputs=tracker_output)
        
        with gr.Tab("Weekly Report"):
            report_btn = gr.Button("Generate Weekly Report")
            report_output = gr.Textbox(label="Weekly Report", lines=20)
            report_btn.click(handle_weekly_report, outputs=report_output)
    
    return interface

if __name__ == "__main__":
    interface = create_mcp_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860)
