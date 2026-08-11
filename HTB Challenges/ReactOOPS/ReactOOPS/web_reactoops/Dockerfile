FROM node:20-alpine

RUN apk add --no-cache libc6-compat curl

WORKDIR /app

COPY challenge/package.json ./
RUN npm install

COPY challenge/ .
RUN mkdir /app/public

RUN npm run build

RUN cp -r .next/static .next/standalone/.next/static
RUN cp -r public .next/standalone/public

ENV NODE_ENV=production
ENV PORT=1337
ENV HOSTNAME="0.0.0.0"

COPY challenge/flag.txt /app/flag.txt

EXPOSE 1337

CMD ["node", ".next/standalone/server.js"]
