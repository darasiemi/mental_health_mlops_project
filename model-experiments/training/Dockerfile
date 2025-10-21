# Base
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System Python + build chain + headers for common PyPI packages
# - build-essential/pkg-config: C/C++ toolchain
# - libjpeg/zlib/libpng/freetype: Pillow/wordcloud/Matplotlib
# - libxml2/libxslt: lxml
# - libpq: psycopg2
# - curl/ca-certificates: TLS + downloads (often handy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    build-essential gcc g++ make pkg-config \
    libjpeg-turbo8-dev zlib1g-dev libpng-dev libfreetype6-dev \
    libxml2-dev libxslt1-dev \
    libpq-dev \
    curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Make `python` -> python3 (many tools expect `python`)
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip tooling and install Pipenv
RUN python -m pip install --upgrade pip setuptools wheel cython pipenv

# after Python/pipenv setup
RUN python -m pip install --no-cache-dir notebook ipykernel

WORKDIR /app

# Copy lockfiles first to leverage layer caching
COPY Pipfile Pipfile.lock ./

# Install EXACTLY what's in Pipfile.lock into the system site-packages
# (deterministic, no extra venv inside the image)
RUN pipenv install --system --deploy --ignore-pipfile

# Optional: if you need Jupyter in the image (classic Notebook + kernel)
# (Skip if Jupyter is already in your Pipfile.lock)
# RUN python -m pip install notebook ipykernel

# Now copy your application code
COPY . .

# Default entry (override at `docker run`)
CMD ["bash"]


