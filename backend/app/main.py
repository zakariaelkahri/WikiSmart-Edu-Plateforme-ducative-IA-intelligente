from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import routes_auth, routes_articles, routes_quiz, routes_admin, routes_health
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.db.init_db import init_db, init_data


# def create_app() -> FastAPI:
setup_logging()

app = FastAPI(
    title="WikiSmart Edu API",
    version="1.0.0",
    description="Core backend for EduSmart intelligent educational platform",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(routes_health.router, prefix="/api/v1")
app.include_router(routes_auth.router, prefix="/api/v1")
app.include_router(routes_articles.router, prefix="/api/v1")
app.include_router(routes_quiz.router, prefix="/api/v1")
app.include_router(routes_admin.router, prefix="/api/v1")

setup_exception_handlers(app)

@app.on_event("startup")
def on_startup() -> None:

    init_db()

# return app
@app.get("/seed")
def seed_database() -> dict:
    init_data()
    # print("Seeding database...")
    return {"message": "Database seeded successfully"}

# app = create_app()


