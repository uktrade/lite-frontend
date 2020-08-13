import os

PORT = os.environ.get("PORT", 8080)
bind = "0.0.0.0:{PORT}".format(PORT=PORT)
workers = 4
worker_connections = 1000
# timeout affect document uploads
# if timeout is set to be too low, documents that would successfully upload will fail.
# creating a 502 bad gateway error
timeout = 600
