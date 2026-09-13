import json
from datetime import datetime, timezone

import psycopg2
from pyproj import Transformer


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "feira_marketplace",
    "user": "feira_admin",
    "password": "feira_dev_password",
}


GEOJSON_FILE = "data/feiras_all.json"


# GeoSampa source CRS: EPSG:31983
# Application/database CRS: EPSG:4326
transformer = Transformer.from_crs(
    "EPSG:31983",
    "EPSG:4326",
    always_xy=True,
)


def parse_timestamp(value):
    if not value:
        return None

    value = value.replace("Z", "+00:00")

    return datetime.fromisoformat(value)


def load_geojson():
    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_coordinates(x, y):
    longitude, latitude = transformer.transform(x, y)
    return longitude, latitude


def import_feiras():
    geojson = load_geojson()
    features = geojson["features"]

    print(f"Records found in GeoJSON: {len(features)}")

    connection = psycopg2.connect(**DATABASE_CONFIG)

    try:
        with connection:
            with connection.cursor() as cursor:

                for feature in features:
                    properties = feature["properties"]
                    coordinates = feature["geometry"]["coordinates"]

                    source_id = properties["cd_identificador"]
                    source_record_id = properties.get("cd_registro")

                    name = properties.get("nm_equipamento")
                    address = properties.get("tx_endereco_equipamento")
                    operating_day = properties.get("tx_dia_funcionamento")

                    source_quantity = properties.get("qt_equipamento")
                    source_category_code = properties.get("cd_tipo_categoria")

                    source_loaded_at = parse_timestamp(
                        properties.get("dt_carga")
                    )

                    source_updated_at = parse_timestamp(
                        properties.get("dt_atualizacao")
                    )

                    longitude, latitude = transform_coordinates(
                        coordinates[0],
                        coordinates[1],
                    )

                    cursor.execute(
                        """
                        INSERT INTO feiras (
                            source,
                            source_id,
                            source_record_id,
                            name,
                            address,
                            operating_day,
                            source_quantity,
                            source_category_code,
                            location,
                            source_loaded_at,
                            source_updated_at,
                            source_data
                        )
                        VALUES (
                            'GEOSAMPA',
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            ST_SetSRID(
                                ST_MakePoint(%s, %s),
                                4326
                            )::geography,
                            %s,
                            %s,
                            %s
                        )
                        ON CONFLICT (source, source_id)
                        DO UPDATE SET
                            source_record_id = EXCLUDED.source_record_id,
                            name = EXCLUDED.name,
                            address = EXCLUDED.address,
                            operating_day = EXCLUDED.operating_day,
                            source_quantity = EXCLUDED.source_quantity,
                            source_category_code = EXCLUDED.source_category_code,
                            location = EXCLUDED.location,
                            source_loaded_at = EXCLUDED.source_loaded_at,
                            source_updated_at = EXCLUDED.source_updated_at,
                            source_data = EXCLUDED.source_data,
                            updated_at = NOW();
                        """,
                        (
                            source_id,
                            source_record_id,
                            name,
                            address,
                            operating_day,
                            source_quantity,
                            source_category_code,
                            longitude,
                            latitude,
                            source_loaded_at,
                            source_updated_at,
                            json.dumps(feature),
                        ),
                    )

        print(f"Successfully imported {len(features)} records.")

    finally:
        connection.close()


if __name__ == "__main__":
    import_feiras()