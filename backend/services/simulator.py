import re
import random
import uuid
import time
from typing import List, Dict, Any

class DeceptionSimulator:
    def __init__(self):
        self.common_domains = ["company.internal", "dev.internal", "vault.internal"]
        self.roles = ["admin", "user", "guest", "db_admin", "security_audit"]

    def _generate_user(self, role_filter: str = None) -> Dict[str, Any]:
        """Generate a realistic fake user as requested."""
        role = role_filter if role_filter else random.choice(self.roles)
        username = f"user_{random.randint(100, 999)}"
        return {
            "id": random.randint(1, 10000),
            "username": username,
            "email": f"{username}@{random.choice(self.common_domains)}",
            "role": role,
            "last_login": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - random.randint(0, 864000))),
        }

    def _generate_passwords(self, count: int = 3) -> List[Dict[str, str]]:
        """Generate bcrypt-like hashes."""
        return [
            {
                "username": f"admin_{i}",
                "password_hash": f"$2b$12${uuid.uuid4().hex[:31]}"
            } for i in range(1, count + 1)
        ]

    def _generate_schema(self) -> List[Dict[str, str]]:
        """Generate realistic schema information."""
        return [
            {"column_name": "id", "data_type": "integer"},
            {"column_name": "username", "data_type": "varchar"},
            {"column_name": "email", "data_type": "varchar"},
            {"column_name": "password_hash", "data_type": "text"},
            {"column_name": "role", "data_type": "varchar"},
            {"column_name": "created_at", "data_type": "timestamp"}
        ]

    def _generate_config(self) -> Dict[str, str]:
        """Generate fake system configuration and secrets."""
        return {
            "AWS_SECRET_KEY": f"AKIA{uuid.uuid4().hex[:16].upper()}",
            "OPENAI_API_KEY": f"sk-{uuid.uuid4().hex[:48]}",
            "DATABASE_URL": "postgresql://prod_user:hidden_pass@db.company.internal:5432/main",
            "REDIS_PASSWORD": uuid.uuid4().hex[:16]
        }

    def simulate_query(self, query: str) -> Dict[str, Any]:
        """
        Query-Aware Deception Engine.
        Returns realistic fake data based on query intent.
        """
        query_upper = query.upper()
        
        # 1. Schema Recon (information_schema)
        if any(kw in query_upper for kw in ["INFORMATION_SCHEMA", "COLUMNS", "TABLES"]):
            data = self._generate_schema()
            return self._build_response(data, query)

        # 2. Destructive Queries (DROP / DELETE / TRUNCATE)
        if any(kw in query_upper for kw in ["DROP", "DELETE", "TRUNCATE"]):
            return {
                "status": "success",
                "message": "Query executed successfully",
                "rows_affected": random.randint(1, 50),
                "execution_time": f"{round(random.uniform(0.001, 0.2), 4)}s"
            }

        # 3. Credential Harvesting
        if "PASSWORD" in query_upper or "HASH" in query_upper:
            data = self._generate_passwords(random.randint(2, 5))
            return self._build_response(data, query)

        # 4. Config / Secrets
        if any(kw in query_upper for kw in ["API_KEY", "CONFIG", "SECRET"]):
            data = [self._generate_config()]
            return self._build_response(data, query)

        # 5. User Data Queries
        if "FROM USERS" in query_upper:
            # Detect Role Filter
            role_match = re.search(r"ROLE\s*=\s*'(\w+)'", query_upper)
            target_role = role_match.group(1).lower() if role_match else None
            
            count = random.randint(2, 5)
            data = [self._generate_user(target_role) for _ in range(count)]
            
            # Detect Requested Columns
            columns_match = re.search(r"SELECT\s+(.+?)\s+FROM", query_upper)
            if columns_match:
                cols_str = columns_match.group(1).replace(" ", "")
                if cols_str != "*":
                    requested_columns = [c.strip().lower() for c in cols_str.split(",")]
                    data = [{k: v for k, v in row.items() if k in requested_columns} for row in data]
            
            return self._build_response(data, query)

        # Fallback realistic data
        data = [{"id": i, "name": f"system_node_{i}", "status": "online"} for i in range(1, 4)]
        return self._build_response(data, query)

    def _build_response(self, data: Any, query: str) -> Dict[str, Any]:
        """Helper to build consistent success response."""
        return {
            "status": "success",
            "data": data,
            "query_executed": query,
            "execution_time": f"{round(random.uniform(0.001, 0.2), 4)}s"
        }
