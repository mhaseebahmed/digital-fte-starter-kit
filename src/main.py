import time
from watchdog.observers import Observer
from src.foundation.logger import setup_logger
from src.foundation.config import settings
from src.watchers.filesystem import RobustHandler

logger = setup_logger("main")

def main():
    logger.info("🚀 Starting Digital FTE (Bronze Tier)...")
    
    # 1. Setup Office
    settings.get_inbox_path().mkdir(parents=True, exist_ok=True)
    settings.get_processing_path().mkdir(parents=True, exist_ok=True)
    settings.get_done_path().mkdir(parents=True, exist_ok=True)

    # 2. Launch Watcher
    observer = Observer()
    handler = RobustHandler()
    observer.schedule(handler, path=str(settings.get_inbox_path()), recursive=False)
    observer.start()
    
    logger.info(f"👀 Watching: {settings.get_inbox_path()}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("🛑 Shutting down...")
    
    observer.join()

if __name__ == "__main__":
    main()
