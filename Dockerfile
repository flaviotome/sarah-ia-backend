FROM ubuntu:22.04

# Base image with Python
FROM python:3.9-slim

# Install dependencies for Chrome and Xvfb
RUN apt-get update && apt-get install -y \
    xvfb \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libgtk-3-0 \
    libgbm-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crie um diretório para o Chrome
RUN mkdir -p /opt/chrome

#No diretorio raiz do projeto, utilize o comando 'wget' para baixar as versoes compativeis do Google Chrome e do Chromedriver

# Copie o arquivo chrome-linux64.zip do diretório de build
COPY chrome-linux64.zip /opt/chrome/

# Extraia o arquivo
RUN unzip /opt/chrome/chrome-linux64.zip -d /opt/chrome/

# Adicione o binário do Chrome ao PATH
ENV PATH="/opt/chrome/chrome-linux64:${PATH}"


# Crie um diretório para o ChromeDriver
RUN mkdir -p /opt/chromedriver

# Copie o arquivo chromedriver-linux64.zip do diretório de build
COPY chromedriver-linux64.zip /opt/chromedriver/

# Extraia o arquivo
RUN unzip /opt/chromedriver/chromedriver-linux64.zip -d /opt/chromedriver/

# Adicione o binário do ChromeDriver ao PATH
ENV PATH="/opt/chromedriver:${PATH}"

# Copy the Python dependencies list
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files to the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Copy entrypoint script to set up Xvfb and Chrome
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Start the application
ENTRYPOINT ["/entrypoint.sh"]
