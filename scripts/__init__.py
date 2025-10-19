from .__imports import *
import os as _os

# create dirs (output, data, templates) if not exists
_os.makedirs("output", exist_ok=True)
_os.makedirs("data", exist_ok=True)
_os.makedirs("templates", exist_ok=True)
