

import pytsk3
import datetime

# Path to your disk image file
image_path = r"D:\disk_image_B.img"

# Open the image using pytsk3
img = pytsk3.Img_Info(image_path)
fs = pytsk3.FS_Info(img)

# Function to extract and print timestamps
def list_file_timestamps(fs_info):
    directory = fs_info.open_dir(path="/")
    for entry in directory:
        if not hasattr(entry, "info") or not entry.info.name:
            continue

        name = entry.info.name.name.decode("utf-8")
        if name in [".", ".."]:
            continue

        meta = entry.info.meta
        if meta:
            print(f"📄 File: {name}")
            print(f"  🕒 Created : {datetime.datetime.fromtimestamp(meta.crtime).isoformat() if meta.crtime else 'N/A'}")
            print(f"  ✏️ Modified: {datetime.datetime.fromtimestamp(meta.mtime).isoformat() if meta.mtime else 'N/A'}")
            print(f"  👁️ Accessed: {datetime.datetime.fromtimestamp(meta.atime).isoformat() if meta.atime else 'N/A'}")
            print("-" * 60)

# Run the function
list_file_timestamps(fs)
