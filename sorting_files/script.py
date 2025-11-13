import os
import shutil
from loguru import logger
from abc import ABC, abstractmethod


class Filesort(ABC):
    @abstractmethod
    def sort_files(self,source:str,destination:str,config:dict):
        pass

class Sorting(Filesort):
    def sort_files(self,source:str,destination:str,config:dict):
        try:
            if not os.path.exists(source):
                logger.error(f"Source folder not found")
                return
            if not os.path.exists(destination):
                os.makedirs(destination)
                logger.info(f"Created destination folder")
            
            ext_map={}

            for category,extensions in  config.items():
                for ext in extensions.split(","):
                    ext_map[ext.strip().lower()]=category

            all_files=[
                f for f in os.listdir(source)
                if os.path.isfile(os.path.join(source,f))
            ]
            moved,skipped,errors=0,0,0

            for file in all_files:
                try:
                    _,ext=os.path.splitext(file)
                    ext=ext.lower()
                    category=ext_map.get(ext,"Others")
                    target_folder=os.path.join(destination,category)
                    os.makedirs(target_folder,exist_ok=True)

                    src=os.path.join(source,file)
                    dst=os.path.join(target_folder,file)

                    if(os.path.exists(dst)):
                        logger.warning(f"skipped existing file:{file}")
                        skipped +=1
                        continue

                    shutil.move(src,dst)
                    logger.info(f"Moved {file} to {category}")
                    moved +=1

                except Exception as e:
                    logger.error(f"Error moving{file}:{e}")
                    errors+=1

            logger.success(f"sorting complete!!! moved : {moved},skipped : {skipped}, errors : {errors}")
        
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")

