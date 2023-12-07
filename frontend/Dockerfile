FROM node:20-alpine

WORKDIR /frontend/project

COPY ./project/package*.json ./

RUN npm install

COPY ./project .

EXPOSE 8080

CMD ["npm", "run", "serve"]