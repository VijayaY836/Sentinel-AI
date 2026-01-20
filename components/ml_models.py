"""
SENTINEL AI - Machine Learning Models
======================================
Ensemble ML models for advanced anomaly detection.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


def train_ml_models(data, files_count):
    """Train ensemble of ML models for advanced anomaly detection"""
    
    # Prepare features
    if files_count >= 2:
        feature_cols = ['enrol_total', 'demo_total', 'bio_total', 'gap_abs', 'compliance_rate', 'migration_index']
    else:
        feature_cols = ['total_updates', 'youth_updates', 'adult_updates', 'record_count', 'youth_ratio']
    
    # Filter available columns
    available_features = [col for col in feature_cols if col in data.columns]
    X = data[available_features].fillna(0)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=available_features)
    
    results = {}
    
    # Model 1: Isolation Forest (Unsupervised Anomaly Detection)
    iso_forest = IsolationForest(
        contamination=0.15,
        random_state=42,
        n_estimators=100
    )
    data['ml_anomaly_score'] = iso_forest.fit_predict(X_scaled)
    data['ml_anomaly_confidence'] = -iso_forest.score_samples(X_scaled)
    
    # Normalize confidence to 0-100
    min_conf = data['ml_anomaly_confidence'].min()
    max_conf = data['ml_anomaly_confidence'].max()
    data['ml_confidence'] = ((data['ml_anomaly_confidence'] - min_conf) / (max_conf - min_conf) * 100)
    
    results['isolation_forest'] = {
        'model': iso_forest,
        'anomalies_detected': len(data[data['ml_anomaly_score'] == -1]),
        'total_samples': len(data)
    }
    
    # Model 2: Random Forest Classifier
    label_map = {'NORMAL': 0, 'HIGH': 1, 'CRITICAL': 2}
    y = data['risk_level'].map(label_map)
    
    if len(X) > 10:
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        rf_classifier.fit(X_train, y_train)
        
        rf_probs = rf_classifier.predict_proba(X_scaled)
        n_classes = rf_probs.shape[1]
        classes = rf_classifier.classes_
        
        data['ml_critical_probability'] = 0.0
        
        if 2 in classes:
            critical_idx = list(classes).index(2)
            data['ml_critical_probability'] = rf_probs[:, critical_idx] * 100
        elif n_classes > 1:
            data['ml_critical_probability'] = rf_probs[:, -1] * 100
        
        feature_importance = pd.DataFrame({
            'feature': available_features,
            'importance': rf_classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        results['random_forest'] = {
            'model': rf_classifier,
            'accuracy': rf_classifier.score(X_test, y_test),
            'feature_importance': feature_importance,
            'n_classes': n_classes
        }
    
    # Model 3: Gradient Boosting
    y_risk = data['anomaly_score']
    
    if len(X) > 10:
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_risk, test_size=0.2, random_state=42)
        
        gb_regressor = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        gb_regressor.fit(X_train, y_train)
        
        data['ml_predicted_risk'] = gb_regressor.predict(X_scaled)
        
        results['gradient_boosting'] = {
            'model': gb_regressor,
            'r2_score': gb_regressor.score(X_test, y_test),
            'mean_error': np.mean(np.abs(y_test - gb_regressor.predict(X_test)))
        }
    
    # Ensemble score
    if 'ml_confidence' in data.columns and 'ml_critical_probability' in data.columns:
        data['ml_ensemble_score'] = (
            data['ml_confidence'] * 0.4 +
            data['ml_critical_probability'] * 0.4 +
            (data['ml_predicted_risk'] if 'ml_predicted_risk' in data.columns else data['anomaly_score']) * 0.2
        )
    
    # ML-enhanced risk level
    if 'ml_ensemble_score' in data.columns:
        data['ml_risk_level'] = pd.cut(
            data['ml_ensemble_score'],
            bins=[0, 30, 60, 100],
            labels=['NORMAL', 'HIGH', 'CRITICAL']
        )
    
    return data, results