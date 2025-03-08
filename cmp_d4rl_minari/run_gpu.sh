docker run -td --gpus all \
    --name learn_corl \
    -p 6082:6080 \
    -p 2223:22 \
    -p 8081:8080 \
    --shm-size=512m \
    --volume=/home/ubuntu/CORL:/root/CORL \
    learn_corl

# docker run -td --gpus all \
#     --name border \
#     -p 6080:6080 \
#     --shm-size=512m \
#     --volume="$(pwd)/../../border:/root/border" \
#     --volume="$(pwd)/../marimo:/root/marimo" \
#     border
