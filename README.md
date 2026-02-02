# MirageFTP 🌵

> "The files you see are only a mirage."

**MirageFTP** is a high-interaction-style FTP honeypot written in Python. Unlike traditional low-interaction honeypots that serve a static set of files, MirageFTP generates a dynamic, infinite filesystem on the fly. It is designed to waste attackers' time (Tarpit) and collect detailed intelligence on their behavior.

## ✨ Features

- **🌀 Infinite "Mirage" Filesystem**: Attackers can traverse an endless depth of directories. Every directory exists, and every directory contains enticing fake files.
- **🐢 Smart Tarpit**: Every command response is intentionally delayed (randomized between 0.5s - 2.0s). This frustrates manual attackers and breaks the timing of automated brute-force tools.
- **📝 Real Data Channel Support**: Implements a full TCP stack for Passive (PASV) data channels, allowing file listing (`ls`, `dir`) and file retrieval (`get`) to work seamlessly, keeping the illusion alive.
- **🔍 Context-Aware Honeyfiles**: Dynamically generates files like `backup.sql`, `config.php`, `wallet.dat`, and `id_rsa` with consistent timestamps and believable sizes.
- **📊 JSON Telemetry**: Outputs structured JSON logs containing:
  - Source IP & Port
  - Credentials used (User/Pass)
  - Commands executed
  - Session timestamps

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- No external dependencies (Built purely on `asyncio` standard library)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DhanushNehru/MirageFTP.git
   cd MirageFTP
   ```

2. Run the server:
   ```bash
   python3 main.py
   ```

By default, it listens on port **2121**.

### Configuration

Edit `config.py` to customize the behavior:

```python
HOST = "0.0.0.0"       # Bind address
PORT = 2121            # Port to listen on (use 21 for production, requires sudo)
BANNER = "..."         # Custom FTP Banner
MIN_DELAY = 0.5        # Minimum Tarpit delay (seconds)
MAX_DELAY = 2.0        # Maximum Tarpit delay (seconds)
```

## 🐳 Docker Support

You can essentially run MirageFTP anywhere using Docker.

### Using Docker Compose (Recommended)

1. Build and run in the background:
   ```bash
   docker-compose up -d --build
   ```
2. View the logs (live attack stream):
   ```bash
   docker-compose logs -f
   ```
3. Stop the honeypot:
   ```bash
   docker-compose down
   ```

### Using Standard Docker

1. Build the image:
   ```bash
   docker build -t mirageftp .
   ```
2. Run the container:
   ```bash
   docker run -d -p 2121:2121 --name mirage mirageftp
   ```

## 🕹 Usage

Connect using any FTP client (FileZilla, CLI ftp, netcat):

```bash
ftp -P 2121 localhost
```

**Login:** Accepts *any* username and password (and logs them).

## 🛡 Disclaimer

This software is for **educational and research purposes only**. Do not run this on a production network unless you know what you are doing. It is designed to be attacked.

## 📄 License

MIT License
