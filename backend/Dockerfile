# ==========================================
# STAGE 1: The Builder
# ==========================================
FROM python:3.12 AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# ==========================================
# STAGE 2: The Runtime
# ==========================================
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the app folder into a 'backend' folder inside the container
COPY ./app ./backend/app

EXPOSE 8000

# We must now tell uvicorn to look inside 'backend.app.main'
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]








# # ==========================================
# # STAGE 1: The Builder
# # ==========================================
# FROM python:3.12 AS builder

# # Install system dependencies needed for compilation
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Copy requirements and build wheels
# COPY requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# # ==========================================
# # STAGE 2: The Runtime
# # ==========================================
# FROM python:3.12-slim

# WORKDIR /app

# # Copy the pre-compiled wheels from the builder stage
# COPY --from=builder /app/wheels /wheels

# # Install the packages from the wheels
# RUN pip install --no-cache /wheels/*

# # Copy the actual application code
# COPY ./app ./app

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]