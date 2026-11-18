# syntax=docker/dockerfile:1
# ---------- Stage 1: build the Angular app with Node ----------
# BUILDPLATFORM keeps the Node build native even when producing arm64 images
FROM --platform=$BUILDPLATFORM node:22-alpine AS build

WORKDIR /app
COPY package.json package-lock.json .npmrc ./
RUN npm ci --no-audit --no-fund

COPY . .
RUN npm run build -- --configuration production

# ---------- Stage 2: serve the static bundle with Nginx ----------
FROM nginx:1.29-alpine

LABEL org.opencontainers.image.title="swamini-lms-frontend" \
      org.opencontainers.image.description="Angular frontend for the Swamini LMS served by Nginx" \
      org.opencontainers.image.source="https://github.com/swamini9403/swamini-lms"

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --retries=3 CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
