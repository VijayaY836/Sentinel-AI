"""
SENTINEL AI - Overview Tab
===========================
Main dashboard overview visualizations.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_overview_tab(data, files_count):
    """Render the Overview tab content"""
    st.markdown("### 📊 Risk Intelligence Dashboard")
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        if files_count >= 2 and 'demo_total' in data.columns:
            # Scatter plot with trendline
            fig = px.scatter(data, 
                             x='demo_total', 
                             y='bio_total',
                             size='gap_abs',
                             color='anomaly_score',
                             hover_name='district',
                             hover_data={
                                 'state': True,
                                 'demo_total': ':,',
                                 'bio_total': ':,',
                                 'compliance_rate': ':.1f',
                                 'anomaly_score': ':.0f',
                                 'gap_abs': False
                             },
                             color_continuous_scale='Reds',
                             height=450,
                             labels={'demo_total': 'Demographic Updates', 'bio_total': 'Biometric Updates'})
            
            max_val = max(data['demo_total'].max(), data['bio_total'].max())
            fig.add_trace(go.Scatter(
                x=[0, max_val], 
                y=[0, max_val],
                mode='lines',
                name='Perfect Compliance',
                line=dict(color='#2ed573', dash='dash', width=2),
                showlegend=True
            ))
            
            fig.update_layout(
                template='plotly_white', 
                plot_bgcolor='rgba(255,255,255,0.9)', 
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=16,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Horizontal bar chart
            fig = px.bar(data.head(20), 
                         x='anomaly_score', 
                         y='district',
                         color='risk_level',
                         orientation='h',
                         color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
                         height=450,
                         labels={'anomaly_score': 'Risk Score', 'district': 'District'},
                         text='anomaly_score')
            
            fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            fig.update_layout(
                template='plotly_white', 
                plot_bgcolor='rgba(255,255,255,0.9)', 
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=16,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk Distribution Donut Chart
        risk_counts = data['risk_level'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color=risk_counts.index,
            color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
            hole=0.5,
            height=220,
            title='Risk Level Distribution'
        )
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        fig_pie.update_layout(
            template='plotly_white', 
            plot_bgcolor='rgba(255,255,255,0.9)', 
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title_font_size=14,
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Gauge chart
        avg_risk = data['anomaly_score'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_risk,
            title={'text': "Average Risk Score", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': "#e8f5e9"},
                    {'range': [30, 60], 'color': "#fff3e0"},
                    {'range': [60, 100], 'color': "#ffebee"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 60
                }
            },
            number={'font': {'size': 32}}
        ))
        fig_gauge.update_layout(
            height=220,
            margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown("---")
    
    # Second row - Detailed metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Top 10 Risk Districts")
        top_10 = data.head(10)
        fig_top = go.Figure(go.Bar(
            x=top_10['anomaly_score'],
            y=top_10['district'],
            orientation='h',
            marker=dict(
                color=top_10['anomaly_score'],
                colorscale='Reds',
                showscale=False
            ),
            text=top_10['anomaly_score'].round(0),
            textposition='outside'
        ))
        fig_top.update_layout(
            height=350,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=40),
            xaxis_title="Risk Score",
            yaxis_title="",
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Risk Score Distribution")
        fig_box = go.Figure()
        for risk in ['CRITICAL', 'HIGH', 'NORMAL']:
            risk_data = data[data['risk_level'] == risk]['anomaly_score']
            if len(risk_data) > 0:
                fig_box.add_trace(go.Box(
                    y=risk_data,
                    name=risk,
                    marker_color='#ff4757' if risk == 'CRITICAL' else ('#ffa502' if risk == 'HIGH' else '#2ed573')
                ))
        
        fig_box.update_layout(
            height=350,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=10),
            yaxis_title="Anomaly Score",
            showlegend=True
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col3:
        st.markdown("#### 🗺️ State Risk Summary")
        state_risk = data.groupby('state')['anomaly_score'].mean().sort_values(ascending=False).head(10)
        
        fig_state_mini = go.Figure(go.Bar(
            x=state_risk.values,
            y=state_risk.index,
            orientation='h',
            marker=dict(
                color=state_risk.values,
                colorscale='YlOrRd',
                showscale=False
            ),
            text=state_risk.values.round(1),
            textposition='outside'
        ))
        fig_state_mini.update_layout(
            height=350,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=40),
            xaxis_title="Avg Risk Score",
            yaxis_title="",
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_state_mini, use_container_width=True)