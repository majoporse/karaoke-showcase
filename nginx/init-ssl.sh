#!/bin/sh

if [ -f /etc/letsencrypt/live/hatal.cc/fullchain.pem ]; then
  echo 'Certificate already exists for hatal.cc. Skipping initialization.';
else
  echo 'No certificate found. Requesting from ZeroSSL...';
  certbot certonly --webroot -w /var/www/certbot \
    --cert-name hatal.cc \
    -d hatal.cc \
    --email admin@hatal.cc \
    --agree-tos --no-eff-email \
    --server https://acme.zerossl.com/v2/DV90 \
    --eab-kid GOvXtjYa0O_r5R6HP_tkUQ \
    --eab-hmac-key l6a0SkA75UxUHjg056mQdqJt00Do3W9ZDlszHiPsgBqhhQfelIwyFL31kelqMXBl39YDjvGF3e20BYxpOjUqQA \
    --non-interactive;
fi
