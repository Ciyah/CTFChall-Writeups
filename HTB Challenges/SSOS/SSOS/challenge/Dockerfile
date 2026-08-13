FROM node:bookworm-slim

RUN apt update && apt install -y nginx supervisor curl wget sqlite3 gcc dos2unix
# Install Go 
RUN wget https://go.dev/dl/go1.24.3.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.24.3.linux-amd64.tar.gz
RUN export PATH=$PATH:/usr/local/go/bin

# Install Chrome
RUN wget https://chrome-versions.com/google-chrome-stable-130.0.6723.58-1.deb
RUN apt install -y ./google-chrome-stable-130.0.6723.58-1.deb

# Copy nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

WORKDIR /app/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . .

RUN dos2unix /app/entrypoint.sh /app/bot/start-bot.sh
RUN chmod +x bot/start-bot.sh
RUN chmod +x /app/entrypoint.sh

RUN cd /app/client && npm install
RUN cd /app/bot && npm install

ENV PATH=$PATH:/usr/local/go/bin
RUN cd /app/sso-provider && \
    /usr/local/go/bin/go mod download && \
    /usr/local/go/bin/go build -o /app/sso-provider/sso-server ./cmd/server/main.go

EXPOSE 1337

# Convert line endings and make scripts executable

ENTRYPOINT ["./entrypoint.sh"]