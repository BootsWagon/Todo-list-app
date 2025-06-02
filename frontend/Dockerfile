FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Install dependencies
RUN npm install

# Add write permissions for the node user
RUN chown -R node:node /app
USER node

EXPOSE 8080

CMD ["npm", "run", "serve"] 