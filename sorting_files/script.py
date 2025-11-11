import os
import shutil
from loguru import logger

def sorting_files(source,img,aud,vid,doc):
    logger.add("sorting.log",rotation="1 MB")
    logger.info(f"input folder : {source}")
    try:
        os.makedirs(img, exist_ok=True)
        os.makedirs(aud, exist_ok=True)
        os.makedirs(vid, exist_ok=True)
        os.makedirs(doc, exist_ok=True)

        for root,dirs,files in os.walk(source):
            for file in files:
                filepath=os.path.join(root,file) 

                if file.endswith((".pdf",".doc",".txt")):
                    newpath=os.path.join(doc,file)
                    shutil.move(filepath,newpath)
                    logger.info(f"Doc file detected and moved in to docs folder")

                elif file.endswith((".jpeg",".png")):
                    newpath=os.path.join(img,file)
                    shutil.move(filepath,newpath)
                    logger.info(f"Image file detected and moved in to images folder")

                elif file.endswith((".mp3",".wav")):
                    newpath=os.path.join(aud,file)
                    shutil.move(filepath,newpath)
                    logger.info(f"Audio file detected and moved in to audio folder")

                elif file.endswith((".mov",".mp4")):
                    newpath=os.path.join(vid,file)
                    shutil.move(filepath,newpath)
                    logger.info(f"Video file detected and moved in to video folder")

        logger.info(f"Sorting completed successfully")

    except Exception as e:
        logger.info(f"Error in sorting: {e}")

source_dir= r"."
img_dir=r".\images"
vid_dir=r".\video"
aud_dir=r".\audio"
doc_dir=r".\docs"


sorting_files(source_dir,img_dir,aud_dir,vid_dir,doc_dir)
                    
                
