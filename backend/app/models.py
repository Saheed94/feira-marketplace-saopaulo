import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography

from backend.app.database import Base


class Feira(Base):
    __tablename__ = "feiras"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    source = Column(
        String(50),
        nullable=False,
    )

    source_id = Column(
        Integer,
        nullable=False,
    )

    source_record_id = Column(
        String(50),
    )

    name = Column(
        String(255),
        nullable=False,
    )

    address = Column(
        Text,
    )

    operating_day = Column(
        String(30),
        nullable=False,
    )

    source_quantity = Column(
        Integer,
    )

    source_category_code = Column(
        String(10),
    )

    location = Column(
        Geography(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=False,
    )

    source_loaded_at = Column(
        DateTime(timezone=True),
    )

    source_updated_at = Column(
        DateTime(timezone=True),
    )

    source_data = Column(
        JSONB,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )