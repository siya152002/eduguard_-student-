import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import json
import hashlib
import time

# Set page configuration first
st.set_page_config(
    page_title="EduTrack • Student Dropout Prevention system",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS for Beautiful UI
CUSTOM_CSS = """
<style>
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Custom Cards */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 6px solid #667eea;
        margin-bottom: 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .custom-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Risk Level Styles */
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(255,107,107,0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffd93d 0%, #ffbe0b 100%);
        color: black;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(255,217,61,0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #6bcf7f 0%, #4caf50 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(107,207,127,0.3);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-top: 6px solid;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    /* Notification Cards */
    .notification-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid #ffeaa7;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 5px 15px rgba(255,234,167,0.3);
    }
    
    /* Department Filter */
    .department-filter {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    
    /* Teacher Cards */
    .teacher-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
    }
    
    .teacher-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102,126,234,0.4);
    }
    
    /* Modern Login Container */
    .login-container {
        max-width: 450px;
        margin: 80px auto;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .login-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .login-header h3 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .login-header p {
        color: #666;
        font-size: 1rem;
    }
    
    /* Enhanced Input Fields */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.9);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        background: white;
    }
    
    /* Enhanced Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102,126,234,0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    /* Logout Button */
    .logout-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
        box-shadow: 0 8px 25px rgba(255,107,107,0.3) !important;
    }
    
    .logout-btn:hover {
        box-shadow: 0 12px 35px rgba(255,107,107,0.4) !important;
    }
    
    /* User Info Panel */
    .user-info-panel {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
        text-align: center;
    }
    
    /* Demo Credentials Styling */
    .demo-credentials {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 2px dashed #667eea;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .login-container {
            margin: 40px 20px;
            padding: 2rem;
        }
        
        .main-header {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .metric-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
</style>
"""

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Risk Thresholds
RISK_THRESHOLDS = {
    'attendance_red': 60,
    'attendance_yellow': 75,
    'marks_red': 40,
    'marks_yellow': 50,
    'fee_overdue_red': 30,
    'fee_overdue_yellow': 15
}

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': "smtp.gmail.com",
    'smtp_port': 587,
    'email': "sharmasiya5891@gmail.com",
    'password': "pswe bmim ptwy pakh"
}

# Teacher Information with Login Credentials
TEACHER_DATA = {
    "10A": {
        "name": "Dr. Priya Sharma",
        "email": "priya.sharma@school.edu",
        "subject": "Mathematics & Science",
        "phone": "+91-9876543210",
        "experience": "12 years",
        "students_count": 35,
        "username": "priya.sharma",
        "password": "teacher123"
    },
    "10B": {
        "name": "Mr. Rajesh Kumar",
        "email": "rajesh.kumar@school.edu",
        "subject": "Physics & Chemistry",
        "phone": "+91-9876543211",
        "experience": "8 years",
        "students_count": 32,
        "username": "rajesh.kumar",
        "password": "teacher123"
    },
    "11A": {
        "name": "Ms. Anjali Patel",
        "email": "anjali.patel@school.edu",
        "subject": "Biology & Computer Science",
        "phone": "+91-9876543212",
        "experience": "10 years",
        "students_count": 28,
        "username": "anjali.patel",
        "password": "teacher123"
    },
    "11B": {
        "name": "Mr. Vikram Singh",
        "email": "vikram.singh@school.edu",
        "subject": "Commerce & Economics",
        "phone": "+91-9876543213",
        "experience": "15 years",
        "students_count": 30,
        "username": "vikram.singh",
        "password": "teacher123"
    },
    "12A": {
        "name": "Dr. Meera Nair",
        "email": "meera.nair@school.edu",
        "subject": "Mathematics & Physics",
        "phone": "+91-9876543214",
        "experience": "18 years",
        "students_count": 25,
        "username": "meera.nair",
        "password": "teacher123"
    },
    "12B": {
        "name": "Mrs. Sunita Reddy",
        "email": "sunita.reddy@school.edu",
        "subject": "Arts & Humanities",
        "phone": "+91-9876543215",
        "experience": "9 years",
        "students_count": 22,
        "username": "sunita.reddy",
        "password": "teacher123"
    }
}

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def hash_password(password):
    """Simple password hashing function"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    """Verify teacher login credentials"""
    # Check admin first
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True, "admin", "Administrator"
    
    # Check teachers
    for class_name, teacher in TEACHER_DATA.items():
        if teacher['username'] == username and teacher['password'] == password:
            return True, "teacher", teacher['name']
    
    return False, None, None

def login_page():
    """Display modern login page"""
    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1 class="floating">🎓 EduTrack</h1>
                <h3>Welcome Back!</h3>
                <p>Sign in to access your educational dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            # Enhanced input fields with icons
            username = st.text_input(
                "👤 Username", 
                placeholder="Enter your username",
                key="username_input"
            )
            
            password = st.text_input(
                "🔒 Password", 
                type="password", 
                placeholder="Enter your password",
                key="password_input"
            )
            
            # Animated submit button
            submit = st.form_submit_button(
                "🚀 Sign In",
                use_container_width=True
            )
            
            if submit:
                if username and password:
                    success, role, user_name = verify_login(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user_name
                        st.session_state.user_role = role
                        st.success(f"✅ Welcome back, {user_name}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Enhanced demo credentials section
        with st.expander("🔐 Demo Credentials", expanded=False):
            st.markdown('<div class="demo-credentials">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👑 Admin Access**")
                st.code("Username: admin\nPassword: admin123")
                st.markdown("💡 *Full administrative access*")
            
            with col2:
                st.markdown("**👨‍🏫 Teacher Access**")
                st.code("Username: priya.sharma\nPassword: teacher123")
                st.markdown("📚 *All teachers use: teacher123*")
            
            st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logout user with smooth transition"""
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.user_role = None
    st.success("👋 Successfully logged out!")
    time.sleep(1)
    st.rerun()

