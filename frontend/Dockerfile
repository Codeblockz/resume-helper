# Use official Node.js image from the Debian repository for building
FROM node:20-bookworm as build

# Set environment variables
ENV NODE_ENV=development

# Set work directory
WORKDIR /app

# Copy package.json and yarn.lock first to leverage Docker cache
COPY ./package.json .
COPY ./package-lock.json .

# Install Node.js dependencies
RUN npm install --prefer-offline --no-audit --force --legacy-peer-deps

# Copy the rest of the application code
COPY ./ /app

# Build the frontend for production
RUN npm run build

# Use official Nginx image for serving the production build
FROM nginx:alpine as production

# Copy Nginx configuration file
COPY ./default.conf /etc/nginx/conf.d/

# Copy built files from previous stage to Nginx HTML directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 3000 for Nginx
EXPOSE 3000
