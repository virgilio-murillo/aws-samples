FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the processing script
COPY standalone_region_training_test.py /opt/ml/code/
WORKDIR /opt/ml/code

# Set the entrypoint
ENTRYPOINT ["python", "standalone_region_training_test.py"]
