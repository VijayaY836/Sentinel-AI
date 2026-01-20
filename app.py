"""
SENTINEL AI - Main Application
===============================
National Aadhaar Intelligence Platform
Streamlined architecture with modular components.
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
st.set_page_config(page_title="Aadhaar Sentinel AI", layout="wide", page_icon="🛡️")

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
render_header()

# File Upload Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.container():
        uploaded_files_list = st.file_uploader(
            "📂 Load Data",
            type=['csv'],
            accept_multiple_files=True,
            key='multi_upload'
        )
        
        if uploaded_files_list:
            if st.button("🚀 Analyze", use_container_width=True):
                with st.spinner("🧠 Advanced data cleansing and ML training in progress..."):
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
                    
                    # Show cleansing results
                    if total_rows_before > total_rows_after:
                        rows_removed = total_rows_before - total_rows_after
                        st.success(f"✨ Advanced ML Cleansing Complete: {rows_removed:,} anomalous rows removed ({(rows_removed/total_rows_before*100):.1f}%)")
                        
                        if all_reports and 'quality' in all_reports[0]:
                            avg_quality = np.mean([r['quality']['avg_quality_score'] for r in all_reports])
                            st.info(f"📊 Data Quality Score: {avg_quality:.1f}/100")
                    
                    # Analyze datasets
                    if files_count >= 2:
                        district_data = analyze_multiple_datasets(df_enrol, df_demo, df_bio)
                    else:
                        # Fix: Use 'is not None' instead of boolean 'or'
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
                    
                    # Train ML models
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
    
    # Display top metrics
    if files_count >= 2:
        critical_count = len(data[data['risk_level'] == 'CRITICAL'])
        total_gap = data[data['gap'] > 0]['gap'].sum() if 'gap' in data.columns else 0
        avg_compliance = data['compliance_rate'].mean() if 'compliance_rate' in data.columns else 0
        top_district = data.iloc[0]['district']
        
        metric_configs = [
            ("🚨 Critical Zones", critical_count, "#ff4757"),
            ("⚠️ Unverified", f"{int(total_gap):,}", "#ffa502"),
            ("📊 Compliance", f"{avg_compliance:.1f}%", "#5f27cd"),
            ("🎯 Top Risk", top_district, "#764ba2")
        ]
    else:
        critical_count = len(data[data['risk_level'] == 'CRITICAL'])
        total_updates = int(data['total_updates'].sum()) if 'total_updates' in data.columns else 0
        avg_youth_ratio = data['youth_ratio'].mean() if 'youth_ratio' in data.columns else 0
        top_district = data.iloc[0]['district']
        
        metric_configs = [
            ("🚨 High Activity", critical_count, "#ff4757"),
            ("📈 Total Updates", f"{total_updates:,}", "#ffa502"),
            ("👥 Youth Ratio", f"{avg_youth_ratio:.1f}%", "#5f27cd"),
            ("🎯 Hotspot", top_district, "#764ba2")
        ]
    
    cols = st.columns(4)
    for idx, (label, value, color) in enumerate(metric_configs):
        with cols[idx]:
            render_metric_card(label, value, color)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ML Performance Section
    if st.session_state.ml_results:
        st.markdown("### 🤖 AI-Powered Intelligence Engine")
        ml_results = st.session_state.ml_results
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'isolation_forest' in ml_results:
                anomaly_pct = (ml_results['isolation_forest']['anomalies_detected'] / 
                              ml_results['isolation_forest']['total_samples'] * 100)
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #667eea; text-align: center;'>
                    <div class='stat-label'>🔍 Isolation Forest</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #667eea; margin: 8px 0;'>
                        {anomaly_pct:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>Anomalies Detected</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if 'random_forest' in ml_results:
                accuracy = ml_results['random_forest']['accuracy'] * 100
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #2ed573; text-align: center;'>
                    <div class='stat-label'>🎯 Random Forest</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #2ed573; margin: 8px 0;'>
                        {accuracy:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>Classification Accuracy</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if 'gradient_boosting' in ml_results:
                r2 = ml_results['gradient_boosting']['r2_score'] * 100
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #ffa502; text-align: center;'>
                    <div class='stat-label'>📈 Gradient Boosting</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #ffa502; margin: 8px 0;'>
                        {r2:.1f}%
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>R² Score</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if 'ml_ensemble_score' in data.columns:
                ml_critical = len(data[data['ml_risk_level'] == 'CRITICAL']) if 'ml_risk_level' in data.columns else 0
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #764ba2; text-align: center;'>
                    <div class='stat-label'>🧠 AI Ensemble</div>
                    <div style='font-size: 1.8rem; font-weight: 700; color: #764ba2; margin: 8px 0;'>
                        {ml_critical}
                    </div>
                    <div style='font-size: 0.8rem; opacity: 0.7;'>ML-Detected Critical</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs - ALL FUNCTIONAL NOW!
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "🗺️ Geographic", "📈 Trends", 
        "🤖 AI Models", "⚠️ Alerts", "🧹 Data Quality"
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
        ("🤖 AI-Powered", "Multi-model ML ensemble with 3 algorithms"),
        ("⚡ Adaptive Analysis", "Automatically detects patterns in 1-3 datasets"),
        ("📊 Rich Visualizations", "20+ interactive charts and insights")
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
    st.info("👆 Upload your Aadhaar datasets using the file uploader above to begin analysis", icon="💡")