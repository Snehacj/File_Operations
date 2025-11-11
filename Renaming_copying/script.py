import argparse
import os
import shutil
from loguru import logger

def copying(source,output):
    logger.add("copy.log",rotation="1 MB")
    logger.info(f"Input folder : {source}")

    if not os.path.exists(output):
        os.makedirs(output)
    processed=0
    skipped=0

    try:
        for root,dirs,files in os.walk(source):
            for file in files:
                if file.endswith(".csv"):
                    try:
                        file_path=os.path.join(root,file)
                        renamed="filename_"+file
                        new_path=os.path.join(output,renamed)
                        logger.info(f"File renamed successfully")
                        if os.path.exists(new_path):
                            skipped +=1
                            logger.info(f"File already exists so skipped")
                            continue

                        shutil.copy(file_path,new_path)
                        processed +=1
                        logger.info(f"File copied successfully")


                    except Exception as e:
                        logger.info(f"Error copying file: {e}")
        
    except Exception as e:
        logger.info(f"Error in function")
        
    logger.info(f"Total number of files processed : {processed}")
    logger.info(f"Total files skipped : {skipped}")
    logger.info(f"Copying successfull")


source_dir= r".\files"
des_dir=r".\output"
copying(source_dir,des_dir)

