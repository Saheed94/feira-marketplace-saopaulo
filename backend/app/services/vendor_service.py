from sqlalchemy import cast, String
from sqlalchemy.orm import Session

from backend.app.models import User, Vendor, VendorFeira, Feira
from backend.app.schemas import UserCreate, VendorCreate
from backend.app.security import hash_password


def register_vendor(
    db: Session,
    user_data: UserCreate,
    vendor_data: VendorCreate,
) -> Vendor:
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user is not None:
        raise ValueError("A user with this email already exists")

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        role="VENDOR",
        is_active=True,
    )

    db.add(user)
    db.flush()

    vendor = Vendor(
        user_id=user.id,
        business_name=vendor_data.business_name,
        description=vendor_data.description,
        phone=vendor_data.phone,
        status="PENDING",
    )

    db.add(vendor)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(vendor)

    return vendor


def associate_vendor_with_feira(
    db: Session,
    vendor_id,
    feira_id,
) -> VendorFeira:
    vendor = (
        db.query(Vendor)
        .filter(cast(Vendor.id, String) == str(vendor_id))
        .first()
    )

    if vendor is None:
        raise ValueError("Vendor not found")

    feira = (
        db.query(Feira)
        .filter(cast(Feira.id, String) == str(feira_id))
        .first()
    )

    if feira is None:
        raise ValueError("Feira not found")

    existing_relationship = (
        db.query(VendorFeira)
        .filter(
            cast(VendorFeira.vendor_id, String) == str(vendor_id),
            cast(VendorFeira.feira_id, String) == str(feira_id),
        )
        .first()
    )

    if existing_relationship is not None:
        raise ValueError(
            "Vendor is already associated with this feira"
        )

    vendor_feira = VendorFeira(
        vendor_id=vendor_id,
        feira_id=feira_id,
        status="PENDING",
    )

    db.add(vendor_feira)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(vendor_feira)

    return vendor_feira