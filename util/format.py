import subprocess


def format():
    subprocess.run(["uv", "run", "ruff", "check", "."], check=True)
    subprocess.run(["uv", "run", "ruff", "format", "--check", "."], check=True)
