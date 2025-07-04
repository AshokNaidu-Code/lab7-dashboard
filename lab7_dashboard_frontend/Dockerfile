# --- Build Stage ---
FROM node:18 AS builder

WORKDIR /app
COPY . .

# install and build your frontend (change commands to match your project)
RUN npm install
RUN npm run build

# --- Production Stage ---
FROM nginx:stable-alpine

# Copy built files to nginx public directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Optional: custom nginx config (if needed)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]