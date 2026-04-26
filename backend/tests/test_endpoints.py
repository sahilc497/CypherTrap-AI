import httpx
import asyncio

async def test_traps():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Test Root
        print("Testing Root...")
        resp = await client.get("/")
        print(f"Status: {resp.status_code}, Body: {resp.json()}")

        # Test Login Trap
        print("\nTesting Login Trap...")
        resp = await client.post("/login", json={"username": "admin", "password": "password123"})
        print(f"Status: {resp.status_code}, Body: {resp.json()}")

        # Test Admin Trap
        print("\nTesting Admin Trap...")
        resp = await client.get("/admin")
        print(f"Status: {resp.status_code}, Body: {resp.json()}")

        # Test DB Trap
        print("\nTesting DB Trap...")
        resp = await client.post("/db", json={"query": "SELECT * FROM users"})
        print(f"Status: {resp.status_code}, Body: {resp.json()}")

        # Test Config Trap
        print("\nTesting Config Trap...")
        resp = await client.get("/config")
        print(f"Status: {resp.status_code}, Body: {resp.json()}")

if __name__ == "__main__":
    print("Ensure the FastAPI server is running before executing this test.")
    # To run: python backend/tests/test_endpoints.py
    # But we need an event loop
    asyncio.run(test_traps())
