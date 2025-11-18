# Use slim Python base for smaller image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering weirdly in Docker logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies required by openpyxl (minimal)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create working dir
WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Streamlit default config (override at runtime if you like)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]

