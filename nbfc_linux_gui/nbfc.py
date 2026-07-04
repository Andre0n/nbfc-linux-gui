"""Thin wrapper around the nbfc CLI. No GTK here:  pure I/O, unit-testable."""
import subprocess
from subprocess import PIPE


def status():
    """Return parsed `nbfc status --all` as a dict, or None if unavailable."""
    try:
        out = subprocess.run(
            ['nbfc', 'status', '--all'],
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
            ['pkexec', 'nbfc', *args], stdout=PIPE, stderr=PIPE, text=True,
        )
    except OSError as err:
        return str(err)
    if proc.returncode != 0:
        return proc.stderr.strip() or f'nbfc exited {proc.returncode}'
    return None
