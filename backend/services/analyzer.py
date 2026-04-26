import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from backend.database.config import SessionLocal
from backend.models.threat import AttackLog, SessionTrace
import logging

logger = logging.getLogger("ThreatAnalyzer")

class ThreatAnalyzer:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False

    def _get_features(self, db):
        """Extract features from database logs for ML model."""
        logs = db.query(AttackLog).all()
        if len(logs) < 10: # Need minimum data to train
            return None
        
        data = []
        for log in logs:
            # Simple features: path length, method (encoded), duration
            data.append({
                "path_len": len(log.path),
                "method_val": 1 if log.method == "POST" else 0,
                "duration": log.duration or 0.1
            })
        
        return pd.DataFrame(data)

    def train_model(self):
        """Train the Isolation Forest model on historical data."""
        db = SessionLocal()
        try:
            df = self._get_features(db)
            if df is not None:
                self.model.fit(df)
                self.is_trained = True
                logger.info("ML Model trained successfully on historical logs.")
            else:
                logger.info("Not enough data to train ML model yet.")
        finally:
            db.close()

    async def calculate_threat_score(self, ip: str, path: str, method: str, duration: float):
        """Calculate a threat score (0-100) using ML and rules."""
        score = 0
        
        # 1. Rule-based scoring (Static signals)
        if "/admin" in path: score += 30
        if "/db" in path: score += 40
        if method == "POST": score += 10
        
        # 2. ML Anomaly Detection (Dynamic signals)
        if self.is_trained:
            features = pd.DataFrame([{
                "path_len": len(path),
                "method_val": 1 if method == "POST" else 0,
                "duration": duration
            }])
            # Isolation Forest returns -1 for anomalies, 1 for normal
            prediction = self.model.predict(features)[0]
            if prediction == -1:
                score += 20 # Add anomaly bonus
        
        # Cap at 100
        final_score = min(score, 100)
        
        threat_level = "Low"
        if final_score > 75: threat_level = "High"
        elif final_score > 40: threat_level = "Medium"
        
        return final_score, threat_level
