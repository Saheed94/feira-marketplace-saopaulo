# Initial Data Model

## Objective

The first database milestone is to store official São Paulo feira locations and support geographic searches.

## Initial Entity

### feiras

| Field | Description |
|---|---|
| id | Internal UUID |
| source | Official data source |
| source_id | cd_identificador from GeoSampa |
| source_record_id | cd_registro from GeoSampa |
| name | Feira name |
| address | Official address |
| operating_day | Official operating day |
| source_quantity | Preserved source quantity |
| source_category_code | Preserved source category code |
| location | PostGIS geographic point |
| source_loaded_at | Source loading timestamp |
| source_updated_at | Source update timestamp |
| source_data | Original source record as JSONB |
| created_at | Internal creation timestamp |
| updated_at | Internal update timestamp |

## Design Principles

1. `source_id` is the official identity of a feira record.
2. Feira names must not be treated as unique.
3. Original source data must be preserved.
4. Official source fields must not be overwritten with marketplace data.
5. Coordinates will be converted from EPSG:31983 to EPSG:4326.
6. Vendor and product information will be introduced in later phases.

## Future Entities

- vendors
- vendor_feiras
- products
- categories
- customers
- orders
- order_items
- payments
- reviews
- deliveries