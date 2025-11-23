# 1?? Choose a base image with Python
FROM python:3.12.1

# 2?? Set working directory
WORKDIR /data-curation-indie-games

# 3?? Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4?? Copy your project files
COPY . .

# 5?? Expose Jupyter¡¯s default port
EXPOSE 8888

# 6?? Default command: launch Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
