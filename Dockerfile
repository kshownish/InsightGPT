# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
