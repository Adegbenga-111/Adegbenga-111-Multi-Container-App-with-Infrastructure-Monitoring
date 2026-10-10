# =========================================
# Stage 1: Build the React.js Application
# =========================================
FROM dhi.io/node:24-alpine3.22-dev AS builder

WORKDIR /app

# Copy package files directly from the current directory
COPY package.json package-lock.json* ./

RUN --mount=type=cache,target=/root/.npm npm ci

# Copy all source files directly from the current directory
COPY . .

RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================
FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config sitting right next to this Dockerfile
COPY nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginx:nginx --from=builder /app/build /usr/share/nginx/html

USER nginx
EXPOSE 8080

ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]