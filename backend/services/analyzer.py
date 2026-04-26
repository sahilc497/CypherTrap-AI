import re
import time
from typing import Dict, Any, List

# Try to import ML libraries, but provide fallback if environment is broken
try:
    import numpy as np
    from sklearn.ensemble import IsolationForest
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("WARNING: ML libraries (numpy/sklearn) not found. Using regex fallback for threat analysis.")

class ThreatAnalyzer:
    def __init__(self):
        # Configuration
        self.sql_keywords = ["SELECT", "FROM", "WHERE", "UNION", "JOIN", "DROP", "DELETE", "UPDATE", "INSERT", "AND", "OR", "GROUP", "BY", "ORDER", "LIMIT"]
        self.sensitive_keywords = ["PASSWORD", "ADMIN", "CONFIG", "SECRET", "TOKEN", "CREDENTIAL", "PRIVATE", "KEY", "ROOT"]
        
        # Initialize ML model
        self.model = None
        self.is_trained = False
        if ML_AVAILABLE:
            try:
                self.model = IsolationForest(contamination=0.05, random_state=42)
                self._train_baseline()
            except Exception as e:
                print(f"ML Init Error: {e}")
                self.model = None

    def _train_baseline(self):
        """Train the model on synthetic 'normal' queries to establish a baseline."""
        if not ML_AVAILABLE or self.model is None:
            return
            
        # Synthetic "Normal" Queries features
        # [len, kw_count, sensitive_count, special_chars, entropy]
        normal_data = []
        for _ in range(200):
            length = np.random.randint(15, 60)
            kw_count = np.random.randint(1, 4)
            sensitive_count = 0
            special_chars = np.random.randint(0, 5)
            entropy = np.random.uniform(3.0, 4.5)
            normal_data.append([length, kw_count, sensitive_count, special_chars, entropy])
            
        self.model.fit(np.array(normal_data))
        self.is_trained = True

    def extract_features(self, query: str) -> List[float]:
        """Extract numerical features from a SQL query."""
        q = query.upper()
        
        length = len(query)
        kw_count = sum(1 for kw in self.sql_keywords if kw in q)
        sensitive_count = sum(1 for sk in self.sensitive_keywords if sk in q)
        special_chars = sum(1 for char in query if char in ["'", "\"", ";", "--", "*", "=", "(", ")", "<", ">", "+"])
        
        # Calculate character entropy (simplicity vs obfuscation)
        char_counts = {}
        for char in query:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        import math
        entropy = 0
        for count in char_counts.values():
            p = count / len(query)
            entropy -= p * math.log2(p)
            
        return [float(length), float(kw_count), float(sensitive_count), float(special_chars), float(entropy)]

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query using Isolation Forest and return a threat intelligence report.
        """
        features = self.extract_features(query)
        
        if ML_AVAILABLE and self.is_trained:
            # Predict anomaly (-1 is anomaly, 1 is normal)
            X = np.array(features).reshape(1, -1)
            raw_score = self.model.decision_function(X)[0]
            
            # Map raw_score to 0-100 threat_score
            # raw_score is typically between -0.5 and 0.5
            # Negative = More Anomaly. We want to be more sensitive.
            threat_score = np.clip((0.15 - raw_score) * 180, 0, 100)
            
            # Boost score for high-risk manual features
            if features[2] > 0: threat_score += 20 # Sensitive keywords
            if features[3] > 5: threat_score += 15 # Many special chars
            
            threat_score = min(threat_score, 100)
            confidence = np.clip(0.6 + abs(raw_score), 0, 0.99)
        else:
            # Fallback heuristic
            threat_score = min((features[2] * 30) + (features[3] * 10) + (features[1] * 5), 100)
            confidence = 0.6

        # Determine level
        if threat_score < 30:
            level = "Low"
        elif threat_score < 70:
            level = "Medium"
        else:
            level = "High"
            
        return {
            "threat_score": round(float(threat_score), 2),
            "threat_level": level,
            "confidence": round(float(confidence), 2),
            "features": features
        }
