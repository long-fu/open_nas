import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def register_user():
    async with httpx.AsyncClient() as client:
        payload = {
            "username": "client_user",
            "email": "client@example.com",
            "password": "123456"
        }
        response = await client.post(f"{BASE_URL}/register", json=payload)
        print("Register:", response.status_code, response.json())

async def login_user():
    async with httpx.AsyncClient() as client:
        payload = {"username": "client_user", "password": "123456"}
        response = await client.post(f"{BASE_URL}/login", json=payload)
        print("Login:", response.status_code, response.json())

async def main():
    await register_user()
    await login_user()

if __name__ == "__main__":
    asyncio.run(main())
