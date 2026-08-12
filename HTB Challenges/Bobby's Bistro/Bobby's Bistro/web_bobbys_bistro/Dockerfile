FROM python:3.13-slim

WORKDIR /app

# Install system deps
RUN apt update && apt install -y curl supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy app source
COPY . .

RUN mv flag.txt /flag.txt

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /shared
RUN mv supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
