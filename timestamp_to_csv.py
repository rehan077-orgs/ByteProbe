import pytsk3
import datetime
import csv

# Set your disk image path
image_path = r"D:\disk_image_B.img"
img = pytsk3.Img_Info(image_path)
fs = pytsk3.FS_Info(img)


# Output CSV file in ByteProbe folder
csv_file = r"C:\Users\rehan\Desktop\ByteProbe\file_timestamps.csv"


# Recursive function to walk the filesystem and collect file metadata
def walk_dir(directory, path="/", csv_writer=None):
    for entry in directory:
        if entry.info.name.name.decode(errors="ignore") in [".", ".."]:
            continue

        try:
            filepath = f"{path}{entry.info.name.name.decode(errors='ignore')}"
            meta = entry.info.meta

            if meta:
                row = {
                    "File Path": filepath,
                    "Size (Bytes)": meta.size,
                    "Created": datetime.datetime.fromtimestamp(meta.crtime).isoformat() if meta.crtime else "",
                    "Modified": datetime.datetime.fromtimestamp(meta.mtime).isoformat() if meta.mtime else "",
                    "Accessed": datetime.datetime.fromtimestamp(meta.atime).isoformat() if meta.atime else "",
                    "Changed": datetime.datetime.fromtimestamp(meta.ctime).isoformat() if meta.ctime else "",
                }
                csv_writer.writerow(row)

            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entry.as_directory()
                walk_dir(sub_directory, filepath + "/", csv_writer)

        except Exception as e:
            print(f"⚠️ Error reading entry: {e}")

# Create and write CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    fieldnames = ["File Path", "Size (Bytes)", "Created", "Modified", "Accessed", "Changed"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    root_dir = fs.open_dir("/")
    walk_dir(root_dir, "/", writer)

print(f"✅ Done! Timestamp data saved to {csv_file}")
