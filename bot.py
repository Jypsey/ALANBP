import os, glob, datetime, asyncio, logging
import logging.config
from pyrogram import Client

APP_ID = "10001717"
API_HASH = "c8cdc2079f7ab083e644381740260265"
BOT_TOKEN = "7303948858:AAFN5mUdrhn2DhWFkRAMUaCPAl5hrCD98bg"    #@Fjgjgkgkbot
DB_URL = [
    "postgresql://JerryBot:J2024@localhost:5432/JerryBot"
]
DB_CHAT_ID = "-1002306074542"
INTERVAL_IN_SEC = "43200"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(module)s][%(lineno)d][%(levelname)s] -> %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def db_backup():
    app = Client(
        name="backupper",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )
    async with app:
        while True:
            for url in DB_URL:
                x = datetime.datetime.now()
                date_time = x.strftime("%d %b %Y | %I:%M %p")
                date = x.strftime("%d-%b-%Y")
                command_to_run = f"pg_dump --dbname={url} > JerryBackup_{date}.sql"
                try:
                    LOGGER.info("Running backup: %s", command_to_run)
                    result = os.system(command_to_run)
                    if result != 0:
                        LOGGER.warning("Backup failed: %s", command_to_run)
                    else:
                        LOGGER.info("Backup completed successfully: %s", command_to_run)
                except Exception as e:
                    LOGGER.error("Error while executing backup: %s", e)

                for db in glob.glob("*.sql"):
                    try:
                        LOGGER.info("Sending file: %s", db)
                        await app.send_document(int(DB_CHAT_ID), db, caption=f'**📌 UP-Date : {date_time}**')
                        os.remove(db)
                        LOGGER.info("File sent and removed: %s", db)
                    except Exception as e:
                        LOGGER.error("Failed to send file %s: %s", db, e)
                        await app.send_message(int(DB_CHAT_ID), str(e))

                LOGGER.info(
                    "Backup process completed. Sleeping for %s seconds",
                    str(INTERVAL_IN_SEC),
                )
                await asyncio.sleep(int(INTERVAL_IN_SEC))


loop = asyncio.get_event_loop()
loop.run_until_complete(db_backup())