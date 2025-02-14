docker run -td  \
    --name border \
    -p 6080:6080 \
    -p 22:22 \
    -p 8000:8000 \
    -p 8080:8080 \
    --shm-size=512m \
    --volume="$(pwd)/../../border:/root/border" \
    --volume="$(pwd)/../marimo:/root/marimo" \
    border
