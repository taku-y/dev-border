podman run -td  \
    --name border \
    -p 6080:6080 \
    -p 2222:2222 \
    --shm-size=512m \
    --volume="$(pwd)/../../border:/root/border" \
    --volume="$(pwd)/../marimo:/root/marimo" \
    border
