#docker buildx build --pull --no-cache --platform linux/amd64 \
#  -t atlantatecnologia/at-balanca-haenni-simulador:latest \
#  --push .


docker buildx create --use --name mybuilder
docker buildx inspect mybuilder --bootstrap
docker buildx build --pull --no-cache --platform linux/amd64,linux/arm64 \
  -f Dockerfile \
  -t atlantatecnologia/at-balanca-haenni-simulador:latest \
  -t atlantatecnologia/at-balanca-haenni-simulador:arm64 \
  --push .