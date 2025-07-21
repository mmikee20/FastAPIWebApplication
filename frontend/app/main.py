from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api_client import get_items
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 👇 Change this to match your Docker Compose service name and port
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-api:8000")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    items = await get_items(BACKEND_URL)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})
