import os

settings = {}

# Import from environment
for key, val in os.environ.items():
    if key[:6] == "URSAR_":
        settings[key[6:]] = val

# Import from config file