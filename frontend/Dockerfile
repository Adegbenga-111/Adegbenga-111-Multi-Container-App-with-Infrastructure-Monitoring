# =========================================================
# STAGE 1: BUILD THE REACT APPLICATION
# =========================================================

# Use a Node.js image to install dependencies and build React.
# Node.js is needed during development/building, not to serve
# the final static website.
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set /app as the working directory inside the container.
# Commands that follow will run from this directory.
WORKDIR /app

# Copy the package files first.
# package.json lists dependencies; package-lock.json locks
# their versions for reproducible installations.
COPY package.json package-lock.json* ./

# Install dependencies using npm ci.
# The cache mount speeds up later builds by reusing npm's cache.
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the frontend source code into /app.
# This includes src/, public/, nginx.conf and other files
# that are inside the frontend build context.
COPY . .

# Declare the API URL at build time.
# Create React App embeds REACT_APP_* values into the bundle.
# The browser accesses the API through localhost:8000.
ARG REACT_APP_API_URL=http://localhost:8000
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Compile the React source code into static files.
# Create React App normally writes these files to /app/build.
RUN npm run build


# =========================================================
# STAGE 2: SERVE THE BUILT REACT APPLICATION WITH NGINX
# =========================================================

# Use a separate Nginx image to serve the compiled website.
# The Node.js build environment is not needed at runtime.
FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Replace the default Nginx configuration with our own.
# Our configuration should listen on port 8080 and support
# React client-side routes.
COPY nginx.conf /etc/nginx/nginx.conf

# Copy only the compiled website from the builder stage.
# The source code and Node.js dependencies are not copied.
# Set ownership so the nginx user can read the files.
COPY --chown=nginx:nginx --from=builder /app/build /usr/share/nginx/html

# Run Nginx as a non-root user.
USER nginx

# Document the port used by Nginx inside the container.
EXPOSE 8080

# Start Nginx using our custom configuration file.
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]

# Keep Nginx running in the foreground so Docker can manage it.
CMD ["-g", "daemon off;"]
