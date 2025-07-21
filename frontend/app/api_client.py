import httpx

async def get_items(backend_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/items/")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        return []  # Return empty list if backend is unreachable
