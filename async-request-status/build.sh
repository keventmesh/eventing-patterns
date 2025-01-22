docker build -t quay.io/pierdipi/async-request-status-client -f ./client/Dockerfile ./client
docker build -t quay.io/pierdipi/async-request-status-status-service -f ./status/Dockerfile ./status

docker push quay.io/pierdipi/async-request-status-client:latest
docker push quay.io/pierdipi/async-request-status-status-service:latest

# Testing locally
# 1. Run status service
#   docker run --rm --net=host -p 8080:8080 -e SERVICE_HOST=http://localhost:8080 --name status-service quay.io/pierdipi/async-request-status-status-service
# 2. Run client
#   docker run --rm --net=host -e K_SINK=http://127.0.0.1:8080 -e STATUS_ENDPOINT=http://localhost:8080 quay.io/pierdipi/async-request-status-client
