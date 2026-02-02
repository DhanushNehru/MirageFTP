import asyncio
import config
from server import MirageProtocol
from logger import logger

async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: MirageProtocol(),
        config.HOST, config.PORT
    )

    logger.info(f"MirageFTP started on {config.HOST}:{config.PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopping...")
