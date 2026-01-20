"""
SENTINEL AI - UI Styling Components
====================================
All CSS styling and visual theme configuration.
"""

import streamlit as st
import base64
import os


def get_base64_bg():
    """Load background image and convert to base64"""
    try:
        if os.path.exists("bg.png"):
            with open("bg.png", "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
        else:
            for path in ["./bg.png", "../bg.png", "bg.png"]:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        data = base64.b64encode(f.read()).decode()
                    return f"data:image/png;base64,{data}"
    except Exception as e:
        pass
    return None


def apply_custom_styles():
    """Apply all custom CSS styling to the Streamlit app"""
    bg_image = get_base64_bg()
    
    bg_style = f"""
        .stApp {{
            background-image: url('{bg_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    """ if bg_image else """
        .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 50%, #f5f7fa 100%);
        }}
    """
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
        
        * {{ font-family: 'Inter', sans-serif; }}
        
        {bg_style}
        
        .main {{ color: #1a1a1a; }}
        
        [data-testid="stSidebar"] {{ display: none; }}
        section[data-testid="stSidebar"] {{ display: none; }}
        
        h1, h2, h3 {{ color: #1a1a1a !important; text-shadow: none; }}
        p {{ text-shadow: none; color: #2d2d2d; }}
        
        .metric-card {{
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        
        .critical {{ border-left: 4px solid #ff4757; }}
        .high {{ border-left: 4px solid #ffa502; }}
        .normal {{ border-left: 4px solid #2ed573; }}
        
        .big-stat {{
            font-size: 3rem;
            font-weight: 900;
            line-height: 1;
            margin: 8px 0;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 32px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: rgba(255,255,255,0.6);
            padding: 10px;
            border-radius: 12px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: rgba(255,255,255,0.8);
            border-radius: 8px;
            color: #1a1a1a;
            font-weight: 600;
            padding: 12px 24px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        div[data-testid="stExpander"] {{
            background: rgba(255,255,255,0.8);
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 8px;
            margin: 8px 0;
        }}
        
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main header section"""
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 4.5rem; font-weight: 900; margin: 0; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   filter: drop-shadow(0 0 20px rgba(102,126,234,0.5));'>
            🛡️ SENTINEL AI
        </h1>
        <p style='font-size: 1.4rem; opacity: 0.95; margin-top: 10px; font-weight: 600;'>
            National Aadhaar Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, color):
    """Render a styled metric card"""
    st.markdown(f"""
    <div class='metric-card' style='border-left: 4px solid {color};'>
        <div class='stat-label'>{label}</div>
        <div class='big-stat' style='color: {color};'>{value}</div>
    </div>
    """, unsafe_allow_html=True)