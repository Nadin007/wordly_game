# build env
FROM node:18.3.0-alpine3.14 as build
WORKDIR /app
COPY ./wordly-frontend/package*.json ./
RUN npm install
COPY ./wordly-frontend ./
RUN npm run build
# copy recursively 
CMD cp -r build result_build
