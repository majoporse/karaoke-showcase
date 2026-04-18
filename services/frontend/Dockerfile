# --- Stage 1 & 2: Build ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
COPY .env.example .env

RUN npm run build

# --- Stage 3: Serve ---
FROM nginx:alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom config to the conf.d directory
# Ensure your local file is named 'nginx.conf'
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build files to the standard Nginx serve directory
COPY --from=build /app/build/client /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]