import sqlite3
from datetime import datetime

class EmailStorage:
    def __init__(self, db_path="jobhunt.db"):
        self.db_path = db_path
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

    def get_emails_by_classification(self, days=7):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT classification, COUNT(*) 
            FROM emails 
            WHERE date(processed_at) >= date('now', '-? days')
            GROUP BY classification
        ''', (days,))
        
        result = dict(cursor.fetchall())
        conn.close()
        return result

    def save_job_application(self, company, position, status, email_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO job_applications 
            (company, position, status, last_update, email_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (company, position, status, datetime.now().isoformat(), email_id))
        
        conn.commit()
        conn.close()

    def get_job_applications_stats(self, days=7):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM job_applications 
            WHERE date(last_update) >= date('now', '-? days')
            GROUP BY status
        ''', (days,))
        
        result = dict(cursor.fetchall())
        conn.close()
        return result

    def get_recent_job_related_emails(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, subject, sender, classification, content 
            FROM emails 
            WHERE classification IN ('Positive', 'Rejection', 'Applied-Confirmation')
            ORDER BY processed_at DESC
        ''')
        
        result = cursor.fetchall()
        conn.close()
        return result
