# São Paulo Feira Livre Data Source

## Official Source

Provider:

Prefeitura do Município de São Paulo

Dataset:

Feiras Livres

Source platform:

GeoSampa

Feature type:

geoportal:equipamento_feira_livre

WFS endpoint:

http://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/wfs

## Dataset Purpose

The dataset contains official georeferenced points representing feira livre locations in São Paulo.

The dataset is intended to provide the geographic foundation for the marketplace's feira discovery functionality.

## Current Dataset Statistics

- Total records: 975
- Geometry type: Point
- Coordinate reference system: EPSG:31983
- Source identifier: cd_identificador
- Feira name: nm_equipamento
- Address: tx_endereco_equipamento
- Operating day: tx_dia_funcionamento
- Source quantity: qt_equipamento

## Important Limitations

The official dataset does not provide:

- Number of individual vendors or stalls
- Complete feira boundaries
- Exact physical extent of each feira
- Vendor information
- Product information
- Product prices
- Inventory
- Customer reviews
- Delivery information

Therefore, GeoSampa will be used as the official geographic reference layer, while marketplace-specific information will be stored separately in our application database.