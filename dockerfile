# Use stable Node image (fixes your pull error)
FROM node:18

# Create app directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose port
EXPOSE 3000

# Start the correct file (FIXED)
CMD ["node", "server.js"]