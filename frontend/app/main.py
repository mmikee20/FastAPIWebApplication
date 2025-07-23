from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api_client import get_items
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Use env variable or default to Docker network name for backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-api:8000")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    items = await get_items(BACKEND_URL)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

