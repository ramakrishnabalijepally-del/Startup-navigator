from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, articles, resources, contact, search, dashboard, admin

settings = get_settings()

app = FastAPI(
    title="Startup Navigator API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Support comma-separated origins in FRONTEND_URL env var.
# e.g. FRONTEND_URL=https://foo.vercel.app,http://localhost:3000
_origins = [o.strip() for o in settings.frontend_url.split(",") if o.strip()]
if "http://localhost:3000" not in _origins:
    _origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(resources.router)
app.include_router(contact.router)
app.include_router(search.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
