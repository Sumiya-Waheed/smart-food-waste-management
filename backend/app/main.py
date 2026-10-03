from fastapi import FastAPI

from app.routes.donation_requests import router as donation_requests_router
from app.routes.donations import router as donations_router
from app.routes.organizations import router as organizations_router
from app.routes.restaurants import router as restaurants_router


app = FastAPI(
    title="Smart Food Waste Management API",
    description=(
        "Backend API for the Smart Food Waste Management "
        "hackathon project."
    ),
    version="1.0.0",
)


app.include_router(donations_router)
app.include_router(restaurants_router)
app.include_router(organizations_router)
app.include_router(donation_requests_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Smart Food Waste Management API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy",
    }