def load_students_from_json():
    """Load students from JSON file with better error handling"""
    try:
        with open('students.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if 'students' in data and isinstance(data['students'], list):
            return data['students']
        else:
            st.error("❌ JSON file structure is incorrect. Expected {'students': []}")
            return []
            
    except FileNotFoundError:
        st.error("❌ students.json file not found. Please create the file in the same directory as main.py")
        return []
    except json.JSONDecodeError as e:
        st.error(f"❌ Error decoding JSON file: {str(e)}")
        st.info("💡 Please check that your students.json file contains valid JSON format")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected error loading students: {str(e)}")
        return []

# Email Alert System
class EmailAlertSystem:
    def __init__(self, email_config):
        self.smtp_server = email_config['smtp_server']
        self.smtp_port = email_config['smtp_port']
        self.email = email_config['email']
        self.password = email_config['password']
    
    def send_alert(self, to_email, student_name, risk_type, risk_details):
        """Send email alert to parents/students"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = f"🚨 EduTrack Alert: {student_name} - {risk_type}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; border-radius: 10px;">
                    <h2>🎓 EduTrack Student Alert</h2>
                </div>
                <div style="background: #f8f9fa; padding: 20px; margin-top: 10px; border-radius: 10px;">
                    <h3>Dear Parent/Guardian,</h3>
                    <p>We would like to inform you about your ward's <strong>{risk_type}</strong> status:</p>
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <h4>Student: {student_name}</h4>
                        <p><strong>Alert Type:</strong> {risk_type}</p>
                        <p><strong>Details:</strong> {risk_details}</p>
                        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                    <p>Please contact the school administration for further discussion and support.</p>
                    <p>Best regards,<br>EduTrack Team</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
            
            return True, "Email sent successfully!"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

def compute_risk_level(student):
    """Compute risk level based on student data"""
    risk_score = 0
    
    if student['attendance'] < RISK_THRESHOLDS['attendance_red']:
        risk_score += 3
    elif student['attendance'] < RISK_THRESHOLDS['attendance_yellow']:
        risk_score += 2
    
    if student['marks'] < RISK_THRESHOLDS['marks_red']:
        risk_score += 3
    elif student['marks'] < RISK_THRESHOLDS['marks_yellow']:
        risk_score += 2
    
    if student['fee_overdue_days'] > RISK_THRESHOLDS['fee_overdue_red']:
        risk_score += 3
    elif student['fee_overdue_days'] > RISK_THRESHOLDS['fee_overdue_yellow']:
        risk_score += 2
    
    if risk_score >= 6:
        return 'High'
    elif risk_score >= 3:
        return 'Medium'
    else:
        return 'Low'

def analyze_student_risk(student):
    """Analyze student risk factors"""
    risks = []
    
    if student['attendance'] < RISK_THRESHOLDS['attendance_red']:
        risks.append(f"Attendance critically low: {student['attendance']}%")
    elif student['attendance'] < RISK_THRESHOLDS['attendance_yellow']:
        risks.append(f"Attendance low: {student['attendance']}%")
    
    if student['marks'] < RISK_THRESHOLDS['marks_red']:
        risks.append(f"Marks critically low: {student['marks']}%")
    elif student['marks'] < RISK_THRESHOLDS['marks_yellow']:
        risks.append(f"Marks low: {student['marks']}%")
    
    if student['fee_overdue_days'] > RISK_THRESHOLDS['fee_overdue_red']:
        risks.append(f"Fee overdue: {student['fee_overdue_days']} days")
    elif student['fee_overdue_days'] > RISK_THRESHOLDS['fee_overdue_yellow']:
        risks.append(f"Fee overdue: {student['fee_overdue_days']} days")
    
    return risks

def create_risk_distribution_chart(students):
    """Create risk distribution pie chart"""
    risk_counts = {
        'High': len([s for s in students if s.get('risk_level') == 'High']),
        'Medium': len([s for s in students if s.get('risk_level') == 'Medium']),
        'Low': len([s for s in students if s.get('risk_level') == 'Low'])
    }
    
    colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
    
    fig = px.pie(
        values=list(risk_counts.values()),
        names=list(risk_counts.keys()),
        title='📊 Student Risk Distribution',
        color_discrete_sequence=colors
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_performance_scatter(students):
    """Create attendance vs marks scatter plot"""
    df = pd.DataFrame(students)
    
    fig = px.scatter(
        df, 
        x='attendance', 
        y='marks',
        color='risk_level',
        size='fee_overdue_days',
        hover_data=['name', 'class'],
        title='📈 Attendance vs Marks Analysis',
        color_discrete_map={
            'High': '#ff6b6b',
            'Medium': '#ffd93d', 
            'Low': '#6bcf7f'
        }
    )
    fig.update_layout(
        xaxis_title='Attendance (%)',
        yaxis_title='Marks (%)'
    )
    
    fig.add_hline(y=RISK_THRESHOLDS['marks_red'], line_dash="dash", line_color="red", annotation_text="Marks Risk Threshold")
    fig.add_vline(x=RISK_THRESHOLDS['attendance_red'], line_dash="dash", line_color="red", annotation_text="Attendance Risk Threshold")
    
    return fig

def create_department_analysis(students):
    """Create department-wise analysis"""
    df = pd.DataFrame(students)
    
    dept_stats = df.groupby('class').agg({
        'attendance': 'mean',
        'marks': 'mean',
        'fee_overdue_days': 'mean',
        'risk_level': lambda x: (x == 'High').sum()
    }).round(2)
    
    dept_stats = dept_stats.reset_index()
    dept_stats.columns = ['Class', 'Avg Attendance', 'Avg Marks', 'Avg Fee Overdue Days', 'High Risk Students']
    
    fig = px.bar(
        dept_stats,
        x='Class',
        y=['Avg Attendance', 'Avg Marks'],
        title='🏫 Department-wise Performance Comparison',
        barmode='group'
    )
    fig.update_layout(
        yaxis_title='Percentage (%)',
        xaxis_title='Department/Class'
    )
    return fig, dept_stats

def create_attendance_trend(students):
    """Create attendance distribution histogram"""
    df = pd.DataFrame(students)
    
    fig = px.histogram(
        df, 
        x='attendance',
        nbins=20,
        title='📊 Attendance Distribution',
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        xaxis_title='Attendance (%)',
        yaxis_title='Number of Students'
    )
    
    fig.add_vline(x=RISK_THRESHOLDS['attendance_red'], line_dash="dash", line_color="red", annotation_text="Risk Threshold")
    
    return fig

def create_risk_heatmap(students):
    """Create risk factor heatmap"""
    df = pd.DataFrame(students)
    
    def get_risk_category(student):
        categories = []
        if student['attendance'] < RISK_THRESHOLDS['attendance_red']:
            categories.append('Attendance')
        if student['marks'] < RISK_THRESHOLDS['marks_red']:
            categories.append('Marks')
        if student['fee_overdue_days'] > RISK_THRESHOLDS['fee_overdue_red']:
            categories.append('Fee')
        return ', '.join(categories) if categories else 'No Risk'
    
    df['Risk Factors'] = df.apply(get_risk_category, axis=1)
    risk_counts = df['Risk Factors'].value_counts()
    
    fig = px.bar(
        x=risk_counts.values,
        y=risk_counts.index,
        orientation='h',
        title='🔥 Risk Factors Distribution',
        color=risk_counts.values,
        color_continuous_scale='reds'
    )
    fig.update_layout(
        xaxis_title='Number of Students',
        yaxis_title='Risk Factors'
    )
    return fig

def create_teacher_performance_chart(students, teacher_data):
    """Create teacher performance overview chart"""
    teacher_stats = []
    
    for class_name, teacher_info in teacher_data.items():
        class_students = [s for s in students if s['class'] == class_name]
        if class_students:
            avg_attendance = np.mean([s['attendance'] for s in class_students])
            avg_marks = np.mean([s['marks'] for s in class_students])
            high_risk_count = len([s for s in class_students if s.get('risk_level') == 'High'])
            
            teacher_stats.append({
                'Teacher': teacher_info['name'],
                'Class': class_name,
                'Avg Attendance': avg_attendance,
                'Avg Marks': avg_marks,
                'High Risk Students': high_risk_count,
                'Total Students': len(class_students),
                'Subject': teacher_info['subject']
            })
    
    df = pd.DataFrame(teacher_stats)
    
    if not df.empty:
        fig = px.bar(
            df,
            x='Teacher',
            y=['Avg Attendance', 'Avg Marks'],
            title='👨‍🏫 Teacher Performance Overview',
            barmode='group',
            hover_data=['Class', 'Subject', 'High Risk Students']
        )
        fig.update_layout(
            yaxis_title='Percentage (%)',
            xaxis_title='Teachers'
        )
        return fig, df
    return None, pd.DataFrame()

def main_app():
    """Main application after login"""
    # Enhanced header with user info
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.markdown('<div class="main-header">🎓 EduTrack • Student Success Platform</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="user-info-panel">
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <div style="font-size: 1.5em;">👤</div>
                <div>
                    <div style="font-weight: 600; font-size: 1.1em;">{st.session_state.current_user}</div>
                    <div style="font-size: 0.9em; opacity: 0.9;">{st.session_state.user_role.title()}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", type="secondary", use_container_width=True, key="logout_btn"):
            logout()
    
    # Load students from JSON
    students = load_students_from_json()
    
    if not students:
        st.warning("No student data loaded. Using sample data for demonstration.")
        students = [
            {
                "id": 1,
                "name": "Sample Student",
                "email": "sample@example.com",
                "attendance": 75,
                "marks": 65,
                "fee_overdue_days": 10,
                "class": "10A",
                "parent_name": "Sample Parent",
                "phone": "+91-0000000000",
                "risk_level": "Medium"
            }
        ]
    else:
        for student in students:
            student['risk_level'] = compute_risk_level(student)
    
    # Initialize email system
    email_system = EmailAlertSystem(EMAIL_CONFIG)
    
    # Get unique departments/classes for filtering
    departments = sorted(list(set(student['class'] for student in students)))
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Student Alerts", "Send Alerts", "Analytics", "Student Data", "Teacher Info"])
    
    with tab1:
        # Dashboard metrics
        high_risk = len([s for s in students if s.get('risk_level') == 'High'])
        medium_risk = len([s for s in students if s.get('risk_level') == 'Medium'])
        low_risk = len([s for s in students if s.get('risk_level') == 'Low'])
        
        total_students = len(students)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card" style="border-top-color: #667eea;">📊 Total Students<br><h2>{total_students}</h2></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card" style="border-top-color: #6bcf7f;">✅ Low Risk<br><h2>{low_risk}</h2></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="metric-card" style="border-top-color: #ffd93d;">⚠️ Medium Risk<br><h2>{medium_risk}</h2></div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'<div class="metric-card" style="border-top-color: #ff6b6b;">🚨 High Risk<br><h2>{high_risk}</h2></div>', unsafe_allow_html=True)
        
        # Department Filter Section
        st.markdown('<div class="department-filter">🏫 Department Filter</div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("🔍 Search by student name")
        with col2:
            risk_filter = st.selectbox("Filter by risk level", ["All", "High", "Medium", "Low"])
        with col3:
            department_filter = st.multiselect("Filter by department", departments, default=departments)
        
        # Filter students
        filtered_students = students
        if search_name:
            filtered_students = [s for s in filtered_students if search_name.lower() in s['name'].lower()]
        if risk_filter != "All":
            filtered_students = [s for s in filtered_students if s.get('risk_level') == risk_filter]
        if department_filter:
            filtered_students = [s for s in filtered_students if s['class'] in department_filter]
        
        # Student list
        st.subheader(f"📋 Student Overview ({len(filtered_students)} students)")
        
        for student in filtered_students:
            risk_level = student.get('risk_level', 'Low')
            risk_class = f"risk-{risk_level.lower()}"
            teacher_info = TEACHER_DATA.get(student['class'], {})
            teacher_name = teacher_info.get('name', 'Not Assigned')
            
            st.markdown(f'''
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <h4>{student["name"]} - Class {student["class"]}</h4>
                        <p>📧 {student["email"]} | 📞 {student["phone"]}</p>
                        <p>Parent: {student["parent_name"]} | Teacher: {teacher_name}</p>
                        <p>📊 Attendance: {student["attendance"]}% | 📝 Marks: {student["marks"]}% | 💰 Fee Overdue: {student["fee_overdue_days"]} days</p>
                    </div>
                    <div class="{risk_class}" style="min-width: 100px; text-align: center;">
                        {risk_level} Risk
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🚨 Students Needing Attention")
        
        high_risk_students = [s for s in students if s.get('risk_level') == 'High']
        medium_risk_students = [s for s in students if s.get('risk_level') == 'Medium']
        
        if high_risk_students:
            st.subheader("🔴 High Risk Students")
            for student in high_risk_students:
                risks = analyze_student_risk(student)
                teacher_info = TEACHER_DATA.get(student['class'], {})
                
                with st.expander(f"🔴 {student['name']} (Class {student['class']}) - {len(risks)} risk factors"):
                    st.write("**Risk Factors:**")
                    for risk in risks:
                        st.write(f"• {risk}")
                    
                    st.write("**Contact Information:**")
                    st.write(f"• Parent: {student['parent_name']}")
                    st.write(f"• Phone: {student['phone']}")
                    st.write(f"• Email: {student['email']}")
                    st.write(f"• Class Teacher: {teacher_info.get('name', 'Not Assigned')}")
                    st.write(f"• Teacher Email: {teacher_info.get('email', 'N/A')}")
                    
                    st.write("**Recommended Actions:**")
                    if any("Attendance" in risk for risk in risks):
                        st.write("• Schedule immediate parent meeting")
                        st.write("• Implement daily attendance monitoring")
                    if any("Marks" in risk for risk in risks):
                        st.write("• Provide extra tutoring sessions")
                        st.write("• Conduct learning assessment")
                    if any("Fee" in risk for risk in risks):
                        st.write("• Contact accounts department urgently")
                        st.write("• Discuss payment plan options")
        
        if medium_risk_students:
            st.subheader("🟡 Medium Risk Students")
            for student in medium_risk_students:
                risks = analyze_student_risk(student)
                teacher_info = TEACHER_DATA.get(student['class'], {})
                
                with st.expander(f"🟡 {student['name']} (Class {student['class']}) - {len(risks)} risk factors"):
                    st.write("**Risk Factors:**")
                    for risk in risks:
                        st.write(f"• {risk}")
                    
                    st.write("**Contact Information:**")
                    st.write(f"• Class Teacher: {teacher_info.get('name', 'Not Assigned')}")
                    st.write(f"• Teacher Email: {teacher_info.get('email', 'N/A')}")
                    
                    st.write("**Recommended Actions:**")
                    st.write("• Monitor progress weekly")
                    st.write("• Send progress report to parents")
                    st.write("• Schedule counseling session")
        
        if not high_risk_students and not medium_risk_students:
            st.success("🎉 No students currently require immediate attention!")
    
    with tab3:
        st.subheader("✉️ Send Email Alerts")
        
        student_options = {f"{s['name']} (Class {s['class']}) - {s['email']}": s for s in students}
        
        if student_options:
            selected_student_key = st.selectbox("Select Student", list(student_options.keys()))
            selected_student = student_options[selected_student_key]
            
            teacher_info = TEACHER_DATA.get(selected_student['class'], {})
            st.info(f"**Selected Student:** {selected_student['name']} | **Class:** {selected_student['class']} | **Parent:** {selected_student['parent_name']} | **Teacher:** {teacher_info.get('name', 'Not Assigned')}")
            
            risk_factors = analyze_student_risk(selected_student)
            
            if risk_factors:
                st.warning(f"**Detected Risk Factors for {selected_student['name']}:**")
                for risk in risk_factors:
                    st.write(f"• {risk}")
                
                default_message = f"We have identified the following concerns regarding {selected_student['name']}'s academic performance:\n\n" + "\n".join(f"• {risk}" for risk in risk_factors)
                custom_message = st.text_area("Customize Alert Message", value=default_message, height=150)
                
                if st.button("🚨 Send Alert Email", type="primary"):
                    with st.spinner("Sending email..."):
                        success, message = email_system.send_alert(
                            selected_student['email'],
                            selected_student['name'],
                            "Academic Performance Alert",
                            custom_message
                        )
                        
                        if success:
                            st.success(f"✅ Alert sent successfully to {selected_student['email']}")
                            st.balloons()
                        else:
                            st.error(f"❌ {message}")
            else:
                st.success(f"✅ {selected_student['name']} has no critical risk factors")
                
                if st.button("📧 Send Positive Feedback"):
                    positive_message = f"We are pleased to inform you that {selected_student['name']} is performing well academically. Keep up the good work!"
                    success, message = email_system.send_alert(
                        selected_student['email'],
                        selected_student['name'],
                        "Positive Performance Update",
                        positive_message
                    )
                    if success:
                        st.success("✅ Positive feedback sent!")
        else:
            st.warning("No students available to send alerts.")
    
    with tab4:
        st.subheader("📊 Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_risk = create_risk_distribution_chart(students)
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            fig_scatter = create_performance_scatter(students)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_dept, dept_stats = create_department_analysis(students)
            st.plotly_chart(fig_dept, use_container_width=True)
            
            st.subheader("📋 Department Statistics")
            st.dataframe(dept_stats, use_container_width=True)
        
        with col2:
            fig_attendance = create_attendance_trend(students)
            st.plotly_chart(fig_attendance, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_teacher, teacher_stats = create_teacher_performance_chart(students, TEACHER_DATA)
            if fig_teacher is not None:
                st.plotly_chart(fig_teacher, use_container_width=True)
            else:
                st.info("No teacher performance data available")
        
        with col2:
            fig_heatmap = create_risk_heatmap(students)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.subheader("📈 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        avg_attendance = np.mean([s['attendance'] for s in students])
        avg_marks = np.mean([s['marks'] for s in students])
        fee_overdue_count = len([s for s in students if s['fee_overdue_days'] > 0])
        
        with col1:
            st.metric("Average Attendance", f"{avg_attendance:.1f}%")
        with col2:
            st.metric("Average Marks", f"{avg_marks:.1f}%")
        with col3:
            st.metric("Students with Fee Due", fee_overdue_count)
        with col4:
            st.metric("Total Departments", len(departments))
    
    with tab5:
        st.subheader("📊 Student Data Overview")
        
        df = pd.DataFrame(students)
        df['teacher'] = df['class'].map(lambda x: TEACHER_DATA.get(x, {}).get('name', 'Not Assigned'))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Attendance", f"{df['attendance'].mean():.1f}%")
        with col2:
            st.metric("Average Marks", f"{df['marks'].mean():.1f}%")
        with col3:
            st.metric("Students with Fee Due", f"{len(df[df['fee_overdue_days'] > 0])}")
        
        st.dataframe(df[['name', 'class', 'teacher', 'attendance', 'marks', 'fee_overdue_days', 'risk_level']], use_container_width=True)
        
        if st.button("📥 Export Student Data to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"edutrack_students_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with tab6:
        st.subheader("👨‍🏫 Teacher Information")
        
        total_teachers = len(TEACHER_DATA)
        total_students_under_teachers = sum([teacher['students_count'] for teacher in TEACHER_DATA.values()])
        avg_experience = np.mean([int(teacher['experience'].split()[0]) for teacher in TEACHER_DATA.values()])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Teachers", total_teachers)
        with col2:
            st.metric("Total Students Under Teachers", total_students_under_teachers)
        with col3:
            st.metric("Average Experience (Years)", f"{avg_experience:.1f}")
        
        st.subheader("🏫 Teacher Directory")
        
        for class_name, teacher in TEACHER_DATA.items():
            class_students = [s for s in students if s['class'] == class_name]
            high_risk_count = len([s for s in class_students if s.get('risk_level') == 'High'])
            avg_attendance = np.mean([s['attendance'] for s in class_students]) if class_students else 0
            avg_marks = np.mean([s['marks'] for s in class_students]) if class_students else 0
            
            st.markdown(f'''
            <div class="teacher-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 2;">
                        <h3>{teacher["name"]}</h3>
                        <p><strong>Class:</strong> {class_name} | <strong>Subject:</strong> {teacher["subject"]}</p>
                        <p><strong>Experience:</strong> {teacher["experience"]} | <strong>Students:</strong> {len(class_students)}</p>
                        <p><strong>Email:</strong> {teacher["email"]} | <strong>Phone:</strong> {teacher["phone"]}</p>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; margin-bottom: 5px;">
                            <p style="margin: 0;">Avg Attendance<br><strong>{avg_attendance:.1f}%</strong></p>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; margin-bottom: 5px;">
                            <p style="margin: 0;">Avg Marks<br><strong>{avg_marks:.1f}%</strong></p>
                        </div>
                        <div style="background: rgba(255,107,107,0.8); padding: 10px; border-radius: 8px;">
                            <p style="margin: 0;">High Risk<br><strong>{high_risk_count}</strong></p>
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.subheader("📋 Teacher Performance Summary")
        
        teacher_performance = []
        for class_name, teacher in TEACHER_DATA.items():
            class_students = [s for s in students if s['class'] == class_name]
            if class_students:
                avg_attendance = np.mean([s['attendance'] for s in class_students])
                avg_marks = np.mean([s['marks'] for s in class_students])
                high_risk_count = len([s for s in class_students if s.get('risk_level') == 'High'])
                medium_risk_count = len([s for s in class_students if s.get('risk_level') == 'Medium'])
                
                teacher_performance.append({
                    'Teacher': teacher['name'],
                    'Class': class_name,
                    'Subject': teacher['subject'],
                    'Experience': teacher['experience'],
                    'Students': len(class_students),
                    'Avg Attendance': round(avg_attendance, 1),
                    'Avg Marks': round(avg_marks, 1),
                    'High Risk': high_risk_count,
                    'Medium Risk': medium_risk_count
                })
        
        if teacher_performance:
            performance_df = pd.DataFrame(teacher_performance)
            st.dataframe(performance_df, use_container_width=True)
            
            if st.button("📥 Export Teacher Data to CSV"):
                csv = performance_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"edutrack_teachers_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

def main():
    """Main function to control app flow"""
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()