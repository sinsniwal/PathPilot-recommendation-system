FROM node:20-alpine

WORKDIR /frontend/project

COPY ./project .

RUN npm install

EXPOSE 8080

CMD ["npm", "run", "serve"]