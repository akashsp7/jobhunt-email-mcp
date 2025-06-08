#!/usr/bin/env python3
"""
Gradio Web Interface for JobHunt Email Intelligence
Backup testing interface for the MCP server tools
"""

import gradio as gr
import json
from mcp_server.tools import EmailTools

def create_gradio_interface():
    """Create Gradio interface for testing MCP tools"""
    email_tools = EmailTools()
    
    def handle_classify_emails(count, tags_str):
        tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else None
        result = email_tools.classify_emails(int(count), tags)
        return json.dumps(result, indent=2)
    
    def handle_important_emails(days):
        result = email_tools.get_important_emails(int(days))
        return json.dumps(result, indent=2)
    
    def handle_job_tracker():
        result = email_tools.update_job_tracker()
        return json.dumps(result, indent=2)
    
    def handle_weekly_report():
        result = email_tools.generate_weekly_report()
        return json.dumps(result, indent=2)
    
    def handle_extract_info(email_id):
        result = email_tools.extract_email_info(email_id)
        return json.dumps(result, indent=2)
    
    with gr.Blocks(title="JobHunt Email Intelligence - Web Interface") as interface:
        gr.Markdown("# 🎯 JobHunt Email Intelligence")
        gr.Markdown("Web testing interface for MCP server tools")
        
        with gr.Tab("Classify Emails"):
            with gr.Row():
                count_input = gr.Number(value=50, label="Email Count")
                tags_input = gr.Textbox(
                    value="Positive,Rejection,Applied-Confirmation,Spam", 
                    label="Tags (comma-separated)"
                )
            classify_btn = gr.Button("Classify Emails")
            classify_output = gr.Textbox(label="Classification Results", lines=20)
            classify_btn.click(
                handle_classify_emails, 
                inputs=[count_input, tags_input], 
                outputs=classify_output
            )
        
        with gr.Tab("Important Emails"):
            days_input = gr.Number(value=3, label="Days to Check")
            important_btn = gr.Button("Get Important Emails")
            important_output = gr.Textbox(label="Important Emails", lines=20)
            important_btn.click(
                handle_important_emails, 
                inputs=[days_input], 
                outputs=important_output
            )
        
        with gr.Tab("Job Tracker"):
            tracker_btn = gr.Button("Update Job Tracker")
            tracker_output = gr.Textbox(label="Job Tracker Updates", lines=20)
            tracker_btn.click(handle_job_tracker, outputs=tracker_output)
        
        with gr.Tab("Weekly Report"):
            report_btn = gr.Button("Generate Weekly Report")
            report_output = gr.Textbox(label="Weekly Report", lines=20)
            report_btn.click(handle_weekly_report, outputs=report_output)
        
        with gr.Tab("Extract Email Info"):
            email_id_input = gr.Textbox(label="Gmail Message ID")
            extract_btn = gr.Button("Extract Info")
            extract_output = gr.Textbox(label="Extracted Information", lines=15)
            extract_btn.click(
                handle_extract_info, 
                inputs=[email_id_input], 
                outputs=extract_output
            )
    
    return interface

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860)
