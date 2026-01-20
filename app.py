"""
SENTINEL AI - Aadhaar Societal Trends Analysis Platform
========================================================
Unlocking enrollment patterns to support informed policy-making
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import custom modules
from components.styles import apply_custom_styles, render_header, render_metric_card
from components.ml_models import train_ml_models
from utils.data_processing import analyze_single_dataset, analyze_multiple_datasets
from data_cleanser import SentinelDataCleanser

# Import all tab renderers
from tabs.tab_overview import render_overview_tab
from tabs.tab_geographic import render_geographic_tab
from tabs.tab_trends import render_trends_tab
from tabs.tab_ai_models import render_ai_models_tab
from tabs.tab_alerts import render_alerts_tab
from tabs.tab_quality import render_quality_tab

# Page configuration
st.set_page_config(
    page_title="Aadhaar Societal Trends Platform", 
    layout="wide", 
    page_icon="🛡️"
)

# Initialize session state
if 'data_processed' not in st.session_state:
    st.session_state.data_processed = False
if 'district_data' not in st.session_state:
    st.session_state.district_data = None
if 'ml_results' not in st.session_state:
    st.session_state.ml_results = None
if 'cleansing_report' not in st.session_state:
    st.session_state.cleansing_report = None

# Apply styling
apply_custom_styles()

# Header with Societal Focus
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
        Aadhaar Societal Trends & Insights Platform
    </p>
    <p style='font-size: 1rem; opacity: 0.8; margin-top: 5px;'>
        Unlocking enrollment patterns to support informed policy-making
    </p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div style='background: rgba(255,243,205,0.3); padding: 15px; border-radius: 8px; 
            border-left: 4px solid #667eea; margin: 20px 0;'>
    <p style='margin: 0; font-size: 0.9rem; color: #1a1a1a;'>
        <strong>ℹ️ Methodology Note:</strong> This platform identifies enrollment and update patterns 
        using machine learning to reveal societal trends such as migration flows, demographic shifts, 
        and administrative load distribution. All analysis is based on aggregate statistical patterns, 
        not individual citizen assessments.
    </p>
</div>
""", unsafe_allow_html=True)

# File Upload Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.container():
        uploaded_files_list = st.file_uploader(
            "📂 Load Aadhaar Data",
            type=['csv'],
            accept_multiple_files=True,
            key='multi_upload'
        )
        
        if uploaded_files_list:
            if st.button("🚀 Analyze Trends", use_container_width=True):
                with st.spinner("🧠 Processing enrollment data and identifying patterns..."):
                    files_count = len(uploaded_files_list)
                    df_enrol = df_demo = df_bio = None
                    
                    # Cleansing statistics
                    total_rows_before = total_rows_after = 0
                    all_reports = []
                    cleanser = SentinelDataCleanser(contamination=0.05, verbose=False)
                    
                    # Process each file
                    for file in uploaded_files_list:
                        df_raw = pd.read_csv(file)
                        rows_before = len(df_raw)
                        total_rows_before += rows_before
                        
                        # Apply ML-powered cleansing
                        df_clean, cleansing_report = cleanser.clean_pipeline(df_raw)
                        rows_after = len(df_clean)
                        total_rows_after += rows_after
                        all_reports.append(cleansing_report)
                        
                        # Standardization
                        df_clean.columns = [c.strip().lower().replace('_', ' ') for c in df_clean.columns]
                        for col in ['state', 'district']:
                            if col in df_clean.columns:
                                df_clean[col] = df_clean[col].str.strip().str.title()
                        
                        # Classify dataset
                        filename = file.name.lower()
                        if 'enrol' in filename or 'enrollment' in filename:
                            df_enrol = df_clean
                        elif 'demo' in filename or 'demographic' in filename:
                            df_demo = df_clean
                        elif 'bio' in filename or 'biometric' in filename:
                            df_bio = df_clean
                        else:
                            if df_enrol is None:
                                df_enrol = df_clean
                            elif df_demo is None:
                                df_demo = df_clean
                            else:
                                df_bio = df_clean
                    
                    # Store cleansing report
                    st.session_state.cleansing_report = {
                        'total_rows_before': total_rows_before,
                        'total_rows_after': total_rows_after,
                        'rows_removed': total_rows_before - total_rows_after,
                        'removal_rate': ((total_rows_before - total_rows_after) / total_rows_before * 100) if total_rows_before > 0 else 0,
                        'detailed_reports': all_reports
                    }
                    
                    # Show cleansing results (USER-FACING LANGUAGE)
                    if total_rows_before > total_rows_after:
                        rows_removed = total_rows_before - total_rows_after
                        st.success(f"✨ Data Quality Enhancement: {rows_removed:,} incomplete records filtered ({(rows_removed/total_rows_before*100):.1f}%)")
                        
                        if all_reports and 'quality' in all_reports[0]:
                            avg_quality = np.mean([r['quality']['avg_quality_score'] for r in all_reports])
                            st.info(f"📊 Data Completeness Score: {avg_quality:.1f}/100")
                    
                    # Analyze datasets (INTERNAL LOGIC UNCHANGED)
                    if files_count >= 2:
                        district_data = analyze_multiple_datasets(df_enrol, df_demo, df_bio)
                    else:
                        if df_enrol is not None:
                            single_df = df_enrol
                            dtype = 'enrol'
                        elif df_demo is not None:
                            single_df = df_demo
                            dtype = 'demo'
                        else:
                            single_df = df_bio
                            dtype = 'bio'
                        district_data = analyze_single_dataset(single_df, dtype)
                    
                    # Train ML models (INTERNAL LOGIC UNCHANGED)
                    district_data, ml_results = train_ml_models(district_data, files_count)
                    
                    st.session_state.district_data = district_data
                    st.session_state.ml_results = ml_results
                    st.session_state.data_processed = True
                    st.session_state.files_count = files_count
                st.rerun()

