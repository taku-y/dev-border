# Path to the border repository to mount into the container.
# Defaults to ../../border but can be overridden with the first argument.
# Resolved to an absolute path because podman (on the macOS VM) does not
# resolve relative volume paths against the host shell's cwd.
BORDER_PATH="${1:-../../border}"
BORDER_PATH="$(cd "$(dirname "$BORDER_PATH")" && pwd)/$(basename "$BORDER_PATH")"

podman run -td  \
    --name border \
    -p 6080:6080 \
    -p 2222:22 \
    --shm-size=512m \
    --volume="${BORDER_PATH}:/root/border" \
    --volume="$(pwd)/../marimo:/root/marimo" \
    border
