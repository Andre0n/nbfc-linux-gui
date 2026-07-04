"""Thin wrapper around the nbfc CLI. No GTK here:  pure I/O, unit-testable."""
import os
import subprocess
from subprocess import PIPE

# Inside a Flatpak sandbox nbfc/pkexec live on the host, reached via flatpak-spawn.
_HOST = ['flatpak-spawn', '--host'] if os.path.exists('/.flatpak-info') else []


def status():
    """Return parsed `nbfc status --all` as a dict, or None if unavailable."""
    try:
        out = subprocess.run(
            [*_HOST, 'nbfc', 'status', '--all'],
            stdout=PIPE, stderr=PIPE, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None  # nbfc missing or service down

    result = {}
    for line in out.splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            result[key.strip()] = value.strip()
    return result


def apply(args):
    """Run `pkexec nbfc <args>`. Return None on success, else an error string."""
    try:
        proc = subprocess.run(
            [*_HOST, 'pkexec', 'nbfc', *args], stdout=PIPE, stderr=PIPE, text=True,
        )
    except OSError as err:
        return str(err)
    if proc.returncode != 0:
        return proc.stderr.strip() or f'nbfc exited {proc.returncode}'
    return None
