docker network create visit-net

docker run -d --name cache \
  --network visit-net \
  redis:8-alpine

docker run -d --name visit-counter \
  --network visit-net \
  -p 127.0.0.1:5050:5000 \
  -e REDIS_HOST=TODO \
  visit-counter:v1
