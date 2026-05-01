FROM node:22.21

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --no-cache

EXPOSE 5175

CMD ["node_modules/.bin/vite"]
