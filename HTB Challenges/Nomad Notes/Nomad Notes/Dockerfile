FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

COPY challenge/package*.json ./
RUN npm install --no-audit --no-fund

COPY challenge/ ./challenge/

RUN cp challenge/flag.txt ./flag.txt

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV BROWSERSLIST_IGNORE_OLD_DATA=1

RUN npx tailwindcss \
    -c ./challenge/tailwind.config.js \
    -i ./challenge/styles/input.css \
    -o ./challenge/public/css/app.css \
    --minify

CMD ["node", "challenge/app.js"]