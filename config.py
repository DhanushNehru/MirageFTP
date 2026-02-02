# Configuration for MirageFTP

HOST = "0.0.0.0"
PORT = 2121

# Banner to display on connection
BANNER = "220 ProFTPD 1.3.5 Server (MirageFTP) [::ffff:127.0.0.1]"

# Tarpit settings (in seconds)
MIN_DELAY = 0.5
MAX_DELAY = 2.0

# Filesystem settings
MAX_DEPTH = 10  # Max depth to allow "cd" before resetting or looping
