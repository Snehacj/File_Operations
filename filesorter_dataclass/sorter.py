import os
import shutil
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class FileSorterConfig:
    categories: dict
    ext_map: dict = field(init=False)

    def __post_init__(self):
        mapping = {}
        for category, extensions in self.categories.items():
            for ext in extensions.split(","):
                ext = ext.strip().lower()
                mapping[ext] = category
        self.ext_map = mapping


class FileSorter:
    def __init__(self, config: FileSorterConfig):
        self.config = config

    def sort_files(self, source: str, destination: str):
        try:
            if not os.path.exists(source):
                logger.error("Source folder not found")
                return

            if not os.path.exists(destination):
                os.makedirs(destination)
                logger.info("Destination folder created")

            files = [
                f for f in os.listdir(source)
                if os.path.isfile(os.path.join(source, f))
            ]

            moved = skipped = errors = 0

            for file in files:
                try:
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()

                    category = self.config.ext_map.get(ext, "Others")
                    target_folder = os.path.join(destination, category)
                    os.makedirs(target_folder, exist_ok=True)

                    src = os.path.join(source, file)
                    dst = os.path.join(target_folder, file)

                    if os.path.exists(dst):
                        logger.warning(f"Skipped existing file: {file}")
                        skipped += 1
                        continue

                    shutil.move(src, dst)
                    logger.info(f"Moved {file} → {category}")
                    moved += 1

                except Exception as e:
                    logger.error(f"Error moving {file}: {e}")
                    errors += 1

            logger.success(
                f"Sorting completed: moved={moved}, skipped={skipped}, errors={errors}"
            )

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
