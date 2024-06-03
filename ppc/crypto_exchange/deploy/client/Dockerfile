FROM node:18

WORKDIR /client

COPY . .

RUN rm -rf node_modules/ && npm install

CMD ["npm", "run", "dev"]
