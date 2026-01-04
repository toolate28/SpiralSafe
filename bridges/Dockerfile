# SpiralSafe Hardware Bridges - Production Container
FROM python:3.11-slim

LABEL maintainer="Hope&&Sauced Collaborative"
LABEL description="SpiralSafe hardware integration bridges - ATOM trail, hologram, Tartarus Pro"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libusb-1.0-0 \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bridge modules
COPY atom/ ./atom/
COPY hologram/ ./hologram/
COPY tartarus/ ./tartarus/
COPY *.py ./
COPY README.md .

# Create ATOM trail directory
RUN mkdir -p /data/atom-trails

# Create volume for persistent ATOM data
VOLUME ["/data/atom-trails"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ATOM_TRAIL_PATH=/data/atom-trails/default.atom
ENV DEVICE_MODE=virtual

# Expose ports (for future web interface)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from hologram import HologramDevice; import asyncio; asyncio.run(HologramDevice('virtual').connect())"

# Default command: run hologram bridge in ATOM streaming mode
CMD ["python", "hologram-bridge.py", "--mode", "atom", "--trail", "/data/atom-trails/default.atom", "--device", "virtual"]
