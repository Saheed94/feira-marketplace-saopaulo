from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ============================================================
# FEIRA SCHEMAS
# ============================================================

class FeiraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str | None = None
    operating_day: str


class NearbyFeiraResponse(FeiraResponse):
    distance_km: float


class FeiraDetailResponse(FeiraResponse):
    source: str
    source_id: int
    source_record_id: str | None = None
    source_quantity: int | None = None
    source_category_code: str | None = None


# ============================================================
# USER SCHEMAS
# ============================================================

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool


# ============================================================
# VENDOR SCHEMAS
# ============================================================

class VendorCreate(BaseModel):
    business_name: str
    description: str | None = None
    phone: str | None = None


class VendorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    business_name: str
    description: str | None = None
    phone: str | None = None
    status: str


# ============================================================
# VENDOR REGISTRATION
# ============================================================

class VendorRegistrationRequest(BaseModel):
    user: UserCreate
    vendor: VendorCreate


# ============================================================
# VENDOR-FEIRA SCHEMAS
# ============================================================

class VendorFeiraCreate(BaseModel):
    feira_id: UUID


class VendorFeiraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vendor_id: UUID
    feira_id: UUID
    status: str