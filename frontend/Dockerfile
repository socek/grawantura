FROM node:23 AS builder

ENV CODE_DIR /code

WORKDIR $CODE_DIR
RUN mkdir -p $CODE_DIR && mkdir -p /node_modules && ln -s /node_modules
ENV PATH /code/node_modules/.bin:$PATH

RUN npm install -g vite

COPY code/*.json .
COPY code/*.js .
COPY code/yarn.lock .
RUN yarn install

COPY code code/

# build target SPA
FROM builder AS frontend

RUN npm install -g vite
RUN vite build

# prepare target image with SPA only
FROM nginx:latest
WORKDIR /usr/share/nginx/html

COPY --from=frontend /code/dist .

EXPOSE 3000
CMD ["vite"]
