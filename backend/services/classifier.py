import re
from typing import Dict, Any, List

class AttackClassifier:
    """
    Hybrid Rule + ML classification system for security events.
    """
    def __init__(self):
        self.patterns = {
            "Destructive Attack": [
                r"DROP\s+TABLE",
                r"DROP\s+DATABASE",
                r"TRUNCATE\s+",
                r"DELETE\s+FROM",
                r"ALTER\s+TABLE",
                r"UPDATE\s+.*SET"
            ],
            "SQL Injection": [
                r"UNION\s+SELECT",
                r"OR\s+1=1",
                r"'\s+OR\s+'",
                r"SLEEP\(",
                r"BENCHMARK\(",
                r"CASE\s+WHEN",
                r"--\s*$"
            ],
            "Reconnaissance": [
                r"INFORMATION_SCHEMA",
                r"PG_CATALOG",
                r"VERSION\(",
                r"USER\(",
                r"DATABASE\(",
                r"SHOW\s+TABLES",
                r"DESCRIBE\s+"
            ],
            "Credential Harvesting": [
                r"PASSWORD",
                r"SECRET",
                r"TOKEN",
                r"API_KEY",
                r"CREDENTIALS",
                r"AUTH_KEY",
                r"ACCESS_KEY"
            ]
        }

    def classify(self, query: str, threat_score: float) -> str:
        """
        Determine the attack type based on patterns and ML threat score.
        """
        query_upper = query.upper()
        
        # 1. Check for specific dangerous patterns
        for attack_type, pattern_list in self.patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query_upper):
                    return attack_type
        
        # 2. Heuristic fallback based on threat score
        if threat_score > 70:
            return "Advanced Persistent Threat (APT)"
        elif threat_score > 30:
            return "Anomalous Behavioral Pattern"
        
        return "Normal Traffic"

    def get_insight(self, attack_type: str, threat_score: float) -> str:
        """
        Generate a human-readable security insight.
        """
        insights = {
            "SQL Injection": "Attacker is attempting to bypass authentication or extract data via blind/union injection.",
            "Reconnaissance": "Suspicious metadata scanning detected. Attacker is mapping the database schema.",
            "Credential Harvesting": "Targeted attempt to locate administrative or system credentials detected.",
            "Destructive Attack": "Unauthorized attempt to modify or delete core system structures.",
            "Advanced Persistent Threat (APT)": "Highly irregular query pattern detected. Potential targeted attack.",
            "Anomalous Behavioral Pattern": "Suspicious interaction detected. Increasing deception depth.",
            "Normal Traffic": "Request aligns with typical user behavior."
        }
        
        return insights.get(attack_type, "Unknown activity detected.")
