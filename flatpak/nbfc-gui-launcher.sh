#!/bin/sh
# Run the package from /app without pip/site-packages version coupling.
export PYTHONPATH="/app/share/nbfc_linux_gui:${PYTHONPATH}"
exec python3 -m nbfc_linux_gui "$@"
