# dev-border

Development environment for the [`border`](https://github.com/taku-y/border)
reinforcement learning library.

This repository collects the container images, helper scripts, and notes used to
build, run, and test the `border` crates across different platforms (Apple
Silicon, x86_64, and cloud GPU instances). It does not contain the library code
itself; instead it expects the `border` repository to be cloned alongside this
one and mounts it into the containers as a volume.

## Layout

Clone `border` next to `dev-border` so that the volume mounts in the run scripts
resolve correctly:

```text
.
├── border/       # the library (cloned separately)
└── dev-border/   # this repository
```

## Directories

| Directory         | Purpose                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `aarch64`         | Container image and scripts for Apple Silicon (aarch64), built with **Podman**. Tested on an M2 MacBook Air. |
| `docker_amd64`    | Container image and scripts for x86_64, built with **Docker**. Includes CPU and GPU (CUDA) variants. |
| `lambda_cloud`    | Notes for provisioning a GPU instance on [Lambda Cloud](https://lambdalabs.com/) and running the `docker_amd64` image there. |
| `cmp_d4rl_minari` | A separate container (`learn_corl`) for comparing the [D4RL](https://github.com/Farama-Foundation/D4RL) and [Minari](https://github.com/Farama-Foundation/Minari) offline-RL datasets. |
| `marimo`          | [marimo](https://marimo.io/) notebooks (e.g. `minari_dataset.py`) mounted into the containers. |
| `mlruns`          | [MLflow](https://mlflow.org/) tracking data produced by example runs.                       |

## Quick start

Each container directory ships `build*.sh`, `run*.sh`, and `remove.sh` helper
scripts and its own `README.md` with the details. In general:

```bash
cd <directory>   # e.g. aarch64 or docker_amd64
sh build.sh      # build the image
sh run.sh        # start the container (detached)
sh remove.sh     # stop and remove the container
```

The containers expose a browser-based GUI (noVNC) on `localhost:6080`. Inside
the GUI you can open a terminal and run examples, for instance:

```bash
cd $HOME/border
cargo run --example dqn_cartpole --features=tch
```

For GPU support on x86_64, use the `*_gpu.sh` variants in `docker_amd64`, which
build against a CUDA base image and pass `--gpus all` to the container.

## Atari ROMs (optional)

Some examples use the Atari Learning Environment (ALE) and require Atari ROMs.
The easiest way to obtain them is the
[AutoROM](https://pypi.org/project/AutoROM/) package; the `border-atari-env`
crate reads the ROM directory from the `ATARI_ROM_DIR` environment variable:

```bash
pip install autorom
mkdir $HOME/atari_rom
AutoROM --install-dir $HOME/atari_rom
export ATARI_ROM_DIR=$HOME/atari_rom
```

See the per-directory `README.md` files for platform-specific instructions.
