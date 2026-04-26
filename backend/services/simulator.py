import random
import uuid
import re
from datetime import datetime
from typing import List, Dict, Any

class DeceptionSimulator:
    """Advanced Query-Aware simulation engine for high-fidelity deception."""

    def _generate_user(self, force_role: str = None) -> Dict[str, Any]:
        roles = ["admin", "user", "guest", "developer", "superuser"]
        role = force_role if force_role else random.choice(roles)
        username = f"{role}_{random.randint(10, 99)}"
        
        return {
            "id": random.randint(100, 999),
            "username": username,
            "email": f"{username}@company.internal",
            "role": role,
            "password_hash": f"$2b$12${uuid.uuid4().hex[:30]}",
            "last_login": datetime.utcnow().isoformat(),
            "status": "active"
        }

    def _generate_config(self) -> Dict[str, Any]:
        services = ["AWS_SECRET_KEY", "OPENAI_API_KEY", "STRIPE_SK", "DB_PASSWORD"]
        key_name = random.choice(services)
        return {
            "id": random.randint(1, 50),
            "config_name": key_name,
            "config_value": f"sk_live_{uuid.uuid4().hex}",
            "created_at": datetime.utcnow().isoformat()
        }

    def simulate_query(self, query: str) -> Dict[str, Any]:
        query_upper = query.upper()
        print(f"[ATTACK] SQL Query Detected: {query}")

        # 1. Handle DROP / DELETE / UPDATE (Modifying queries)
        if any(kw in query_upper for kw in ["DROP", "DELETE", "TRUNCATE", "UPDATE"]):
            return {
                "status": "success",
                "message": "Query executed successfully. Rows affected: 1",
                "data": [],
                "query_executed": query
            }

        # 2. Context Detection
        data = []
        
        # Detect Config/Secrets
        if any(kw in query_upper for kw in ["CONFIG", "API_KEY", "SECRET", "VAULT"]):
            data = [self._generate_config() for _ in range(random.randint(2, 4))]
        
        # Detect User Data
        else:
            # Parse Role Filter (e.g., role='admin')
            role_match = re.search(r"ROLE\s*=\s*'(\w+)'", query_upper)
            requested_role = role_match.group(1).lower() if role_match else None
            
            data = [self._generate_user(force_role=requested_role) for _ in range(random.randint(2, 5))]

        # 3. Column Filtering (SELECT col1, col2 FROM ...)
        # Simple regex to extract columns between SELECT and FROM
        column_match = re.search(r"SELECT\s+(.*?)\s+FROM", query_upper)
        if column_match and "*" not in column_match.group(1):
            requested_cols = [c.strip().lower() for c in column_match.group(1).split(",")]
            
            # Filter each record to only include requested columns
            filtered_data = []
            for record in data:
                filtered_record = {k: v for k, v in record.items() if k in requested_cols}
                # If the filter left nothing (e.g. invalid columns), keep original to avoid suspicion
                filtered_data.append(filtered_record if filtered_record else record)
            data = filtered_data

        return {
            "status": "success",
            "data": data,
            "query_executed": query,
            "execution_time": f"{random.uniform(0.001, 0.005):.4f}s"
        }
