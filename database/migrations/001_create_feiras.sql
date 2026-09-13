CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS feiras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    source VARCHAR(50) NOT NULL DEFAULT 'GEOSAMPA',

    source_id BIGINT NOT NULL,

    source_record_id VARCHAR(50),

    name VARCHAR(255) NOT NULL,

    address TEXT,

    operating_day VARCHAR(30) NOT NULL,

    source_quantity INTEGER,

    source_category_code VARCHAR(10),

    location GEOGRAPHY(POINT, 4326) NOT NULL,

    source_loaded_at TIMESTAMPTZ,

    source_updated_at TIMESTAMPTZ,

    source_data JSONB NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_feiras_source
        UNIQUE (source, source_id)
);

CREATE INDEX IF NOT EXISTS idx_feiras_location
ON feiras
USING GIST (location);

CREATE INDEX IF NOT EXISTS idx_feiras_operating_day
ON feiras (operating_day);

CREATE INDEX IF NOT EXISTS idx_feiras_name
ON feiras (name);