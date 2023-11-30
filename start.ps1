docker build --tag trolleway_photo:latest .
docker run --rm -v "${PWD}/photos:/opt/photo_tools/photos"  -it trolleway_photo:latest