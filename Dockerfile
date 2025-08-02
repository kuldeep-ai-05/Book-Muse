# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /frontend

# Copy and install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all frontend source code into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app, listening on all interfaces
CMD ["streamlit", "run", "BookMuse.py", "--server.port=8501", "--server.address=0.0.0.0"]
