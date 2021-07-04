FROM nginx:alpine
 
RUN apk update \
    && apk upgrade \
    #openssl追加
    && apk add --no-cache openssl \
    #certbot追加
    && apk add --no-cache certbot \
    && apk add --no-cache bash
 
RUN set -x ; \
    addgroup -g 82 -S www-data ; \
    adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1
 
 
EXPOSE 80 443
