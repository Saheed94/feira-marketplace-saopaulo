# Feira Marketplace

A hyperlocal marketplace for discovering traditional **Feiras Livres**
in São Paulo, comparing vendor prices, and connecting consumers with
local sellers.

> **Project status:** The location-data foundation and an initial
> location API were previously implemented locally. The production AWS
> architecture and the broader marketplace capabilities described below
> are the intended design, not a claim that they have already been
> deployed. Verify the current repository and database before treating
> any implementation status as current.

------------------------------------------------------------------------

## Table of contents

-   [1. Project vision](#1-project-vision)
-   [2. Core user journeys](#2-core-user-journeys)
-   [3. Project status](#3-project-status)
-   [4. Technology direction](#4-technology-direction)
-   [5. Architecture at a glance](#5-architecture-at-a-glance)
-   [6. Detailed application
    architecture](#6-detailed-application-architecture)
-   [7. Request and data flows](#7-request-and-data-flows)
-   [8. Feira location data](#8-feira-location-data)
-   [9. Data model](#9-data-model)
-   [10. API design](#10-api-design)
-   [11. Security and operational
    considerations](#11-security-and-operational-considerations)
-   [12. Local development](#12-local-development)
-   [13. Suggested implementation
    roadmap](#13-suggested-implementation-roadmap)
-   [14. Product scope and future
    opportunities](#14-product-scope-and-future-opportunities)
-   [15. Contribution and development
    principles](#15-contribution-and-development-principles)

------------------------------------------------------------------------

## 1. Project vision

Feira Marketplace aims to make local market discovery and price
comparison easier for people in São Paulo, Brazil.

Consumers often need to visit multiple markets or contact sellers
individually to find a product, compare prices, and determine which
market is convenient. At the same time, many small Feira vendors rely on
physical foot traffic and WhatsApp rather than dedicated digital
storefronts.

The platform brings these two sides together.

### Product objectives

1.  **Discover:** Help consumers find Feiras and vendors near a
    location.
2.  **Compare:** Let consumers search for products and compare vendor
    prices.
3.  **Connect:** Make it easy to contact vendors, initially through
    WhatsApp or telephone.
4.  **Empower vendors:** Give small sellers a simple way to publish
    products, prices, and availability.
5.  **Build reliable local data:** Use official municipal Feira
    locations as the geographical foundation, then add
    marketplace-managed vendor and product information.

### Initial market

-   Launch geography: Municipality of São Paulo, Brazil.
-   Initial location reference: São Paulo municipal GeoSampa Feiras
    Livres dataset.
-   Primary experience: Discover → Compare → Contact.
-   Product localisation: Brazilian Portuguese should be considered for
    the Brazil launch, even though English was selected for the initial
    development experience.

------------------------------------------------------------------------

## 2. Core user journeys

### Consumer

1.  Open the marketplace.
2.  Search for a product or allow location access.
3.  Discover nearby Feiras and vendors.
4.  Compare product prices, units, distance, and update freshness.
5.  Open a vendor profile.
6.  Contact the vendor through WhatsApp or telephone.

### Vendor

1.  Create an account.
2.  Submit business and contact details.
3.  Select the Feira location(s) where the business operates.
4.  Wait for administrator review where approval is required.
5.  Create product listings with standardised units and prices.
6.  Update prices and availability.
7.  Receive customer enquiries through the published contact channel.

### Administrator

1.  Review vendor applications.
2.  Approve, reject, or suspend vendor profiles.
3.  Moderate product listings and reports.
4.  Maintain marketplace categories and operational data.
5.  Review data quality and activity.

------------------------------------------------------------------------

## 3. Project status

The following reflects the last project checkpoint recorded in the
development notes. It is not a live inspection of the current local
repository.

  -----------------------------------------------------------------------
  Area                    Last recorded position  Notes
  ----------------------- ----------------------- -----------------------
  Product concept and MVP Defined                 Discover, compare,
  scope                                           contact

  GeoSampa Feira dataset  Imported                975 location records
                                                  recorded

  Coordinate              Implemented             EPSG:31983 to EPSG:4326
  transformation                                  

  PostgreSQL + PostGIS    Implemented             Spatial location
                                                  storage

  Original source         Preserved               JSONB `source_data`
  attributes                                      field

  Spatial index           Recorded as implemented Verify index in current
                                                  database

  Initial backend         Implemented and tested  Earlier implementation
                                                  used Python/FastAPI

  Feira listing and       Tested                  Verify current route
  detail APIs                                     definitions

  Nearby Feira API        Tested                  Verify current spatial
                                                  query

  User authentication     Next milestone          Not confirmed as
                                                  implemented

  Vendor onboarding       Next milestone          Not confirmed as
                                                  implemented

  Vendor-to-Feira         Next milestone          Not confirmed as
  association                                     implemented

  Product catalogue and   Planned                 Not confirmed as
  pricing                                         implemented

  Consumer and vendor     Planned                 Verify repository
  frontend                                        

  AWS production          Target architecture     Not confirmed as
  deployment                                      deployed
  -----------------------------------------------------------------------

**Important technology history:** the earlier working local backend used
Python, FastAPI, and SQLAlchemy. Later planning selected Node.js, with
NestJS and TypeScript proposed for the application backend. Do not
assume a migration has happened. Inspect the actual repository before
changing frameworks or rewriting working location functionality.

------------------------------------------------------------------------

## 4. Technology direction

The following is the proposed technology direction. Actual dependencies
and deployed services must be verified against the repository and cloud
account.

  -----------------------------------------------------------------------
  Layer                   Proposed technology     Responsibility
  ----------------------- ----------------------- -----------------------
  Web frontend            Next.js + TypeScript    Consumer, vendor, and
                                                  admin interfaces

  Backend API             Node.js / NestJS +      Business logic and API
                          TypeScript (proposed)   

  Existing backend        Python / FastAPI        Earlier working
  baseline                                        location API

  Relational database     PostgreSQL              Users, vendors,
                                                  products, prices

  Geospatial database     PostGIS                 Feira points and
                                                  proximity queries

  Cache                   Redis (optional)        Caching and
                                                  rate-limiting support

  Maps                    Google Maps or Mapbox   Map display and
                                                  location interaction

  Media storage           Amazon S3               Vendor and product
                                                  images

  Containers              Docker                  Reproducible
                                                  application packaging

  Compute                 AWS ECS Fargate         Managed container
                                                  runtime

  Load balancing          Application Load        HTTPS routing to
                          Balancer                backend

  Database hosting        Amazon Aurora           Managed production
                          PostgreSQL Serverless   database
                          v2 (target)             

  Secrets                 AWS Secrets Manager     Database and
                                                  application secrets

  CDN                     Amazon CloudFront       Frontend and static
                                                  asset delivery

  Infrastructure as Code  Terraform               Repeatable cloud
                                                  infrastructure

  CI/CD                   GitHub Actions          Build, test, scan, and
                          (proposed)              deploy

  Observability           Amazon CloudWatch       Logs, metrics, alarms
  -----------------------------------------------------------------------

### Why PostgreSQL and PostGIS?

The marketplace has both relational and geographical requirements.

PostgreSQL supports relationships between users, vendors, products,
listings, and prices. PostGIS adds spatial types, indexes, and functions
for queries such as "find Feiras within five kilometres of this
coordinate."

Keeping these capabilities in PostgreSQL reduces the need to operate a
separate geospatial database for the initial product.

------------------------------------------------------------------------

## 5. Architecture at a glance

The diagram below shows the **proposed production target architecture**.
It is a logical design, not a deployment inventory.

``` mermaid
flowchart TB
    C[Consumers]
    V[Vendors]
    A[Administrators]

    subgraph EDGE["Public entry and delivery"]
        DNS[DNS and domain]
        CF[CloudFront CDN]
        WAF[AWS WAF]
        ALB[Application Load Balancer]
        WEB[S3 - Next.js static assets<br/>or frontend hosting origin]
    end

    subgraph APP["AWS application layer - VPC"]
        subgraph PRIVATE_APP["Private application subnets - multiple AZs"]
            ECS[ECS Fargate service<br/>Marketplace API]
            WORKER[Optional background worker<br/>notifications and imports]
        end

        subgraph PRIVATE_DATA["Private data subnets - multiple AZs"]
            DB[(Aurora PostgreSQL<br/>with PostGIS)]
            CACHE[(Optional Redis cache)]
        end

        SM[Secrets Manager]
        CW[CloudWatch logs, metrics and alarms]
    end

    S3MEDIA[S3 product and vendor media]
    EXT[External services<br/>Maps / WhatsApp integration]

    C --> DNS
    V --> DNS
    A --> DNS
    DNS --> CF
    CF --> WEB
    CF --> WAF
    WAF --> ALB
    ALB --> ECS
    ECS --> DB
    ECS -. optional .-> CACHE
    ECS --> SM
    ECS --> S3MEDIA
    ECS --> EXT
    ECS --> CW
    WORKER --> DB
    WORKER --> SM
    WORKER --> S3MEDIA
    WORKER --> CW
```

### Architecture explanation

-   **Consumers, vendors, and administrators:** Use the web application
    through their browsers or mobile browsers.
-   **DNS:** Resolves the marketplace domain.
-   **CloudFront:** Delivers frontend assets and can provide a
    distribution layer for application traffic.
-   **AWS WAF:** Filters malicious or unwanted HTTP requests before they
    reach the application.
-   **Application Load Balancer:** Routes API requests to healthy
    backend tasks.
-   **ECS Fargate:** Runs the containerised API without requiring
    management of EC2 worker nodes.
-   **Aurora PostgreSQL with PostGIS:** Stores relational marketplace
    data and geospatial Feira locations.
-   **Secrets Manager:** Stores database credentials and other sensitive
    configuration.
-   **S3 media bucket:** Stores product and vendor images. Keep the
    bucket private and serve authorised content through controlled
    access or CloudFront.
-   **CloudWatch:** Collects application logs, infrastructure metrics,
    and alarms.
-   **Redis:** Optional. Introduce it only when a measured caching,
    session, or rate-limiting requirement justifies it.
-   **Background worker:** Optional component for asynchronous work such
    as notifications, image processing, and scheduled data-quality
    tasks.
-   **External services:** Map providers and a future WhatsApp
    integration. These are integrations, not part of the core database.

### VPC and network placement

The target production design should use a VPC spanning at least two
Availability Zones.

  -----------------------------------------------------------------------
  Network area            Placement               Purpose
  ----------------------- ----------------------- -----------------------
  Public subnets          Multiple AZs            Application Load
                                                  Balancer and required
                                                  public ingress

  Private application     Multiple AZs            ECS Fargate tasks
  subnets                                         

  Private database        Multiple AZs            Aurora database
  subnets                                         instances

  VPC security groups     Between tiers           Restrict traffic to
                                                  explicitly required
                                                  ports and sources
  -----------------------------------------------------------------------

A subnet is not public merely because its CIDR range looks public or
private. Its route table and routing to an Internet Gateway determine
whether it is public. Security groups and network ACLs provide
additional traffic controls.

The database should not be directly exposed to the public internet. The
application should connect to it over private VPC networking.

------------------------------------------------------------------------

## 6. Detailed application architecture

The backend should initially be a **modular monolith**, not a collection
of microservices. A modular monolith keeps deployment and operations
manageable while allowing clear separation of business responsibilities.

``` mermaid
flowchart TB
    CLIENT[Web / Mobile Browser]

    subgraph API["Marketplace API"]
        ROUTER[HTTP routes and controllers]
        AUTH[Authentication and authorisation]
        USERS[User module]
        VENDORS[Vendor module]
        FEIRAS[Feira locations module]
        CATALOG[Product catalogue module]
        LISTINGS[Vendor listings module]
        PRICING[Price and price history module]
        SEARCH[Search and nearby discovery module]
        ADMIN[Administration and moderation module]
    end

    subgraph DATA["Persistence"]
        PG[(PostgreSQL + PostGIS)]
        OBJECTS[(Object storage - S3)]
    end

    CLIENT --> ROUTER
    ROUTER --> AUTH
    ROUTER --> USERS
    ROUTER --> VENDORS
    ROUTER --> FEIRAS
    ROUTER --> CATALOG
    ROUTER --> LISTINGS
    ROUTER --> PRICING
    ROUTER --> SEARCH
    ROUTER --> ADMIN

    USERS --> PG
    VENDORS --> PG
    FEIRAS --> PG
    CATALOG --> PG
    LISTINGS --> PG
    PRICING --> PG
    SEARCH --> PG
    ADMIN --> PG
    VENDORS --> OBJECTS
    CATALOG --> OBJECTS
```

### Suggested module responsibilities

  -----------------------------------------------------------------------
  Module                              Responsibility
  ----------------------------------- -----------------------------------
  Authentication                      Registration, login, password
                                      hashing, token lifecycle

  Users                               User profile and role management

  Vendors                             Business profile and approval
                                      workflow

  Feiras                              Official Feira location records and
                                      location queries

  Catalogue                           Standard product names and
                                      categories

  Listings                            Vendor-specific product offers

  Pricing                             Current price, price history, unit
                                      and freshness

  Search                              Product search, distance filtering
                                      and comparison

  Administration                      Vendor moderation, reports and data
                                      management
  -----------------------------------------------------------------------

Modules should communicate through clearly defined application services
rather than directly manipulating one another's internal implementation.

------------------------------------------------------------------------

## 7. Request and data flows

### A. Nearby Feira discovery

``` mermaid
sequenceDiagram
    actor Consumer
    participant UI as Web application
    participant API as Marketplace API
    participant DB as PostgreSQL + PostGIS

    Consumer->>UI: Allow location access
    UI->>API: GET /api/v1/feiras/nearby?lat=...&lng=...&radius=...
    API->>API: Validate coordinates and radius
    API->>DB: Execute indexed spatial query
    DB-->>API: Matching Feira records and distances
    API-->>UI: JSON results
    UI-->>Consumer: Display nearby Feiras on map/list
```

The API should validate latitude and longitude ranges, enforce a
sensible maximum radius, and use an appropriate spatial query and index.
Return distances with an explicitly documented unit.

### B. Product price comparison

``` mermaid
sequenceDiagram
    actor Consumer
    participant UI as Web application
    participant API as Marketplace API
    participant DB as PostgreSQL

    Consumer->>UI: Search for a product
    UI->>API: GET /api/v1/products/search?q=tomato
    API->>DB: Find matching standard products
    DB-->>API: Matching product IDs
    API->>DB: Fetch active vendor listings and latest valid prices
    DB-->>API: Vendor, Feira, price, unit and update time
    API-->>UI: Comparable offers
    UI-->>Consumer: Sort by price or distance
```

Price comparison must account for units. A price per kilogram should not
be compared directly with a price per pack unless the quantity is known
and a valid conversion can be made.

The response should show when each price was last confirmed or updated.

### C. Vendor onboarding and Feira association

``` mermaid
flowchart TD
    START[Vendor creates account]
    PROFILE[Submit business profile]
    LOCATION[Select existing Feira location]
    PENDING[Vendor status: PENDING]
    REVIEW[Administrator reviews application]
    DECISION{Approved?}
    ACTIVE[Vendor becomes ACTIVE]
    REJECTED[Vendor remains unavailable publicly]
    LIST[Create product listings]

    START --> PROFILE
    PROFILE --> LOCATION
    LOCATION --> PENDING
    PENDING --> REVIEW
    REVIEW --> DECISION
    DECISION -->|Yes| ACTIVE
    DECISION -->|No| REJECTED
    ACTIVE --> LIST
```

Vendor-to-Feira association must reference an existing Feira ID. Do not
create duplicate Feira records simply because a vendor registers at a
location already present in the municipal dataset.

------------------------------------------------------------------------

## 8. Feira location data

### Source

-   Dataset: GeoSampa -- Feiras Livres.
-   Publisher: São Paulo municipal government.
-   Recorded imported records: 975.
-   Original CRS: EPSG:31983 (SIRGAS 2000 / UTM zone 23S).
-   Application CRS: EPSG:4326 (WGS 84).
-   Recorded GeoJSON filename: `feiras_all.json`.
-   Recorded import script: `database/scripts/import_feiras.py`.

### Geographic extent

The recorded bounding box is:

  Boundary                   Value
  ------------------- ------------
  Minimum longitude     -46.826900
  Maximum longitude     -46.362653
  Minimum latitude      -24.008510
  Maximum latitude      -23.356460

In longitude/latitude order:

``` text
(-46.826900, -24.008510, -46.362653, -23.356460)
```

This is the extent of the data work, not a substitute for the actual 975
point geometries.

### Coordinate handling

EPSG:31983 is a projected coordinate reference system whose units are
metres. EPSG:4326 stores geographic longitude and latitude in degrees.

When transforming the data, use a GIS library or database transformation
function that understands the source and destination CRS. Do not relabel
EPSG:31983 coordinates as EPSG:4326 without transforming them.

For distance-based queries, use an appropriate PostGIS geography
operation or a correctly projected geometry. Document the distance unit
returned by the API.

### Source data versus marketplace data

The municipal dataset answers: **Where are the official Feira
locations?**

Marketplace-managed records answer:

-   Which vendors operate at a Feira?
-   What products do they sell?
-   What are their current prices?
-   Is the product available?
-   When was the price last updated?
-   How can the customer contact the vendor?

Keep these concerns separate. Preserve the original source attributes
for traceability and future reprocessing.

------------------------------------------------------------------------

## 9. Data model

The following is a proposed logical data model. It is not a claim that
every table has already been created.

``` mermaid
erDiagram
    USERS ||--o| VENDORS : owns
    USERS ||--o{ FAVORITES : saves
    VENDORS ||--o{ VENDOR_FEIRAS : operates_at
    FEIRAS ||--o{ VENDOR_FEIRAS : hosts
    CATEGORIES ||--o{ PRODUCTS : groups
    PRODUCTS ||--o{ VENDOR_PRODUCTS : offered_as
    VENDORS ||--o{ VENDOR_PRODUCTS : lists
    VENDOR_PRODUCTS ||--o{ PRICES : has_history
    VENDOR_PRODUCTS ||--o{ AVAILABILITY : reports
    USERS ||--o{ REPORTS : submits

    USERS {
        uuid id PK
        string name
        string email
        string password_hash
        string role
        timestamp created_at
    }

    VENDORS {
        uuid id PK
        uuid user_id FK
        string business_name
        string description
        string phone
        string whatsapp_number
        string status
        timestamp created_at
    }

    FEIRAS {
        uuid id PK
        string source
        string source_id
        string name
        string address
        string operating_day
        geography location
        jsonb source_data
    }

    VENDOR_FEIRAS {
        uuid id PK
        uuid vendor_id FK
        uuid feira_id FK
        string stall_reference
        boolean is_active
    }

    CATEGORIES {
        uuid id PK
        string name
        string slug
    }

    PRODUCTS {
        uuid id PK
        uuid category_id FK
        string name
        string slug
        string description
    }

    VENDOR_PRODUCTS {
        uuid id PK
        uuid vendor_id FK
        uuid product_id FK
        string unit
        boolean is_active
    }

    PRICES {
        uuid id PK
        uuid vendor_product_id FK
        decimal amount
        string currency
        timestamp recorded_at
        uuid recorded_by FK
    }

    AVAILABILITY {
        uuid id PK
        uuid vendor_product_id FK
        boolean is_available
        timestamp checked_at
    }

    FAVORITES {
        uuid id PK
        uuid user_id FK
        string target_type
        uuid target_id
    }

    REPORTS {
        uuid id PK
        uuid user_id FK
        string target_type
        uuid target_id
        string reason
        string status
        timestamp created_at
    }
```

### Data modelling rules

1.  **Feira records:** Preserve source identity and original source
    data. Use a stable unique constraint based on the source and source
    identifier where the source provides a reliable identifier.
2.  **Vendors:** A vendor profile belongs to a user account. Enforce
    appropriate uniqueness and ownership rules.
3.  **Vendor-Feira relationship:** Use a junction table because a vendor
    may operate at multiple Feiras and a Feira may host multiple
    vendors.
4.  **Products:** Keep standard product identity separate from vendor
    offers.
5.  **Vendor products:** Store the vendor-specific listing, unit, and
    active status here.
6.  **Prices:** Append price history rather than overwriting previous
    prices. Define how the current valid price is selected.
7.  **Availability:** Treat availability as time-sensitive information.
8.  **Currency:** Use BRL for Brazilian Real and a decimal/numeric
    database type for monetary values. Avoid floating-point types for
    money.
9.  **Auditability:** Record who submitted or changed important
    marketplace information.
10. **Tenant isolation:** If multi-tenant schema isolation is adopted
    later, define tenant ownership and access controls explicitly. Do
    not add schema-per-tenant complexity without a clear operational
    reason.

------------------------------------------------------------------------

## 10. API design

The following endpoints are a suggested API contract. Existing routes
should be inspected before adding or renaming endpoints.

### Health

  Method   Endpoint             Purpose
  -------- -------------------- -----------------------
  GET      `/health`            Application health
  GET      `/health/database`   Database connectivity

### Feiras

  Method   Endpoint                      Purpose
  -------- ----------------------------- ---------------------------------
  GET      `/api/v1/feiras`              List and filter Feira locations
  GET      `/api/v1/feiras/nearby`       Find nearby Feiras
  GET      `/api/v1/feiras/{feira_id}`   Retrieve one Feira

### Authentication and users

  Method   Endpoint                  Purpose
  -------- ------------------------- -----------------------
  POST     `/api/v1/auth/register`   Register account
  POST     `/api/v1/auth/login`      Authenticate
  GET      `/api/v1/users/me`        Retrieve current user
  PATCH    `/api/v1/users/me`        Update own profile

### Vendors

  Method   Endpoint                                 Purpose
  -------- ---------------------------------------- -----------------------------
  POST     `/api/v1/vendors`                        Submit vendor profile
  GET      `/api/v1/vendors/me`                     Retrieve own vendor profile
  PATCH    `/api/v1/vendors/me`                     Update own vendor profile
  GET      `/api/v1/vendors/{vendor_id}`            Public vendor profile
  POST     `/api/v1/vendors/me/feiras`              Associate vendor with Feira
  DELETE   `/api/v1/vendors/me/feiras/{feira_id}`   Remove association

### Products and pricing

  Method   Endpoint                                Purpose
  -------- --------------------------------------- --------------------------
  GET      `/api/v1/products`                      List/search products
  GET      `/api/v1/products/{product_id}`         Product details
  POST     `/api/v1/vendor-products`               Create vendor listing
  PATCH    `/api/v1/vendor-products/{id}`          Update own listing
  POST     `/api/v1/vendor-products/{id}/prices`   Add a price record
  GET      `/api/v1/products/{id}/offers`          Compare available offers

### Administration

  -------------------------------------------------------------------------------------
  Method                  Endpoint                              Purpose
  ----------------------- ------------------------------------- -----------------------
  GET                     `/api/v1/admin/vendors/pending`       Review pending vendors

  PATCH                   `/api/v1/admin/vendors/{id}/status`   Approve, reject or
                                                                suspend

  GET                     `/api/v1/admin/reports`               Review reports
  -------------------------------------------------------------------------------------

All private endpoints must enforce authentication, authorisation,
ownership, input validation, and appropriate rate limits. Public
endpoints must not expose private account or vendor information.

------------------------------------------------------------------------

## 11. Security and operational considerations

### Authentication and authorisation

-   Hash passwords using a modern password-hashing algorithm such as
    Argon2id or bcrypt with an appropriate work factor.
-   Never store plaintext passwords.
-   Enforce role-based permissions for consumers, vendors, and
    administrators.
-   Verify that vendors can only modify their own profiles and listings.
-   Protect administrative endpoints separately.
-   Validate token expiry and revocation strategy.

### Database

-   Keep production database instances in private subnets.
-   Restrict database ingress to the application security group.
-   Use TLS for database connections where supported and configured.
-   Store credentials in Secrets Manager, not source code or committed
    environment files.
-   Use migrations for controlled schema changes.
-   Back up production data and test restoration.

### API and user data

-   Validate all request bodies and query parameters.
-   Limit search radius and pagination sizes.
-   Apply rate limits to authentication and public search endpoints.
-   Avoid returning unnecessary personal information.
-   Obtain permission before accessing a consumer's location.
-   Do not expose precise consumer coordinates to vendors unless a
    feature genuinely requires it.

### Price integrity

-   Retain historical price changes.
-   Record timestamps and the actor/source of a price update.
-   Display when a price was last updated.
-   Provide a way to report inaccurate prices.
-   Consider vendor confirmation or expiry rules for stale prices.

### Observability

-   Emit structured application logs.
-   Monitor API latency and error rates.
-   Monitor database connections and query performance.
-   Add alarms for unhealthy tasks and database availability.
-   Avoid logging passwords, tokens, or sensitive personal information.

------------------------------------------------------------------------

## 12. Local development

Because the exact current repository and dependency versions have not
been independently inspected, treat these as setup principles rather
than guaranteed copy-and-run commands.

### Prerequisites

-   Git
-   Docker and Docker Compose
-   PostgreSQL with PostGIS, or a PostGIS-enabled container
-   The runtime required by the backend currently in the repository
-   Node.js if the NestJS migration or implementation has been completed
-   Python if the existing FastAPI backend remains in use

### Suggested local services

``` text
Developer machine
│
├── Frontend
│   └── Next.js application
│
├── Backend API
│   └── Existing FastAPI or migrated NestJS application
│
└── Database
    └── PostgreSQL + PostGIS
```

### Environment variables

Use an untracked `.env` file for local development. Provide a
`.env.example` containing variable names and safe placeholders only.

Typical configuration names may include:

``` dotenv
APP_ENV=development
DATABASE_URL=
JWT_SECRET=
S3_BUCKET_NAME=
AWS_REGION=
MAPS_API_KEY=
```

Do not commit real credentials, tokens, private keys, or production
connection strings.

### First-run verification checklist

-   [ ] Confirm which backend framework is actually present.
-   [ ] Confirm PostgreSQL is running.
-   [ ] Confirm the PostGIS extension is enabled.
-   [ ] Apply existing migrations.
-   [ ] Verify the Feira table exists.
-   [ ] Verify the imported record count.
-   [ ] Verify the spatial index exists.
-   [ ] Run backend tests.
-   [ ] Test `/health`.
-   [ ] Test `/health/database`.
-   [ ] Test Feira listing and detail endpoints.
-   [ ] Test nearby Feira search with known coordinates.
-   [ ] Confirm that existing records are not duplicated by ingestion.

Example SQL checks (adjust schema and column names to the actual
migrations):

``` sql
SELECT COUNT(*) FROM feiras;

SELECT PostGIS_Full_Version();

SELECT
    id,
    name,
    ST_SRID(location) AS srid
FROM feiras
LIMIT 5;
```

If `location` is stored as `geometry` or `geography`, adapt the query to
the actual column type. The expected application CRS is EPSG:4326, but
verify it from the database rather than assuming.

------------------------------------------------------------------------

## 13. Suggested implementation roadmap

### Phase 1 --- Repository and data audit

-   Inspect current directory structure and dependencies.
-   Confirm the backend framework.
-   Inspect database migrations and actual schema.
-   Verify the 975 imported Feira records.
-   Verify coordinate SRID and spatial index.
-   Test existing endpoints and spatial queries.
-   Document the actual state before making changes.

**Exit condition:** A reproducible local setup and a verified baseline
of the existing location API.

### Phase 2 --- Authentication and users

-   Create user model and migration.
-   Implement registration and login.
-   Hash passwords securely.
-   Implement roles and authorisation.
-   Add tests for valid and invalid access.

**Exit condition:** Users can register and authenticate securely.

### Phase 3 --- Vendor onboarding

-   Create vendor profile model.
-   Implement vendor submission.
-   Add pending/approved/rejected/suspended states.
-   Implement administrator review.
-   Enforce vendor ownership.

**Exit condition:** A vendor can submit a profile and an administrator
can approve it.

### Phase 4 --- Vendor-Feira association

-   Create the junction table.
-   Reference existing Feira records.
-   Prevent duplicate associations.
-   Support vendors operating at multiple locations.
-   Add tests for invalid and valid associations.

**Exit condition:** Approved vendors can be associated with existing
official Feira locations.

### Phase 5 --- Catalogue and pricing

-   Create categories and standard products.
-   Create vendor product listings.
-   Implement price history.
-   Standardise units and currency.
-   Implement availability and freshness rules.

**Exit condition:** Multiple vendors can offer the same product and
consumers can compare valid offers.

### Phase 6 --- Consumer experience

-   Product search.
-   Nearby Feira and vendor discovery.
-   Price and distance sorting.
-   Vendor profiles.
-   WhatsApp/telephone contact.
-   Map and list views.

**Exit condition:** A consumer can discover a product, compare offers,
and contact a vendor.

### Phase 7 --- Production readiness

-   Dockerise the application.
-   Create Terraform modules.
-   Deploy to ECS Fargate.
-   Provision private Aurora PostgreSQL.
-   Configure S3, ALB, Secrets Manager, CloudWatch and WAF.
-   Implement CI/CD, backups, monitoring and security checks.

**Exit condition:** A tested, monitored and secure production
deployment.

------------------------------------------------------------------------

## 14. Product scope and future opportunities

### Keep the first MVP focused

Prioritise:

-   Feira discovery.
-   Vendor onboarding.
-   Product listings.
-   Price comparison.
-   Vendor contact.

Defer until there is evidence of demand:

-   In-app payments.
-   Delivery fleet management.
-   Complex stock management.
-   AI-based price prediction.
-   Nationwide expansion.
-   Advanced loyalty systems.

### Future WhatsApp-first vendor workflow

Many Feira vendors already use WhatsApp and may not want to manage a
complicated dashboard.

A future integration could allow vendors to:

-   Submit product information through WhatsApp.
-   Send product photographs.
-   Update prices.
-   Report availability.
-   Confirm proposed changes before publication.

This should be an integration layer over the same vendor and product
domain model, not a separate source of truth.

### Potential business model

-   Free basic vendor profiles.
-   Premium vendor subscriptions.
-   Sponsored listings.
-   Future transaction commissions.
-   Aggregated market insights, subject to appropriate privacy and
    data-governance safeguards.

The first priority is marketplace trust, vendor adoption, accurate
prices, and repeat consumer usage.

------------------------------------------------------------------------

## 15. Contribution and development principles

The project should be developed incrementally and with a strong emphasis
on understanding the system.

Development principles:

1.  Inspect before modifying.
2.  Preserve working location functionality.
3.  Do not recreate or duplicate the 975 Feira records.
4.  Keep official municipal data separate from vendor-managed data.
5.  Explain database relationships before implementing them.
6.  Use migrations and automated tests.
7.  Validate every spatial query and coordinate transformation.
8.  Keep secrets out of source control.
9.  Prefer a modular monolith for the initial MVP.
10. Avoid introducing infrastructure or services without a clear
    requirement.
11. Document architecture decisions and operational trade-offs.
12. Verify every claimed implementation milestone against the actual
    code and database.

### Immediate next task

Start by auditing the existing local repository and database.

Specifically verify:

-   Current directory structure.
-   Existing backend framework.
-   Database connection and migrations.
-   PostGIS extension and spatial index.
-   Actual Feira record count.
-   Existing API routes and tests.
-   Current coordinate reference system.
-   Whether the proposed Node.js/NestJS transition has occurred.

Then implement **user authentication, vendor onboarding, vendor
approval, and vendor-to-Feira association** on top of the existing
location foundation.

The goal is not to rebuild what already works. The goal is to evolve the
existing geographical discovery backend into a reliable marketplace
while understanding every important architectural and implementation
decision.
