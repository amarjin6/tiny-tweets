FROM node:20-alpine as build
WORKDIR /usr/src
COPY . .
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN yarn
RUN yarn build

FROM nginx:alpine
COPY --from=build /usr/src/build /usr/share/nginx/html
COPY --from=build /usr/src/nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]
