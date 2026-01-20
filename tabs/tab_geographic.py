"""
SENTINEL AI - Geographic Tab
=============================
Geographic intelligence analysis and state-level visualizations.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_geographic_tab(data, files_count):
    """Render the Geographic Intelligence tab content"""
    st.markdown("### 🗺️ Geographic Intelligence Analysis")
    
    state_summary = data.groupby('state').agg({
        'anomaly_score': 'mean',
        'district': 'count'
    }).reset_index()
    state_summary.columns = ['State', 'Avg Risk Score', 'District Count']
    
    # Top row - Main geographic visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Treemap showing states sized by district count, colored by risk
        fig_tree = px.treemap(
            data,
            path=['state', 'district'],
            values='anomaly_score',
            color='anomaly_score',
            color_continuous_scale='RdYlGn_r',
            title='Risk Hierarchy: States → Districts',
            height=450
        )
        fig_tree.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=10, l=10, r=10)
        )
        fig_tree.update_traces(textposition='middle center', textfont_size=11)
        st.plotly_chart(fig_tree, use_container_width=True)
    
    with col2:
        # Sunburst chart for hierarchical view
        fig_sun = px.sunburst(
            data.head(50),
            path=['risk_level', 'state', 'district'],
            values='anomaly_score',
            color='anomaly_score',
            color_continuous_scale='Reds',
            title='Hierarchical Risk View',
            height=450
        )
        fig_sun.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_sun, use_container_width=True)
    
    st.markdown("---")
    
    # Second row - Detailed state analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced state risk bar chart with gradient
        fig_state = go.Figure()
        top_states = state_summary.sort_values('Avg Risk Score', ascending=False).head(15)
        
        fig_state.add_trace(go.Bar(
            x=top_states['Avg Risk Score'],
            y=top_states['State'],
            orientation='h',
            marker=dict(
                color=top_states['Avg Risk Score'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Risk Score")
            ),
            text=top_states['Avg Risk Score'].round(1),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Risk Score: %{x:.1f}<extra></extra>'
        ))
        
        fig_state.update_layout(
            title='Top 15 States by Average Risk Score',
            height=450,
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=40, l=10, r=40),
            xaxis_title="Average Risk Score",
            yaxis_title="",
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_state, use_container_width=True)
    
    with col2:
        # Scatter plot: District count vs Risk score
        fig_scatter_state = px.scatter(
            state_summary,
            x='District Count',
            y='Avg Risk Score',
            size='District Count',
            color='Avg Risk Score',
            text='State',
            color_continuous_scale='RdYlGn_r',
            title='State Risk vs District Density',
            height=450
        )
        fig_scatter_state.update_traces(
            textposition='top center',
            textfont_size=9
        )
        fig_scatter_state.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=40, l=40, r=40)
        )
        st.plotly_chart(fig_scatter_state, use_container_width=True)
    
    st.markdown("---")
    
    # Third row - Additional insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Districts per state bubble chart
        top_district_states = state_summary.nlargest(10, 'District Count')
        fig_bubble = px.scatter(
            top_district_states,
            x='State',
            y='District Count',
            size='District Count',
            color='Avg Risk Score',
            color_continuous_scale='Reds',
            title='Top 10 States by Districts',
            height=300
        )
        fig_bubble.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=10),
            xaxis={'tickangle': 45}
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    with col2:
        # Risk level distribution by top states
        top_5_states = state_summary.nlargest(5, 'Avg Risk Score')['State'].tolist()
        risk_state_data = data[data['state'].isin(top_5_states)]
        
        fig_risk_dist = px.histogram(
            risk_state_data,
            x='state',
            color='risk_level',
            title='Risk Distribution - Top 5 States',
            color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
            barmode='group',
            height=300
        )
        fig_risk_dist.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=40, l=40, r=10),
            xaxis={'tickangle': 45},
            xaxis_title="State",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_risk_dist, use_container_width=True)
    
    with col3:
        # State statistics table
        st.markdown("#### 📊 State Statistics")
        stats_df = state_summary.nlargest(10, 'Avg Risk Score')[['State', 'Avg Risk Score', 'District Count']]
        stats_df['Avg Risk Score'] = stats_df['Avg Risk Score'].round(1)
        
        st.dataframe(
            stats_df,
            hide_index=True,
            use_container_width=True,
            height=280
        )