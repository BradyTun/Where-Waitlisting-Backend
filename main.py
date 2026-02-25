from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from models import WaitlistEntry
from database import init_db, add_entry, get_all_entries
import os
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from collections import defaultdict

# Test CI/CD change
# Another test change

load_dotenv()

ADMIN_KEY = os.getenv('ADMIN_KEY')

limiter = Limiter(key_func=get_remote_address)

total_requests = defaultdict(int)
banned_ips = set()

class BanMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/waitlist" and request.method == "POST":
            ip = request.client.host
            if ip in banned_ips:
                return JSONResponse(status_code=403, content={"error": "Banned"})
            total_requests[ip] += 1
            if total_requests[ip] >= 6:
                banned_ips.add(ip)
        response = await call_next(request)
        return response

def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too Many Requests, Will be Banned if Continue"})

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    # Add any cleanup here if needed

app = FastAPI(lifespan=lifespan)

app.add_middleware(BanMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

security = HTTPBearer()

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return credentials.credentials

@app.post("/waitlist")
@limiter.limit("3/minute")
async def add_to_waitlist(request: Request, entry: WaitlistEntry):

    if entry.email and '@' not in entry.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    try:
        add_entry(entry)
        return {"message": "Successfully added to waitlist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/waitlist")
async def get_waitlist(admin: str = Depends(verify_admin)):
    try:
        entries = get_all_entries()
        return {"entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}