# Use official Node.js image from the Debian repository
FROM node:20-bookworm

# Set environment variables
ENV NODE_ENV=development

# Set work directory
WORKDIR /app

# Copy package.json and yarn.lock first to leverage Docker cache
COPY ./package.json .
COPY ./package-lock.json .

# Install Node.js dependencies
RUN npm install --prefer-offline --no-audit

# Copy the rest of the application code
COPY ./ /app

# Expose the port the app runs on
EXPOSE 3000

# Run the Vite development server
CMD ["npm", "run", "dev"]
