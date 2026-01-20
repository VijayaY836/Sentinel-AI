"""
SENTINEL AI - Data Quality Tab
===============================
Advanced data cleansing report and quality metrics.
"""

import streamlit as st
import plotly.graph_objects as go


def render_quality_tab(cleansing_report):
    """Render the Data Quality tab content"""
    st.markdown("### 🧹 Advanced Data Cleansing Report")
    
    if cleansing_report:
        report = cleansing_report
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #667eea; text-align: center;'>
                <div class='stat-label'>Rows Processed</div>
                <div class='big-stat' style='color: #667eea; font-size: 2rem;'>{report['total_rows_before']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #2ed573; text-align: center;'>
                <div class='stat-label'>Rows Retained</div>
                <div class='big-stat' style='color: #2ed573; font-size: 2rem;'>{report['total_rows_after']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #ff4757; text-align: center;'>
                <div class='stat-label'>Anomalies Removed</div>
                <div class='big-stat' style='color: #ff4757; font-size: 2rem;'>{report['rows_removed']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #ffa502; text-align: center;'>
                <div class='stat-label'>Removal Rate</div>
                <div class='big-stat' style='color: #ffa502; font-size: 2rem;'>{report['removal_rate']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed cleansing breakdown
        if report['detailed_reports']:
            st.markdown("#### 📊 Cleansing Pipeline Results")
            
            for idx, detailed_report in enumerate(report['detailed_reports']):
                with st.expander(f"📁 Dataset {idx + 1} - Detailed Analysis", expanded=(idx==0)):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 🔍 Outlier Detection (Isolation Forest)")
                        outlier_info = detailed_report.get('outliers', {})
                        st.write(f"- Outliers Detected: **{outlier_info.get('outliers_detected', 0)}**")
                        st.write(f"- Outliers Removed: **{outlier_info.get('outliers_removed', 0)}**")
                        st.write(f"- Features Analyzed: **{outlier_info.get('features_analyzed', 0)}**")
                        
                        st.markdown("##### 📊 Missing Values")
                        missing_info = detailed_report.get('missing_values', {})
                        st.write(f"- Missing Before: **{missing_info.get('missing_before', 0)}**")
                        st.write(f"- Values Imputed: **{missing_info.get('imputed_values', 0)}**")
                    
                    with col2:
                        st.markdown("##### 🎯 Clustering Analysis (DBSCAN)")
                        cluster_info = detailed_report.get('clusters', {})
                        st.write(f"- Clusters Found: **{cluster_info.get('clusters_found', 0)}**")
                        st.write(f"- Unclustered Anomalies: **{cluster_info.get('unclustered_anomalies', 0)}**")
                        
                        st.markdown("##### 📝 Fuzzy Matching")
                        fuzzy_info = detailed_report.get('fuzzy_matching', {})
                        st.write(f"- Corrections Made: **{fuzzy_info.get('corrections_made', 0)}**")
                    
                    # Quality distribution
                    quality_info = detailed_report.get('quality', {})
                    if quality_info:
                        st.markdown("##### ⭐ Data Quality Assessment")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Average Quality", f"{quality_info.get('avg_quality_score', 0):.1f}/100")
                        col2.metric("Minimum Quality", f"{quality_info.get('min_quality_score', 0):.1f}/100")
                        col3.metric("Maximum Quality", f"{quality_info.get('max_quality_score', 0):.1f}/100")
                        
                        # Quality distribution chart
                        quality_dist = quality_info.get('quality_distribution', {})
                        if quality_dist:
                            fig_quality = go.Figure(go.Bar(
                                x=list(quality_dist.keys()),
                                y=list(quality_dist.values()),
                                marker_color=['#ff4757', '#ffa502', '#2ed573', '#667eea'],
                                text=list(quality_dist.values()),
                                textposition='outside'
                            ))
                            fig_quality.update_layout(
                                title='Quality Rating Distribution',
                                height=300,
                                template='plotly_white',
                                plot_bgcolor='rgba(255,255,255,0.9)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                margin=dict(t=50, b=40, l=40, r=40),
                                xaxis_title="Quality Rating",
                                yaxis_title="Count"
                            )
                            st.plotly_chart(fig_quality, use_container_width=True)
        
        st.markdown("---")
        st.markdown("""
        #### 🧠 ML-Powered Cleansing Techniques Used:
        
        1. **Isolation Forest**: Unsupervised anomaly detection in high-dimensional space
        2. **DBSCAN Clustering**: Identifies coordinated fraud patterns and systematic issues
        3. **KNN Imputation**: Intelligent missing value imputation using nearest neighbors
        4. **Fuzzy String Matching**: Standardizes categorical data with typo correction
        5. **Quality Scoring**: Comprehensive data quality assessment (completeness, consistency, reliability)
        """)
    
    else:
        st.info("Data quality report will appear here after analyzing datasets.")