FROM nginx:1.13.5

EXPOSE 80

# Copies nginx.conf to a temporary file, so that we can use envsubst to replace environment variables on startup
COPY mime.types /etc/nginx/mime.types
COPY nginx.conf /etc/nginx/nginx.conf.template

# Use envsubst to replace only those environment variables that are defined in the OS,
# using the Bash built-in compgen to avoid envsubst replacing things that look like
# environment variables but aren't, e.g. `proxy_set_header Host $http_host;`
CMD /bin/bash -c "envsubst \"`printf '${%s} ' $(bash -c \"compgen -A variable\")`\" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"
