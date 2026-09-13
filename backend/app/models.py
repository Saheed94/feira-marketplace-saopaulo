from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)

from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

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
        BIGINT,
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

    vendor_relationships = relationship(
        "VendorFeira",
        back_populates="feira",
        cascade="all, delete-orphan",
    )


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash = Column(
        Text,
        nullable=False,
    )

    full_name = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(20),
        nullable=False,
        default="CUSTOMER",
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    vendor = relationship(
        "Vendor",
        back_populates="user",
        uselist=False,
    )


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    business_name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
    )

    phone = Column(
        String(50),
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
        "User",
        back_populates="vendor",
    )

    feira_relationships = relationship(
        "VendorFeira",
        back_populates="vendor",
        cascade="all, delete-orphan",
    )


class VendorFeira(Base):
    __tablename__ = "vendor_feiras"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    vendor_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "vendors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    feira_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "feiras.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    vendor = relationship(
        "Vendor",
        back_populates="feira_relationships",
    )

    feira = relationship(
        "Feira",
        back_populates="vendor_relationships",
    )