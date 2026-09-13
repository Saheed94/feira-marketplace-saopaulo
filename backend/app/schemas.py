from uuid import UUID

from pydantic import BaseModel, ConfigDict


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