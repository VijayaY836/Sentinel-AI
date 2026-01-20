"""
Societal Insights Generator
===========================
Translates ML patterns into human-readable societal trends
"""

import streamlit as st


def generate_insights(data, files_count):
    """
    Generate policy-relevant insights from data patterns
    """
    insights = []
    
    # Youth ratio insights
    if 'youth_ratio' in data.columns:
        avg_youth = data['youth_ratio'].mean()
        high_youth_districts = data[data['youth_ratio'] > 70]
        
        if len(high_youth_districts) > 0:
            insights.append({
                'category': '👥 Demographic Trends',
                'finding': f"{len(high_youth_districts)} districts show youth-dominant enrollment patterns",
                'interpretation': "This correlates with education migration hubs, first-time enrollment drives, and urban-rural youth mobility. Suggests administrative capacity planning needed for youth-centric services.",
                'actionable': "Deploy mobile enrollment units near educational institutions during admission seasons."
            })
    
    # Compliance patterns
    if 'compliance_rate' in data.columns:
        low_compliance = data[data['compliance_rate'] < 50]
        
        if len(low_compliance) > 0:
            insights.append({
                'category': '📊 Update Completion Patterns',
                'finding': f"{len(low_compliance)} districts show incomplete biometric verification cycles",
                'interpretation': "Gap between demographic updates and biometric completion suggests: (1) Rural connectivity challenges, (2) Awareness gaps about biometric importance, (3) Seasonal agricultural labor migration preventing follow-up visits.",
                'actionable': "Schedule mobile biometric camps during agricultural off-seasons; partner with local banks/post offices for verification."
            })
    
    # Geographic concentration
    state_concentration = data.groupby('state')['district'].count().sort_values(ascending=False)
    top_state = state_concentration.index[0]
    
    insights.append({
        'category': '🗺️ Geographic Load Distribution',
        'finding': f"{top_state} shows highest administrative activity concentration",
        'interpretation': "High enrollment/update density indicates: (1) Population growth centers, (2) Migration destination states, (3) Improved digital infrastructure adoption. Administrative resources should scale proportionally.",
        'actionable': f"Increase permanent enrollment centers in {top_state}; analyze staffing ratios vs. population density."
    })
    
    # Volume patterns
    if 'total_updates' in data.columns:
        high_volume = data.nlargest(10, 'total_updates')
        total_volume = data['total_updates'].sum()
        
        insights.append({
            'category': '📈 Update Volume Trends',
            'finding': f"Top 10 districts account for {(high_volume['total_updates'].sum()/total_volume*100):.1f}% of total update activity",
            'interpretation': "Update concentration in specific districts suggests: (1) Urban migration destinations, (2) Job market hubs requiring address changes, (3) Marriage-related demographic updates in metros. Reflects India's urbanization patterns.",
            'actionable': "Establish express update kiosks in metro stations and commercial centers."
        })
    
    # ML-detected patterns
    if 'ml_confidence' in data.columns:
        unusual_patterns = data[data['ml_confidence'] > 75]
        
        if len(unusual_patterns) > 0:
            insights.append({
                'category': '🔍 Unusual Enrollment Dynamics',
                'finding': f"{len(unusual_patterns)} districts show atypical enrollment/update patterns",
                'interpretation': "Machine learning identified districts with non-standard patterns that may indicate: (1) Sudden policy changes (e.g., benefit scheme launches), (2) Mass migration events, (3) Localized awareness campaigns, (4) Administrative process improvements.",
                'actionable': "Conduct field studies to document success factors; replicate effective practices in similar demographics."
            })
    
    # Seasonal/timing patterns (if detectable)
    if 'record_count' in data.columns:
        high_frequency = data[data['record_count'] > data['record_count'].quantile(0.75)]
        
        insights.append({
            'category': '⏰ Transaction Frequency Patterns',
            'finding': f"{len(high_frequency)} districts show elevated transaction frequencies",
            'interpretation': "High-frequency updates suggest: (1) Regions with mobile populations (construction workers, seasonal laborers), (2) Areas with active benefit disbursement requiring updated details, (3) Border districts with cross-state movement.",
            'actionable': "Implement SMS-based update reminders for high-mobility populations; explore blockchain for permanent portability."
            })
    
    return insights


def render_insight_card(insight):
    """Render a single insight card"""
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 12px; 
                margin: 15px 0; border-left: 5px solid #667eea; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <h4 style='color: #667eea; margin: 0 0 10px 0;'>{insight['category']}</h4>
        <p style='margin: 8px 0; font-weight: 600; color: #2d2d2d;'>
            📌 <strong>Finding:</strong> {insight['finding']}
        </p>
        <p style='margin: 8px 0; color: #4a4a4a; line-height: 1.6;'>
            💡 <strong>Interpretation:</strong> {insight['interpretation']}
        </p>
        <p style='margin: 8px 0; padding: 10px; background: rgba(102,126,234,0.1); 
                   border-radius: 6px; color: #1a1a1a;'>
            ✅ <strong>Actionable:</strong> {insight['actionable']}
        </p>
    </div>
    """, unsafe_allow_html=True)


def add_disclaimer():
    """Add important disclaimer about analytical methods"""
    st.markdown("""
    <div style='background: rgba(255,243,205,0.3); padding: 15px; border-radius: 8px; 
                border-left: 4px solid #ffa502; margin: 20px 0;'>
        <p style='margin: 0; font-size: 0.9rem; color: #1a1a1a;'>
            <strong>ℹ️ Methodology Note:</strong> "System stress" and "unusual pattern" indicators are 
            analytical abstractions representing enrollment/update volume dynamics and demographic variations, 
            not citizen-level risk assessments. All insights are derived from aggregate statistical patterns 
            and machine learning analysis of publicly available Aadhaar enrollment data.
        </p>
    </div>
    """, unsafe_allow_html=True)
