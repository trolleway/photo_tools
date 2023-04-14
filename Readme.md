


Build container


docker build --tag trolleway_photo:latest .

# Run

```
docker run --rm -v "${PWD}/photos:/opt/photo_tools/photos"  -it trolleway_photo:latest

```