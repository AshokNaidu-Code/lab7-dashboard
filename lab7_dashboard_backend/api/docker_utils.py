import subprocess
import shutil
import os
from lab7_dashboard_backend.utils.build_log import add_build_entry

# Resolve Docker CLI path
DOCKER_CLI = shutil.which("docker")

if not DOCKER_CLI or not os.path.exists(DOCKER_CLI):
    raise FileNotFoundError("🚫 Docker CLI not found in PATH. Is Docker Desktop installed and running?")

import shutil
import os

def run_docker(args):
    full_cmd = [DOCKER_CLI] + args
    print("🐳 Running:", full_cmd)
    try:
        return subprocess.run(full_cmd, capture_output=True, text=True)
    except FileNotFoundError as e:
        print("❌ Docker CLI not found:", e)
        return subprocess.CompletedProcess(full_cmd, 1, "", str(e))
    except Exception as e:
        print("🔥 Unexpected error in run_docker:", e)
        return subprocess.CompletedProcess(full_cmd, 1, "", str(e))

def ensure_docker_exists():
    docker_path = shutil.which("docker")
    if not docker_path or not os.path.exists(docker_path):
        raise FileNotFoundError("🚫 Docker CLI not found in PATH.")



def list_running_containers():
    """List all active Docker containers."""
    try:
        result = run_docker(["ps", "--format", "{{.ID}}:::{{.Image}}:::{{.Status}}"])
        lines = result.stdout.strip().split("\n")
        containers = []

        for line in lines:
            parts = line.split(":::")
            if len(parts) == 3:
                containers.append({
                    "id": parts[0],
                    "image": parts[1],
                    "status": parts[2]
                })

        return {"containers": containers}
    except Exception as e:
        return {"error": str(e), "containers": []}
    
def stop_containers_by_image(image: str):
    """Stop all running containers built from a specific image."""
    image = image.strip()
    print("📦 Received image:", repr(image))  # Debug log

    result = run_docker(["ps", "-q", "--filter", f"ancestor={image}"])
    print("🐳 Docker ps output:", repr(result.stdout))  # Debug log

    if result.returncode != 0:
        msg = f"❌ Error checking containers: {result.stderr.strip()}"
        add_build_entry("error", msg)
        return {"status": "error", "message": msg}

    container_ids = result.stdout.strip().splitlines()
    if not container_ids:
        msg = f"🟡 No running containers found for image: {image}"
        add_build_entry("warning", msg)
        return {"status": "warning", "message": msg}

    logs = []
    all_success = True
    for cid in container_ids:
        stop = run_docker(["stop", cid])
        if stop.returncode == 0:
            logs.append(f"🛑 Stopped container {cid}")
        else:
            logs.append(f"❌ Failed to stop {cid}: {stop.stderr.strip()}")
            all_success = False

    final_msg = "\n".join(logs)
    status = "success" if all_success else "error"
    add_build_entry(status, final_msg)
    return {"status": status, "message": final_msg}