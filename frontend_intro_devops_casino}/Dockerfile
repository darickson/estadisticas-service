# syntax=docker/dockerfile:1
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# nginx-unprivileged ya corre como usuario no root (uid 101) por defecto
FROM nginxinc/nginx-unprivileged:1.25-alpine
COPY --from=build /app/dist/casino-frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
