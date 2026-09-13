-- ============================================================
-- Migration 002: Users, Vendors and Vendor-Feira Relationships
-- ============================================================

-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,

    full_name VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL DEFAULT 'CUSTOMER',

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_users_email UNIQUE (email),

    CONSTRAINT chk_users_role
        CHECK (role IN ('CUSTOMER', 'VENDOR', 'ADMIN'))
);

CREATE INDEX IF NOT EXISTS idx_users_email
ON users (email);

CREATE INDEX IF NOT EXISTS idx_users_role
ON users (role);


-- ============================================================
-- VENDORS
-- ============================================================

CREATE TABLE IF NOT EXISTS vendors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    business_name VARCHAR(255) NOT NULL,
    description TEXT,
    phone VARCHAR(50),

    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_vendors_user
        UNIQUE (user_id),

    CONSTRAINT fk_vendors_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_vendors_status
        CHECK (
            status IN (
                'PENDING',
                'APPROVED',
                'SUSPENDED',
                'REJECTED'
            )
        )
);

CREATE INDEX IF NOT EXISTS idx_vendors_status
ON vendors (status);

CREATE INDEX IF NOT EXISTS idx_vendors_business_name
ON vendors (business_name);


-- ============================================================
-- VENDOR_FEIRAS
-- ============================================================

CREATE TABLE IF NOT EXISTS vendor_feiras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    vendor_id UUID NOT NULL,
    feira_id UUID NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_vendor_feira
        UNIQUE (vendor_id, feira_id),

    CONSTRAINT fk_vendor_feiras_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vendor_feiras_feira
        FOREIGN KEY (feira_id)
        REFERENCES feiras(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_vendor_feiras_status
        CHECK (
            status IN (
                'PENDING',
                'APPROVED',
                'REJECTED'
            )
        )
);

CREATE INDEX IF NOT EXISTS idx_vendor_feiras_vendor
ON vendor_feiras (vendor_id);

CREATE INDEX IF NOT EXISTS idx_vendor_feiras_feira
ON vendor_feiras (feira_id);

CREATE INDEX IF NOT EXISTS idx_vendor_feiras_status
ON vendor_feiras (status);