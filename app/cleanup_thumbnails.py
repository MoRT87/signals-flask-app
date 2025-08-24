import os
import time

THUMBNAILS_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'thumbnails')
EXPIRE_SECONDS = 10 * 60  # 10 minutos

def cleanup_old_thumbnails():
    now = time.time()
    for fname in os.listdir(THUMBNAILS_DIR):
        fpath = os.path.join(THUMBNAILS_DIR, fname)
        if os.path.isfile(fpath):
            # Extrae timestamp del nombre del archivo
            try:
                ts = int(fname.split('_')[-1].split('.')[0])
            except Exception:
                continue
            if now - ts > EXPIRE_SECONDS:
                os.remove(fpath)

if __name__ == "__main__":
    cleanup_old_thumbnails()