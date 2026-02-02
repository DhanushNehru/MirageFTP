import asyncio
import random
import config
from logger import logger
from filesystem import MirageFilesystem

class DataChannel:
    def __init__(self):
        self.server = None
        self.reader = None
        self.writer = None
        self.host = None
        self.port = None
        self.connected = asyncio.Event()

    async def start_pasv(self):
        # Bind to a random port
        self.server = await asyncio.start_server(
            self.handle_client, '0.0.0.0', 0
        )
        addr = self.server.sockets[0].getsockname()
        self.port = addr[1]
        self.host = config.HOST
        return self.host, self.port

    async def handle_client(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.connected.set()

    async def send_data(self, data):
        # Wait for client to connect to the data port
        try:
            await asyncio.wait_for(self.connected.wait(), timeout=10.0)
            if self.writer:
                self.writer.write(data)
                await self.writer.drain()
                self.writer.close()
                await self.writer.wait_closed()
        except asyncio.TimeoutError:
            logger.info("Data channel timeout")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.server:
            self.server.close()
        self.connected.clear()
        self.writer = None
        self.reader = None

class MirageProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.fs = MirageFilesystem()
        self.data_channel = DataChannel()
        self.user = None
        self.current_dir = "/"
        self.client_ip = None

    def connection_made(self, transport):
        self.transport = transport
        self.client_ip = transport.get_extra_info('peername')[0]
        logger.info("New connection", extra={"client_ip": self.client_ip})
        self.send_response(config.BANNER)

    def data_received(self, data):
        message = data.decode('utf-8', errors='ignore').strip()
        if not message:
            return

        parts = message.split(' ', 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        logger.info(f"Command received: {cmd} {arg}", extra={"client_ip": self.client_ip, "command": cmd, "user": self.user})

        asyncio.create_task(self.handle_command(cmd, arg))

    async def handle_command(self, cmd, arg):
        # Tarpit delay
        delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)
        await asyncio.sleep(delay)

        if cmd == "USER":
            self.user = arg
            self.send_response("331 Password required for " + arg)
        elif cmd == "PASS":
            # Always accept
            self.send_response("230 User logged in")
            logger.info(f"Login successful", extra={"client_ip": self.client_ip, "user": self.user, "pass": arg})
        elif cmd == "SYST":
            self.send_response("215 UNIX Type: L8")
        elif cmd == "PWD":
            self.send_response(f'257 "{self.current_dir}" is the current directory')
        elif cmd == "CWD":
            # Always succeed and "change" directory
            if arg == "..":
                # simplistic approach to parent
                self.current_dir = "/" # Reset to root for simplicity or handle path parsing
            else:
                if not arg.startswith("/"):
                    self.current_dir = f"{self.current_dir}/{arg}".replace("//", "/")
                else:
                    self.current_dir = arg
            self.send_response("250 CWD command successful")
        elif cmd == "TYPE":
            self.send_response("200 Type set to " + arg)
        elif cmd == "PASV":
            host, port = await self.data_channel.start_pasv()
            # Format IP and port for PASV response: h1,h2,h3,h4,p1,p2
            # host is 0.0.0.0, we need the actual IP or just assume 127.0.0.1 for local testing,
            # or better, use the socket info.
            # For this honeypot specific case, we'll try to use the server's local ip or 127.0.0.1
            ip_parts = "127,0,0,1".split('.') # Defaulting to localhost for safety/simplicity in this env
            if hasattr(config, "HOST") and config.HOST != "0.0.0.0":
                 ip_parts = config.HOST.replace('.', ',')

            p1 = port // 256
            p2 = port % 256
            self.send_response(f"227 Entering Passive Mode ({','.join(ip_parts)},{p1},{p2}).")
        elif cmd == "LIST" or cmd == "NLST":
            self.send_response("150 Opening ASCII mode data connection for file list")
            listing = self.fs.generate_listing(self.current_dir)
            await self.data_channel.send_data(listing.encode('utf-8'))
            self.send_response("226 Transfer complete")
        elif cmd == "RETR":
             self.send_response("150 Opening BINARY mode data connection")
             content = self.fs.get_file_content(arg)
             await self.data_channel.send_data(content)
             self.send_response("226 Transfer complete")
        elif cmd == "QUIT":
            self.send_response("221 Goodbye.")
            self.transport.close()
        else:
            self.send_response("500 Unknown command")

    def send_response(self, message):
        if not message.endswith("\r\n"):
            message += "\r\n"
        self.transport.write(message.encode('utf-8'))
