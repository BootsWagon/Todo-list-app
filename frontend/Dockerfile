FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Add write permissions for the node user
RUN chown -R node:node /app
USER node

EXPOSE 8080

CMD ["npm", "run", "serve"] 