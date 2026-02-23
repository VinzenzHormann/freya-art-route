# Step 1: Use an official Python "slim" image (lightweight)
FROM python:3.11-slim

# Step 2: Set the "office" directory inside the container
WORKDIR /app

# Step 3: Copy the requirements list first (for faster building)
COPY requirements.txt .

# Step 4: Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your code and your CSV into the container
COPY main.py .
COPY venues.csv .

# Step 6: The command to start the API
# We use 0.0.0.0 to make it accessible to the internet
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]