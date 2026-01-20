"""
SENTINEL AI - Trends Tab
=========================
Statistical trends and distribution analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def render_trends_tab(data, files_count):
    """Render the Trends & Statistics tab content"""
    st.markdown("### 📈 Statistical Trends & Distribution Analysis")
    
    # Top row - Main distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Violin plot for anomaly score by risk level
        fig_violin = go.Figure()
        for risk in ['NORMAL', 'HIGH', 'CRITICAL']:
            risk_data = data[data['risk_level'] == risk]['anomaly_score']
            if len(risk_data) > 0:
                fig_violin.add_trace(go.Violin(
                    y=risk_data,
                    name=risk,
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor='rgba(255,71,87,0.5)' if risk == 'CRITICAL' else ('rgba(255,165,2,0.5)' if risk == 'HIGH' else 'rgba(46,213,115,0.5)'),
                    line_color='#ff4757' if risk == 'CRITICAL' else ('#ffa502' if risk == 'HIGH' else '#2ed573')
                ))
        
        fig_violin.update_layout(
            title='Anomaly Score Distribution by Risk Level',
            height=400,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=40, l=40, r=40),
            yaxis_title="Anomaly Score",
            showlegend=True
        )
        st.plotly_chart(fig_violin, use_container_width=True)
    
    with col2:
        # Enhanced histogram with KDE overlay
        if 'compliance_rate' in data.columns:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=data['compliance_rate'],
                nbinsx=25,
                name='Compliance Rate',
                marker_color='#667eea',
                opacity=0.7
            ))
            
            fig_hist.update_layout(
                title='Compliance Rate Distribution',
                height=400,
                template='plotly_white',
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=40, l=40, r=40),
                xaxis_title="Compliance Rate (%)",
                yaxis_title="Frequency",
                showlegend=False
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=data['youth_ratio'],
                nbinsx=25,
                name='Youth Ratio',
                marker_color='#667eea',
                opacity=0.7
            ))
            
            fig_hist.update_layout(
                title='Youth Ratio Distribution',
                height=400,
                template='plotly_white',
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=40, l=40, r=40),
                xaxis_title="Youth Ratio (%)",
                yaxis_title="Frequency",
                showlegend=False
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Second row - Correlation and advanced analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Multi-metric box plot comparison
        if files_count >= 2 and 'compliance_rate' in data.columns:
            metrics_data = []
            for metric in ['anomaly_score', 'compliance_rate']:
                for val in data[metric]:
                    metrics_data.append({'Metric': metric.replace('_', ' ').title(), 'Value': val})
            
            metrics_df = pd.DataFrame(metrics_data)
            fig_multi_box = px.box(
                metrics_df,
                x='Metric',
                y='Value',
                color='Metric',
                title='Key Metrics Distribution Comparison',
                height=400,
                color_discrete_map={
                    'Anomaly Score': '#ff4757',
                    'Compliance Rate': '#667eea'
                }
            )
        else:
            fig_multi_box = px.box(
                data,
                y='anomaly_score',
                color='risk_level',
                title='Anomaly Score by Risk Category',
                height=400,
                color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'}
            )
        
        fig_multi_box.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=40, l=40, r=40)
        )
        st.plotly_chart(fig_multi_box, use_container_width=True)
    
    with col2:
        # Ridge plot style - multiple distributions
        fig_ridge = go.Figure()
        
        percentiles = [25, 50, 75]
        for i, pct in enumerate(percentiles):
            threshold = data['anomaly_score'].quantile(pct / 100)
            subset = data[data['anomaly_score'] <= threshold]
            
            fig_ridge.add_trace(go.Violin(
                x=subset['anomaly_score'],
                name=f'{pct}th Percentile',
                orientation='h',
                side='positive',
                line_color=['#2ed573', '#ffa502', '#ff4757'][i]
            ))
        
        fig_ridge.update_layout(
            title='Anomaly Score Percentile Distribution',
            height=400,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=40, l=40, r=40),
            xaxis_title="Anomaly Score",
            yaxis_title="Percentile Group"
        )
        st.plotly_chart(fig_ridge, use_container_width=True)
    
    # Correlation heatmap (if multiple datasets)
    if files_count >= 2:
        st.markdown("---")
        st.markdown("#### 🔗 Correlation Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            numeric_cols = ['enrol_total', 'demo_total', 'bio_total', 'compliance_rate', 'anomaly_score']
            corr_data = data[numeric_cols].corr()
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=corr_data.values,
                x=[col.replace('_', ' ').title() for col in corr_data.columns],
                y=[col.replace('_', ' ').title() for col in corr_data.index],
                colorscale='RdBu_r',
                zmid=0,
                text=corr_data.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 12},
                colorbar=dict(title="Correlation")
            ))
            
            fig_heatmap.update_layout(
                title='Metric Correlation Matrix',
                height=400,
                template='plotly_white',
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=80, l=80, r=40)
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            # Statistical summary table
            st.markdown("#### 📊 Statistical Summary")
            summary_stats = data[['anomaly_score', 'compliance_rate']].describe().round(2)
            summary_stats.index = ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']
            st.dataframe(summary_stats, use_container_width=True, height=360)
    
    st.markdown("---")
    
    # Third row - Time-based or sequential analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Cumulative distribution
        sorted_scores = np.sort(data['anomaly_score'])
        cumulative = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores) * 100
        
        fig_cdf = go.Figure()
        fig_cdf.add_trace(go.Scatter(
            x=sorted_scores,
            y=cumulative,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#667eea', width=2),
            name='CDF'
        ))
        
        fig_cdf.update_layout(
            title='Cumulative Distribution',
            height=300,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=10),
            xaxis_title="Anomaly Score",
            yaxis_title="Cumulative %"
        )
        st.plotly_chart(fig_cdf, use_container_width=True)
    
    with col2:
        # Score range analysis
        bins = [0, 30, 60, 100]
        labels = ['Low', 'Medium', 'High']
        data_copy = data.copy()
        data_copy['Score Range'] = pd.cut(data_copy['anomaly_score'], bins=bins, labels=labels)
        range_counts = data_copy['Score Range'].value_counts()
        
        fig_range = go.Figure(go.Bar(
            x=range_counts.index,
            y=range_counts.values,
            marker_color=['#2ed573', '#ffa502', '#ff4757'],
            text=range_counts.values,
            textposition='outside'
        ))
        
        fig_range.update_layout(
            title='Score Range Distribution',
            height=300,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=10),
            xaxis_title="Score Range",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_range, use_container_width=True)
    
    with col3:
        # Outlier detection visualization
        Q1 = data['anomaly_score'].quantile(0.25)
        Q3 = data['anomaly_score'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data['anomaly_score'] < (Q1 - 1.5 * IQR)) | (data['anomaly_score'] > (Q3 + 1.5 * IQR))]
        
        fig_outlier = go.Figure()
        fig_outlier.add_trace(go.Box(
            y=data['anomaly_score'],
            name='All Data',
            marker_color='#667eea',
            boxpoints='outliers'
        ))
        
        fig_outlier.update_layout(
            title=f'Outlier Detection ({len(outliers)} outliers)',
            height=300,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=10),
            yaxis_title="Anomaly Score",
            showlegend=False
        )
        st.plotly_chart(fig_outlier, use_container_width=True)