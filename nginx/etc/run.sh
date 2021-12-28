#!/bin/bash

echo HERE: '$$SERVER_NAME '

envsubst '$$SERVER_NAME ' < /etc/nginx/nginx.conf.tmp > /etc/nginx/nginx.conf &&

nginx -g "daemon off;"
