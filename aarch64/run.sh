# Path to the border repository to mount into the container.
# Defaults to ../../border but can be overridden with the first argument.
BORDER_PATH="${1:-$(pwd)/../../border}"

podman run -td  \
    --name border \
    -p 6080:6080 \
    -p 2222:22 \
    --shm-size=512m \
    --volume="${BORDER_PATH}:/root/border" \
    --volume="$(pwd)/../marimo:/root/marimo" \
    border
