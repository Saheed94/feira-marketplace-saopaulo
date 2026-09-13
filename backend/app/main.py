from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.database import engine, get_db
from backend.app.models import Feira
from backend.app.schemas import (
    FeiraDetailResponse,
    FeiraResponse,
    NearbyFeiraResponse,
    VendorFeiraCreate,
    VendorFeiraResponse,
    VendorRegistrationRequest,
    VendorResponse,
)
# from backend.app.schemas import (
#     FeiraDetailResponse,
#     FeiraResponse,
#     NearbyFeiraResponse,
#     VendorRegistrationRequest,
#     VendorResponse,
# )

from backend.app.services.vendor_service import (
    associate_vendor_with_feira,
    register_vendor,
)

app = FastAPI(
    title="São Paulo Feira Marketplace API",
    description="API for discovering feiras and local marketplace vendors in São Paulo.",
    version="0.1.0",
)


# ==================================================
# Health Checks
# ==================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "feira-marketplace-api",
    }


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect():
            return {
                "status": "healthy",
                "database": "connected",
            }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }


# ==================================================
# Vendor Registration
# ==================================================

@app.post(
    "/api/v1/vendors/register",
    response_model=VendorResponse,
    status_code=201,
)
def register_vendor_endpoint(
    registration_data: VendorRegistrationRequest,
    db: Session = Depends(get_db),
):
    try:
        return register_vendor(
            db=db,
            user_data=registration_data.user,
            vendor_data=registration_data.vendor,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


# ==================================================
# Vendor-Feira Association
# ==================================================

@app.post(
    "/api/v1/vendors/{vendor_id}/feiras",
    response_model=VendorFeiraResponse,
    status_code=201,
)
def associate_vendor_feira(
    vendor_id: UUID,
    relationship_data: VendorFeiraCreate,
    db: Session = Depends(get_db),
):
    try:
        return associate_vendor_with_feira(
            db=db,
            vendor_id=vendor_id,
            feira_id=relationship_data.feira_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
# ==================================================
# List Feiras
# ==================================================

@app.get(
    "/api/v1/feiras",
    response_model=list[FeiraResponse],
)
def list_feiras(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: Session = Depends(get_db),
):
    return (
        db.query(Feira)
        .order_by(Feira.name)
        .offset(offset)
        .limit(limit)
        .all()
    )


# ==================================================
# Nearby Feiras
# ==================================================

@app.get(
    "/api/v1/feiras/nearby",
    response_model=list[NearbyFeiraResponse],
)
def nearby_feiras(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
    ),
    radius_km: float = Query(
        default=5,
        gt=0,
        le=50,
    ),
    operating_day: str | None = Query(
        default=None,
        min_length=5,
        max_length=30,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: Session = Depends(get_db),
):
    user_location = func.ST_GeogFromText(
        f"SRID=4326;POINT({longitude} {latitude})"
    )

    distance_meters = func.ST_Distance(
        Feira.location,
        user_location,
    )

    results = (
        db.query(
            Feira,
            (distance_meters / 1000).label("distance_km"),
        )
        .filter(
            func.ST_DWithin(
                Feira.location,
                user_location,
                radius_km * 1000,
            ),
            Feira.operating_day == operating_day
            if operating_day
            else True,
        )
        .order_by(distance_meters)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": feira.id,
            "name": feira.name,
            "address": feira.address,
            "operating_day": feira.operating_day,
            "distance_km": round(distance, 2),
        }
        for feira, distance in results
    ]


# ==================================================
# Feira Details
# ==================================================

@app.get(
    "/api/v1/feiras/{feira_id}",
    response_model=FeiraDetailResponse,
)
def get_feira(
    feira_id: UUID,
    db: Session = Depends(get_db),
):
    feira = (
        db.query(Feira)
        .filter(Feira.id == feira_id)
        .first()
    )

    if feira is None:
        raise HTTPException(
            status_code=404,
            detail="Feira not found",
        )

    return feira