"""
SENTINEL AI - Data Processing Utilities
========================================
Functions for loading, cleaning, and analyzing Aadhaar datasets.
"""

import pandas as pd
import numpy as np


def load_and_clean(file):
    """Load and perform basic cleaning on CSV file"""
    if file is None:
        return None
    df = pd.read_csv(file)
    df.columns = [c.strip().lower().replace('_', ' ') for c in df.columns]
    
    for col in ['state', 'district']:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    
    return df


def analyze_single_dataset(df, dtype):
    """Analyze patterns in a single dataset"""
    if 'district' not in df.columns:
        return None
    
    results = []
    grouped = df.groupby('district')
    
    for district, group in grouped:
        state = group.iloc[0].get('state', 'Unknown') if 'state' in group.columns else 'Unknown'
        
        ignore_cols = ['date', 'state', 'district', 'pincode']
        total = 0
        youth_total = 0
        adult_total = 0
        
        for col in group.columns:
            if col.lower() in ignore_cols:
                continue
            try:
                col_sum = pd.to_numeric(group[col], errors='coerce').sum()
                if not pd.isna(col_sum):
                    total += col_sum
                    if '5' in col or '17' in col:
                        youth_total += col_sum
                    elif '18' in col or 'greater' in col.lower():
                        adult_total += col_sum
            except:
                continue
        
        record_count = len(group)
        avg_per_record = total / record_count if record_count > 0 else 0
        youth_ratio = (youth_total / total * 100) if total > 0 else 0
        
        volume_score = min(total / 10000, 40)
        demographic_score = 20 if youth_ratio > 60 or youth_ratio < 20 else 0
        frequency_score = 30 if record_count > 100 else (15 if record_count > 50 else 0)
        
        anomaly_score = volume_score + demographic_score + frequency_score
        risk_level = 'CRITICAL' if anomaly_score > 60 else ('HIGH' if anomaly_score > 30 else 'NORMAL')
        
        results.append({
            'district': district,
            'state': state,
            'total_updates': total,
            'youth_updates': youth_total,
            'adult_updates': adult_total,
            'record_count': record_count,
            'avg_per_record': avg_per_record,
            'youth_ratio': youth_ratio,
            'anomaly_score': anomaly_score,
            'risk_level': risk_level,
            'dataset_type': dtype
        })
    
    return pd.DataFrame(results).sort_values('anomaly_score', ascending=False)


def analyze_multiple_datasets(enrol_df, demo_df, bio_df):
    """Compare multiple datasets"""
    district_map = {}
    
    datasets = [
        (enrol_df, 'enrol'),
        (demo_df, 'demo'),
        (bio_df, 'bio')
    ]
    
    for df, dtype in datasets:
        if df is None:
            continue
        
        if 'district' not in df.columns:
            continue
            
        grouped = df.groupby('district')
        
        for district, group in grouped:
            if district not in district_map:
                state = group.iloc[0].get('state', 'Unknown') if 'state' in group.columns else 'Unknown'
                district_map[district] = {
                    'district': district,
                    'state': state,
                    'enrol_total': 0,
                    'demo_total': 0,
                    'bio_total': 0
                }
            
            ignore_cols = ['date', 'state', 'district', 'pincode']
            for col in group.columns:
                if col.lower() in ignore_cols:
                    continue
                
                try:
                    col_sum = pd.to_numeric(group[col], errors='coerce').sum()
                    if not pd.isna(col_sum):
                        if dtype == 'enrol':
                            district_map[district]['enrol_total'] += col_sum
                        elif dtype == 'demo':
                            district_map[district]['demo_total'] += col_sum
                        elif dtype == 'bio':
                            district_map[district]['bio_total'] += col_sum
                except:
                    continue
    
    results = []
    for district, data in district_map.items():
        gap = data['demo_total'] - data['bio_total']
        compliance_rate = (data['bio_total'] / data['demo_total'] * 100) if data['demo_total'] > 0 else 100
        migration_index = (data['demo_total'] / data['enrol_total']) if data['enrol_total'] > 0 else 0
        
        anomaly_score = 0
        if gap > 0:
            anomaly_score += min(gap / 1000, 50)
        if compliance_rate < 50:
            anomaly_score += 30
        elif compliance_rate < 80:
            anomaly_score += 15
        if migration_index > 2:
            anomaly_score += 20
        
        risk_level = 'CRITICAL' if anomaly_score > 60 else ('HIGH' if anomaly_score > 30 else 'NORMAL')
        
        results.append({
            'district': district,
            'state': data['state'],
            'enrol_total': data['enrol_total'],
            'demo_total': data['demo_total'],
            'bio_total': data['bio_total'],
            'gap': gap,
            'gap_abs': abs(gap),
            'compliance_rate': compliance_rate,
            'migration_index': migration_index,
            'anomaly_score': anomaly_score,
            'risk_level': risk_level
        })
    
    return pd.DataFrame(results).sort_values('anomaly_score', ascending=False)