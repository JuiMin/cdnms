import os

# First load ENV Variables
HOSTSERVER = os.getenv("HOSTSERVER", "localhost")
PORT = os.getenv("PORT", 443)

# Constructed constants
_transfer_protocol = "http" if HOSTSERVER == "localhost" else "https"
API_BASE = f"{_transfer_protocol}://{HOSTSERVER}:{PORT}/"
