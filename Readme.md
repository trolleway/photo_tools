


Build container


docker build --tag trolleway_photo:latest .

# Run

```
docker run --rm -v "${PWD}:/opt/photo_tools"  -it trolleway_photo:latest

```