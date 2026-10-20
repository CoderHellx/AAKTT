# Ubuntu development setup

How to set up AAKTT+ on Ubuntu (tested target: Ubuntu 24.04 LTS) and keep working with Claude
Code the same way as on Windows. Every step ends with a **check**. Don't move on until it passes.

> **Why Ubuntu:** Docker runs natively (no VM), file access is faster, there are no line-ending
> issues, and it matches CI and any future server, which all run Linux.

---

## 0. Ground rules

- **Keep the repo in your Linux home** (e.g. `~/dev/aaktt`), *not* on the Windows partition
  (`/mnt/c/...`). The NTFS partition is slow from Linux and breaks file permissions.
- Your `.env` is not in Git, so you'll create a fresh one from `.env.example` (step 6).
- Ollama models and Docker data are per-OS. You'll download the model again (~5 GB).

## 1. Base packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl build-essential ca-certificates
```

**Check:** `git --version` prints a version.

## 2. Git identity + GitHub sign-in

```bash
git config --global user.name "CoderHellx"
git config --global user.email "ea.hengirmen@gmail.com"
git config --global init.defaultBranch main
```

Sign in to GitHub with the official CLI. It stores credentials securely, so `git push` just works:

```bash
sudo apt install -y gh        # if not found: follow https://cli.github.com
gh auth login                 # choose: GitHub.com → HTTPS → "Login with a web browser"
gh auth setup-git
```

**Check:** `gh auth status` shows you're logged in as CoderHellx.

## 3. NVIDIA driver (for Ollama on your RTX 4060)

```bash
ubuntu-drivers devices        # shows the recommended driver
sudo ubuntu-drivers install   # installs it
sudo reboot
```

If **Secure Boot** is on, you'll be asked to set a password during install, and after the reboot
a blue "MOK management" screen appears. Choose *Enroll MOK* and enter that password, or the
driver won't load.

**Check:** `nvidia-smi` shows "GeForce RTX 4060 Laptop GPU" and about 8 GB of memory.

## 4. Docker Engine (native, no Docker Desktop needed)

```bash
curl -fsSL https://get.docker.com | sh       # Docker's official install script
sudo usermod -aG docker $USER                # run docker without sudo
```

**Log out and back in** (or reboot) so the group change applies.

**Check:** `docker run --rm hello-world` prints "Hello from Docker!" without `sudo`.

## 5. uv (Python manager) and Python 3.13

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc              # or open a new terminal
uv python install 3.13        # uv manages Python itself, so there's no conflict with Ubuntu's system Python
```

**Check:** `uv --version` works in a new terminal.

## 6. Clone and run the project

```bash
mkdir -p ~/dev && cd ~/dev
git clone https://github.com/CoderHellx/AAKTT-.git aaktt
cd aaktt
cp .env.example .env
docker compose up -d --wait   # Postgres; should end with "Healthy"
cd backend
uv sync                       # creates .venv from uv.lock: identical versions to Windows
uv run pytest                 # expect: 6 passed
uv run uvicorn app.main:create_app --factory --reload
```

**Check:** http://localhost:8000/health returns
`{"status":"ok","version":"0.1.0","database":"ok"}`.

## 7. Ollama + the model

```bash
curl -fsSL https://ollama.com/install.sh | sh   # installs and starts it as a system service
ollama pull qwen3:8b
```

**Check:** `ollama run qwen3:8b "Say hi in 3 words"` answers, and `nvidia-smi` shows Ollama
using GPU memory while it runs. If it's slow and the GPU is idle, step 3 didn't work.

## 8. Editor

VS Code (`sudo snap install code --classic`) with these extensions: **Python**, **Ruff**,
**Docker**. In settings, enable **Format On Save** with Ruff as the Python formatter. Then
whitespace never fails `ruff format --check` again.

## 9. Claude Code

On Ubuntu, Claude Code runs in the terminal. Install it from the official docs:
https://docs.claude.com/en/docs/claude-code/setup

```bash
curl -fsSL https://claude.ai/install.sh | bash   # native installer (see docs if this changes)
cd ~/dev/aaktt
claude                                            # sign in on first run
```

**How the mentoring carries over:** Claude Code automatically reads `CLAUDE.md` (your mentoring
rules) from the repo. The conversation history from Windows does **not** carry over, so start the
first session with:

> Read CLAUDE.md, ARCHITECTURE.md and the "Current status" section of README.md, then check
> `git log`. We're continuing Phase 1, milestone 1, step 5 (CI). Explain the why first, then
> wait for my go.

Useful habits in the terminal version:
- **Shift+Tab** cycles permission modes (e.g. auto-accept edits vs. ask every time).
- `/init` is **not** needed: `CLAUDE.md` already exists.
- Run the dev server in a *second* terminal tab, so Claude and the server don't share one.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `permission denied ... docker.sock` | Group change not applied | Log out/in, or `newgrp docker` |
| `docker compose up` fails: port 5432 in use | A system Postgres is running | `sudo systemctl stop postgresql` (and `disable` it) |
| `uv: command not found` | Shell not reloaded | `source ~/.bashrc` or open a new terminal |
| `nvidia-smi` not found / fails | Driver not loaded (often Secure Boot) | Redo step 3, enroll MOK |
| Ollama very slow | Running on CPU | Check `nvidia-smi` while it generates |
