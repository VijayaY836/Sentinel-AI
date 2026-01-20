"""
SENTINEL AI - AI Models Tab
============================
ML model performance, feature importance, and predictions analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_ai_models_tab(data, ml_results):
    """Render the AI Models tab content"""
    st.markdown("### 🤖 AI-Powered Intelligence Models")
    
    if ml_results:
        # Model Overview Cards
        st.markdown("#### 🧠 Multi-Model Ensemble Architecture")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='metric-card' style='border-left: 4px solid #667eea;'>
                <h4 style='color: #667eea; margin-bottom: 10px;'>🔍 Isolation Forest</h4>
                <p style='font-size: 0.9rem; line-height: 1.6;'>
                    <b>Type:</b> Unsupervised Learning<br>
                    <b>Purpose:</b> Anomaly Detection<br>
                    <b>Method:</b> Isolates outliers in high-dimensional space<br>
                    <b>Strength:</b> Finds unknown fraud patterns
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card' style='border-left: 4px solid #2ed573;'>
                <h4 style='color: #2ed573; margin-bottom: 10px;'>🎯 Random Forest</h4>
                <p style='font-size: 0.9rem; line-height: 1.6;'>
                    <b>Type:</b> Supervised Classification<br>
                    <b>Purpose:</b> Risk Level Prediction<br>
                    <b>Method:</b> Ensemble of decision trees<br>
                    <b>Strength:</b> High accuracy, interpretable
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card' style='border-left: 4px solid #ffa502;'>
                <h4 style='color: #ffa502; margin-bottom: 10px;'>📈 Gradient Boosting</h4>
                <p style='font-size: 0.9rem; line-height: 1.6;'>
                    <b>Type:</b> Supervised Regression<br>
                    <b>Purpose:</b> Risk Score Forecasting<br>
                    <b>Method:</b> Sequential error correction<br>
                    <b>Strength:</b> Precise numerical predictions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feature Importance Analysis
        if 'random_forest' in ml_results:
            st.markdown("#### 🎯 Feature Importance Analysis")
            st.markdown("*Understanding which factors drive risk predictions*")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                feat_imp = ml_results['random_forest']['feature_importance']
                
                fig_importance = go.Figure(go.Bar(
                    x=feat_imp['importance'],
                    y=feat_imp['feature'],
                    orientation='h',
                    marker=dict(
                        color=feat_imp['importance'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Importance")
                    ),
                    text=feat_imp['importance'].round(3),
                    textposition='outside'
                ))
                
                fig_importance.update_layout(
                    title='Random Forest Feature Importance',
                    height=400,
                    template='plotly_white',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=40, l=150, r=40),
                    xaxis_title="Importance Score",
                    yaxis_title="",
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_importance, use_container_width=True)
            
            with col2:
                st.markdown("**📊 Key Insights:**")
                for idx, row in feat_imp.head(5).iterrows():
                    importance_pct = row['importance'] * 100
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.6); padding: 10px; border-radius: 6px; margin: 8px 0; border-left: 3px solid #667eea;'>
                        <b>{row['feature'].replace('_', ' ').title()}</b><br>
                        <span style='color: #667eea; font-size: 1.2rem; font-weight: 700;'>{importance_pct:.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ML vs Rule-based Comparison
        st.markdown("#### ⚖️ ML Predictions vs Rule-Based Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter: Rule-based vs ML
            if 'ml_ensemble_score' in data.columns:
                fig_comparison = px.scatter(
                    data.head(100),
                    x='anomaly_score',
                    y='ml_ensemble_score',
                    color='risk_level',
                    size='ml_confidence' if 'ml_confidence' in data.columns else None,
                    hover_name='district',
                    color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
                    title='Rule-Based vs AI Ensemble Score',
                    labels={'anomaly_score': 'Rule-Based Score', 'ml_ensemble_score': 'AI Ensemble Score'},
                    height=400
                )
                
                # Add diagonal line
                fig_comparison.add_trace(go.Scatter(
                    x=[0, 100],
                    y=[0, 100],
                    mode='lines',
                    name='Perfect Agreement',
                    line=dict(color='gray', dash='dash')
                ))
                
                fig_comparison.update_layout(
                    template='plotly_white',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=40, l=40, r=40)
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
        
        with col2:
            # Model agreement analysis
            if 'ml_risk_level' in data.columns:
                agreement = (data['risk_level'] == data['ml_risk_level']).sum() / len(data) * 100
                
                st.markdown(f"""
                <div class='metric-card' style='border-left: 4px solid #764ba2; text-align: center;'>
                    <div class='stat-label'>Model Agreement Rate</div>
                    <div class='big-stat' style='color: #764ba2; font-size: 3rem;'>{agreement:.1f}%</div>
                    <p style='font-size: 0.9rem; margin-top: 10px;'>
                        ML models agree with rule-based classification in {agreement:.0f}% of cases
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Confusion-style comparison
                comparison_data = []
                for rb_level in ['NORMAL', 'HIGH', 'CRITICAL']:
                    for ml_level in ['NORMAL', 'HIGH', 'CRITICAL']:
                        count = len(data[(data['risk_level'] == rb_level) & (data['ml_risk_level'] == ml_level)])
                        comparison_data.append({
                            'Rule-Based': rb_level,
                            'ML Model': ml_level,
                            'Count': count
                        })
                
                comp_df = pd.DataFrame(comparison_data)
                comp_pivot = comp_df.pivot(index='Rule-Based', columns='ML Model', values='Count')
                
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=comp_pivot.values,
                    x=comp_pivot.columns,
                    y=comp_pivot.index,
                    colorscale='Blues',
                    text=comp_pivot.values,
                    texttemplate='%{text}',
                    textfont={"size": 14},
                    colorbar=dict(title="Count")
                ))
                
                fig_heatmap.update_layout(
                    title='Classification Agreement Matrix',
                    height=280,
                    template='plotly_white',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=40, l=80, r=40),
                    xaxis_title="ML Model",
                    yaxis_title="Rule-Based"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("---")
        
        # ML Confidence Analysis
        st.markdown("#### 🎲 AI Confidence Distribution")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'ml_confidence' in data.columns:
                fig_conf = px.histogram(
                    data,
                    x='ml_confidence',
                    color='risk_level',
                    nbins=30,
                    title='Anomaly Detection Confidence',
                    color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
                    height=320
                )
                fig_conf.update_layout(
                    template='plotly_white',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=40, l=40, r=10),
                    xaxis_title="ML Confidence Score"
                )
                st.plotly_chart(fig_conf, use_container_width=True)
        
        with col2:
            if 'ml_critical_probability' in data.columns:
                fig_prob = px.box(
                    data,
                    x='risk_level',
                    y='ml_critical_probability',
                    color='risk_level',
                    title='Critical Risk Probability',
                    color_discrete_map={'CRITICAL': '#ff4757', 'HIGH': '#ffa502', 'NORMAL': '#2ed573'},
                    height=320
                )
                fig_prob.update_layout(
                    template='plotly_white',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=40, l=40, r=10),
                    yaxis_title="Probability (%)"
                )
                st.plotly_chart(fig_prob, use_container_width=True)
        
        with col3:
            if 'ml_predicted_risk' in data.columns:
                # Prediction accuracy
                actual = data['anomaly_score']
                predicted = data['ml_predicted_risk']
                
                fig_pred = go.Figure()
                fig_pred.add_trace(go.Scatter(
                    x=actual,
                    y=predicted,
                    mode='markers',
                    marker=dict(
                        size=5,
                        color=data['ml_confidence'] if 'ml_confidence' in data.columns else '#667eea',
                        colorscale='Viridis',
                        showscale=True
                    ),
                    name='Predictions'
                ))
                fig_pred.add_trace(go.Scatter(
                    x=[0, 100],
                    y=[0, 100],
                    mode='lines',
                    line=dict(color='red', dash='dash'),
                    name='Perfect Prediction'
                ))
                
                fig_pred.update_layout(
                    title='Prediction Accuracy',
                    height=320,
                    template='plotly_white',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=40, l=40, r=10),
                    xaxis_title="Actual Risk",
                    yaxis_title="Predicted Risk"
                )
                st.plotly_chart(fig_pred, use_container_width=True)
        
        st.markdown("---")
        
        # Top ML-identified anomalies
        st.markdown("#### 🚨 Top ML-Identified Anomalies")
        
        if 'ml_confidence' in data.columns:
            top_ml = data.nlargest(10, 'ml_confidence')
            
            fig_top_ml = go.Figure()
            
            fig_top_ml.add_trace(go.Bar(
                name='Rule-Based Score',
                x=top_ml['district'],
                y=top_ml['anomaly_score'],
                marker_color='#667eea'
            ))
            
            if 'ml_ensemble_score' in top_ml.columns:
                fig_top_ml.add_trace(go.Bar(
                    name='AI Ensemble Score',
                    x=top_ml['district'],
                    y=top_ml['ml_ensemble_score'],
                    marker_color='#ff4757'
                ))
            
            fig_top_ml.update_layout(
                title='Top 10 ML-Detected Anomalies: Score Comparison',
                height=400,
                barmode='group',
                template='plotly_white',
                plot_bgcolor='rgba(255,255,255,0.9)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=80, l=40, r=40),
                xaxis={'tickangle': 45},
                yaxis_title="Risk Score"
            )
            st.plotly_chart(fig_top_ml, use_container_width=True)
    
    else:
        st.info("ML models will be trained automatically when you analyze data. Upload datasets to see AI-powered insights!")