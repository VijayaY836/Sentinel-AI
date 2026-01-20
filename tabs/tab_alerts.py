"""
SENTINEL AI - Alerts Tab
=========================
Critical alerts dashboard with actionable insights.
"""

import streamlit as st
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


def render_alerts_tab(data, files_count):
    """Render the Alerts & Action Dashboard tab content"""
    st.markdown("### ⚠️ Critical Alerts & Action Dashboard")
    
    critical_districts = data[data['risk_level'] == 'CRITICAL']
    high_districts = data[data['risk_level'] == 'HIGH']
    
    # Alert summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='border-left: 4px solid #ff4757; text-align: center;'>
            <div class='stat-label'>Critical Alerts</div>
            <div class='big-stat' style='color: #ff4757; font-size: 2.5rem;'>{len(critical_districts)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='border-left: 4px solid #ffa502; text-align: center;'>
            <div class='stat-label'>High Priority</div>
            <div class='big-stat' style='color: #ffa502; font-size: 2.5rem;'>{len(high_districts)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        urgent_count = len(data[data['anomaly_score'] > 80]) if len(data) > 0 else 0
        st.markdown(f"""
        <div class='metric-card' style='border-left: 4px solid #e74c3c; text-align: center;'>
            <div class='stat-label'>Urgent Action</div>
            <div class='big-stat' style='color: #e74c3c; font-size: 2.5rem;'>{urgent_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_affected = len(data[data['risk_level'].isin(['CRITICAL', 'HIGH'])])
        st.markdown(f"""
        <div class='metric-card' style='border-left: 4px solid #95a5a6; text-align: center;'>
            <div class='stat-label'>Total Affected</div>
            <div class='big-stat' style='color: #2d2d2d; font-size: 2.5rem;'>{total_affected}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Priority Matrix and Timeline
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Priority action matrix
        st.markdown("#### 🎯 Priority Action Matrix")
        
        priority_data = data[data['risk_level'].isin(['CRITICAL', 'HIGH'])].nlargest(20, 'anomaly_score')
        
        fig_priority = go.Figure()
        
        # Create scatter plot with urgency levels
        for risk in ['CRITICAL', 'HIGH']:
            risk_subset = priority_data[priority_data['risk_level'] == risk]
            fig_priority.add_trace(go.Scatter(
                x=risk_subset.index,
                y=risk_subset['anomaly_score'],
                mode='markers+text',
                name=risk,
                marker=dict(
                    size=15,
                    color='#ff4757' if risk == 'CRITICAL' else '#ffa502',
                    symbol='diamond' if risk == 'CRITICAL' else 'circle',
                    line=dict(width=2, color='white')
                ),
                text=risk_subset['district'].str[:10],
                textposition='top center',
                textfont=dict(size=8),
                hovertemplate='<b>%{text}</b><br>Score: %{y:.0f}<extra></extra>'
            ))
        
        fig_priority.update_layout(
            height=350,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=40, l=40, r=10),
            yaxis_title="Risk Score",
            xaxis_title="Priority Rank",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Alert severity breakdown
        st.markdown("#### 📊 Severity Breakdown")
        
        severity_data = []
        for risk_level in ['CRITICAL', 'HIGH', 'NORMAL']:
            count = len(data[data['risk_level'] == risk_level])
            severity_data.append({'Level': risk_level, 'Count': count})
        
        from pandas import DataFrame
        severity_df = DataFrame(severity_data)
        
        fig_severity = go.Figure(go.Funnel(
            y=severity_df['Level'],
            x=severity_df['Count'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=['#ff4757', '#ffa502', '#2ed573']),
            connector={"line": {"color": "#667eea", "dash": "dot", "width": 3}}
        ))
        
        fig_severity.update_layout(
            height=350,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed alerts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Top 10 Critical Districts - Radar View")
        
        top_critical = data.nlargest(10, 'anomaly_score')
        
        fig_radar = go.Figure()
        
        for idx, row in top_critical.head(5).iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row['anomaly_score'], row.get('youth_ratio', 50), 
                   100 - row.get('compliance_rate', 50) if 'compliance_rate' in row else 50],
                theta=['Risk Score', 'Youth Ratio', 'Non-Compliance'],
                fill='toself',
                name=row['district'][:15]
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            height=400,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("#### 📍 Alert Distribution by State")
        
        state_alerts = data[data['risk_level'].isin(['CRITICAL', 'HIGH'])].groupby(['state', 'risk_level']).size().reset_index(name='count')
        
        fig_state_alert = px.bar(
            state_alerts.nlargest(20, 'count'),
            x='count',
            y='state',
            color='risk_level',
            orientation='h',
            color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502'},
            barmode='stack',
            height=400
        )
        
        fig_state_alert.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=10, r=40),
            xaxis_title="Alert Count",
            yaxis_title="",
            legend_title="Alert Level",
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_state_alert, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🚨 Critical Alert Details")
    
    # Detailed expandable alerts
    critical_list = data[data['risk_level'] == 'CRITICAL'].head(10)
    
    if len(critical_list) > 0:
        for idx, row in critical_list.iterrows():
            # Use simple boolean check instead of numpy bool
            is_first = (idx == critical_list.index[0])
            with st.expander(f"🔴 {row['district']}, {row['state']} - Risk Score: {row['anomaly_score']:.0f}", expanded=bool(is_first)):
                # Visual indicator bar
                risk_pct = min(row['anomaly_score'], 100)
                st.markdown(f"""
                <div style='background: linear-gradient(90deg, #ff4757 0%, #ff4757 {risk_pct}%, #e0e0e0 {risk_pct}%, #e0e0e0 100%); 
                            height: 8px; border-radius: 4px; margin-bottom: 15px;'></div>
                """, unsafe_allow_html=True)
                
                if files_count >= 2:
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📊 Demo Updates", f"{int(row.get('demo_total', 0)):,}")
                    c2.metric("🔐 Bio Updates", f"{int(row.get('bio_total', 0)):,}")
                    c3.metric("✅ Compliance", f"{row.get('compliance_rate', 0):.1f}%")
                    c4.metric("⚠️ Gap", f"{int(row.get('gap', 0)):,}")
                    
                    st.markdown("---")
                    st.markdown("**🎯 Recommended Actions:**")
                    
                    actions = []
                    if row.get('gap', 0) > 5000:
                        actions.append(f"🚨 **URGENT**: Deploy mobile biometric units - {int(row['gap']):,} pending verifications")
                    if row.get('compliance_rate', 100) < 50:
                        actions.append("📢 Launch immediate biometric awareness campaign")
                    if row.get('compliance_rate', 100) < 80:
                        actions.append("🎓 Conduct compliance training for local staff")
                    if row.get('migration_index', 0) > 2:
                        actions.append("🔍 Investigate high address change frequency patterns")
                    
                    for action in actions:
                        st.markdown(f"- {action}")
                    
                    if not actions:
                        st.markdown("- 📋 Monitor situation and maintain current protocols")
                    
                else:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("📈 Total Updates", f"{int(row.get('total_updates', 0)):,}")
                    c2.metric("👥 Youth Ratio", f"{row.get('youth_ratio', 0):.1f}%")
                    c3.metric("📝 Records", f"{int(row.get('record_count', 0)):,}")
                    
                    st.markdown("---")
                    st.markdown("**📋 Observations:**")
                    
                    if row.get('youth_ratio', 50) > 70:
                        st.markdown("- 👶 Unusually high youth enrollment detected (possible migration hub)")
                    if row.get('record_count', 0) > 100:
                        st.markdown("- 📊 High transaction frequency - requires monitoring")
                    if row.get('total_updates', 0) > 10000:
                        st.markdown("- ⚡ Exceptional activity volume - verify legitimacy")
    else:
        # Check for HIGH risk districts
        high_districts = data[data['risk_level'] == 'HIGH']
        
        if len(high_districts) > 0:
            st.warning(f"⚠️ No CRITICAL alerts, but {len(high_districts)} districts are at HIGH risk. Monitor closely.")
            
            # Show top 5 HIGH risk districts
            st.markdown("#### Top HIGH Risk Districts:")
            for idx, row in high_districts.head(5).iterrows():
                st.markdown(f"""
                <div style='background: rgba(255,165,2,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #ffa502;'>
                    <b style='color: #1a1a1a;'>{row['district']}, {row['state']}</b><br>
                    <span style='color: #ffa502; font-weight: 600;'>Risk Score: {row['anomaly_score']:.0f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No critical or high-risk alerts at this time. All districts operating within normal parameters.")
    
    # Export section
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**📥 Export Options**")
    
    with col2:
        csv = data.to_csv(index=False)
        st.download_button(
            "📄 Full Report (CSV)", 
            csv, 
            f"sentinel_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", 
            "text/csv", 
            use_container_width=True
        )
    
    with col3:
        critical_csv = data[data['risk_level'] == 'CRITICAL'].to_csv(index=False)
        st.download_button(
            "🚨 Critical Only", 
            critical_csv, 
            f"sentinel_critical_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", 
            "text/csv", 
            use_container_width=True
        )