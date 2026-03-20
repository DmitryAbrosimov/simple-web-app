FROM nginx:stable-alpine3.23-slim

ARG EXPOSE_NGINX_PORT=80

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE ${EXPOSE_NGINX_PORT}

CMD ["nginx", "-g", "daemon off;"]
