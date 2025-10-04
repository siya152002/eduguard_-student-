# Configuration and styling constants

# Page Configuration
PAGE_CONFIG = {
    'page_title': "EduGuard • Student Success Platform",
    'page_icon': "🎓",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Custom CSS for Beautiful UI
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
    }
    
    .risk-high {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .risk-medium {
        background: linear-gradient(45deg, #ffd93d, #ffbe0b);
        color: black;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .risk-low {
        background: linear-gradient(45deg, #6bcf7f, #4caf50);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid;
    }
    
    .notification-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
"""

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