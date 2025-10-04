import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st
from config import EMAIL_CONFIG

class EmailNotifier:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.email = EMAIL_CONFIG['email']
        self.password = EMAIL_CONFIG['password']
        
    def send_alert(self, to_email, student_name, risk_level, risk_factors):
        """Send email alert to counselors/parents"""
        try:
            # Create message
            subject = f"🚨 EduGuard Alert: {student_name} - {risk_level}"
            
            # HTML email content
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: {'#ff6b6b' if 'HIGH' in risk_level else '#ffd93d' if 'MEDIUM' in risk_level else '#6bcf7f'};">
                    EduGuard Student Alert
                </h2>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                    <h3>Student: {student_name}</h3>
                    <p><strong>Risk Level:</strong> {risk_level}</p>
                    <p><strong>Alert Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    
                    <h4>Risk Factors:</h4>
                    <ul>
            """
            
            for factor in risk_factors:
                body += f"<li>⚠️ {factor}</li>"
            
            body += f"""
                    </ul>
                    
                    <h4>Recommended Actions:</h4>
                    <ul>
                        <li>📞 Contact student immediately</li>
                        <li>👥 Schedule counseling session</li>
                        <li>📊 Monitor progress closely</li>
                        <li>💬 Coordinate with parents</li>
                    </ul>
                    
                    <p style="margin-top: 20px; color: #666;">
                        This is an automated alert from EduGuard System.
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            st.error(f"📧 Email failed: {str(e)}")
            st.info("💡 Tip: Use Gmail App Password instead of regular password")
            return False
    
    def send_weekly_report(self, to_email, report_data):
        """Send weekly summary report"""
        try:
            subject = "📊 EduGuard Weekly Report"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>EduGuard Weekly Summary Report</h2>
                <p><strong>Report Period:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h3>📈 Institutional Overview</h3>
                    <ul>
                        <li>Total Students: {report_data['total_students']}</li>
                        <li>High Risk: {report_data['high_risk']}</li>
                        <li>Medium Risk: {report_data['medium_risk']}</li>
                        <li>Low Risk: {report_data['low_risk']}</li>
                    </ul>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h3>🎯 Critical Students Needing Attention</h3>
            """
            
            for student in report_data['critical_students']:
                body += f"<p>• <strong>{student['name']}</strong> - {', '.join(student['risk_factors'])}</p>"
            
            body += """
                </div>
                
                <p style="margin-top: 20px; color: #666;">
                    Best regards,<br>EduGuard System
                </p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            st.error(f"📧 Weekly report failed: {str(e)}")
            return False