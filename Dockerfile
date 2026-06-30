FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    xvfb \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libx11-xcb1 \
    fonts-liberation

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

RUN apt-get update && apt-get install -y google-chrome-stable

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]