# Main Dashboard
if st.session_state.data_processed and st.session_state.district_data is not None:
    data = st.session_state.district_data
    files_count = st.session_state.get('files_count', 1)
    
    # Helper function to translate internal terms to user-facing terms
    def display_term(internal_term):
        """Translate internal terminology to user-facing language"""
        mapping = {
            'CRITICAL': 'High Activity',
            'HIGH': 'Elevated Activity',
            'NORMAL': 'Standard Activity',
            'risk_level': 'Activity Level',
            'anomaly_score': 'System Stress Index'
        }
        return mapping.get(internal_term, internal_term)
    
    # Display top metrics (USER-FACING LABELS)
    if files_count >= 2:
        high_activity_count = len(data[data['risk_level'] == 'CRITICAL'])  # Internal: risk_level
        total_gap = data[data['gap'] > 0]['gap'].sum() if 'gap' in data.columns else 0
        avg_completion = data['compliance_rate'].mean() if 'compliance_rate' in data.columns else 0
        top_district = data.iloc[0]['district']
        
        metric_configs = [
            ("📍 High Activity Zones", high_activity_count, "#667eea"),  # User-facing label
            ("⏳ Pending Updates", f"{int(total_gap):,}", "#ffa502"),
            ("✅ Update Completion", f"{avg_completion:.1f}%", "#2ed573"),
            ("🎯 Top District", top_district, "#764ba2")
        ]
    else:
        high_activity_count = len(data[data['risk_level'] == 'CRITICAL'])  # Internal: risk_level
        total_updates = int(data['total_updates'].sum()) if 'total_updates' in data.columns else 0
        avg_youth = data['youth_ratio'].mean() if 'youth_ratio' in data.columns else 0
        top_district = data.iloc[0]['district']
        
        metric_configs = [
            ("📍 High Activity Zones", high_activity_count, "#667eea"),  # User-facing label
            ("📈 Total Transactions", f"{total_updates:,}", "#ffa502"),
            ("👥 Youth Enrollment", f"{avg_youth:.1f}%", "#2ed573"),
            ("🎯 Peak District", top_district, "#764ba2")
        ]
    
    cols = st.columns(4)
    for idx, (label, value, color) in enumerate(metric_configs):
        with cols[idx]:
            render_metric_card(label, value, color)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Societal Insights Section
    st.markdown("## 💡 Key Societal Insights")
    st.markdown("*Policy-relevant findings from enrollment and update pattern analysis*")
    
    # Generate insights dynamically from data
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        # Youth enrollment insight
        if 'youth_ratio' in data.columns:
            avg_youth = data['youth_ratio'].mean()
            high_youth_districts = len(data[data['youth_ratio'] > 70])
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 12px; 
                        margin: 15px 0; border-left: 5px solid #667eea; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <h4 style='color: #667eea; margin: 0 0 10px 0;'>👥 Demographic Trends</h4>
                <p style='margin: 8px 0; font-weight: 600; color: #2d2d2d;'>
                    📌 <strong>Finding:</strong> {high_youth_districts} districts show youth-dominant enrollment patterns
                </p>
                <p style='margin: 8px 0; color: #4a4a4a; line-height: 1.6;'>
                    💡 <strong>Interpretation:</strong> This correlates with education migration hubs, first-time enrollment drives, 
                    and urban-rural youth mobility. Suggests administrative capacity planning needed for youth-centric services.
                </p>
                <p style='margin: 8px 0; padding: 10px; background: rgba(102,126,234,0.1); 
                           border-radius: 6px; color: #1a1a1a;'>
                    ✅ <strong>Actionable:</strong> Deploy mobile enrollment units near educational institutions during admission seasons.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with insights_col2:
        # Geographic concentration insight
        state_concentration = data.groupby('state')['district'].count().sort_values(ascending=False)
        top_state = state_concentration.index[0]
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 12px; 
                    margin: 15px 0; border-left: 5px solid #2ed573; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <h4 style='color: #2ed573; margin: 0 0 10px 0;'>🗺️ Geographic Load Distribution</h4>
            <p style='margin: 8px 0; font-weight: 600; color: #2d2d2d;'>
                📌 <strong>Finding:</strong> {top_state} shows highest administrative activity concentration
            </p>
            <p style='margin: 8px 0; color: #4a4a4a; line-height: 1.6;'>
                💡 <strong>Interpretation:</strong> High enrollment/update density indicates population growth centers, 
                migration destination states, and improved digital infrastructure adoption.
            </p>
            <p style='margin: 8px 0; padding: 10px; background: rgba(46,213,115,0.1); 
                       border-radius: 6px; color: #1a1a1a;'>
                ✅ <strong>Actionable:</strong> Increase permanent enrollment centers in {top_state}; 
                analyze staffing ratios vs. population density.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📊 Detailed Analytics Dashboard")
    
    # ML Performance Section (USER-FACING LABELS)
    if st.session_state.ml_results:
        st.markdown("### 🤖 Pattern Detection Engine Performance")
        ml_results = st.session_state.ml_results
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'isolation_forest' in ml_results:
                pattern_pct = (ml_results['isolation_forest']['anomalies_detected'] / 
                              ml_results['isolation_forest']['total_samples'] * 100)
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #667eea; text-align: center;'>
                    <div class='stat-label'>🔍 Pattern Detection</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #667eea; margin: 8px 0;'>
                        {pattern_pct:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>Unusual Patterns Identified</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if 'random_forest' in ml_results:
                accuracy = ml_results['random_forest']['accuracy'] * 100
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #2ed573; text-align: center;'>
                    <div class='stat-label'>🎯 Classification Model</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #2ed573; margin: 8px 0;'>
                        {accuracy:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>Prediction Accuracy</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if 'gradient_boosting' in ml_results:
                r2 = ml_results['gradient_boosting']['r2_score'] * 100
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #ffa502; text-align: center;'>
                    <div class='stat-label'>📈 Forecasting Model</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #ffa502; margin: 8px 0;'>
                        {r2:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>R² Score</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if 'ml_ensemble_score' in data.columns:
                ml_high = len(data[data['ml_risk_level'] == 'CRITICAL']) if 'ml_risk_level' in data.columns else 0
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #764ba2; text-align: center;'>
                    <div class='stat-label'>🧠 AI Ensemble</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #764ba2; margin: 8px 0;'>
                        {ml_high}
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>High-Activity Patterns</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs (USER-FACING LABELS)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "🗺️ Geographic Trends", 
        "📈 Statistical Analysis", 
        "🤖 Pattern Detection", 
        "📍 Focus Areas", 
        "🧹 Data Quality"
    ])
    
    with tab1:
        render_overview_tab(data, files_count)
    
    with tab2:
        render_geographic_tab(data, files_count)
    
    with tab3:
        render_trends_tab(data, files_count)
    
    with tab4:
        render_ai_models_tab(data, st.session_state.ml_results)
    
    with tab5:
        render_alerts_tab(data, files_count)
    
    with tab6:
        render_quality_tab(st.session_state.cleansing_report)

else:
    # Welcome screen
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        ("🔍 Pattern Discovery", "ML-powered identification of enrollment and update trends"),
        ("📊 Societal Insights", "Translate data patterns into policy-relevant findings"),
        ("🗺️ Geographic Analysis", "Regional enrollment dynamics and administrative load mapping")
    ]
    
    for idx, (title, desc) in enumerate(features):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; min-height: 180px;'>
                <h3 style='margin-bottom: 15px; font-size: 1.5rem;'>{title}</h3>
                <p style='opacity: 0.8; font-size: 1rem;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👆 Upload Aadhaar enrollment/update datasets to discover societal trends and patterns", icon="💡")
