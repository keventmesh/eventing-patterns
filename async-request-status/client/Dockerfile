# Use Red Hat's Universal Base Image (UBI) for Python
FROM registry.access.redhat.com/ubi9/python-311:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    K_SINK="" \
    STATUS_ENDPOINT=""

# Switch to root for installation
USER 0

# Create app directory and set permissions
RUN mkdir -p /opt/app-root/src && \
    chown -R 1001:0 /opt/app-root/src && \
    chmod -R g=u /opt/app-root/src

WORKDIR /opt/app-root/src

# Copy requirements and install dependencies
COPY --chown=1001:0 requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=1001:0 client.py .

# Switch back to non-root user (1001 is the default non-root user in UBI images)
USER 1001

# Define entry point
CMD ["python", "client.py"]
