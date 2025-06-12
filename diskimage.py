import os

def create_disk_image(source_drive, output_path, chunk_size=1024*1024):
    """
    Create a raw disk image from source_drive and save to output_path.
    
    Args:
        source_drive (str): Raw device path (e.g. '\\\\.\\B:')
        output_path (str): File path to save disk image (e.g. 'D:\\disk_image_B.img')
        chunk_size (int): Number of bytes to read at once (default 1MB)
    """
    try:
        with open(source_drive, 'rb') as src, open(output_path, 'wb') as dst:
            print(f"Starting disk image creation from {source_drive}...")
            
            total_bytes = 0
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                dst.write(chunk)
                total_bytes += len(chunk)
                print(f"\rWritten {total_bytes / (1024*1024):.2f} MB", end='')
                
            print("\nDisk image creation completed successfully.")
    except PermissionError:
        print("❌ Permission denied: Run the script as Administrator!")
    except FileNotFoundError:
        print("❌ Source drive not found or inaccessible.")
    except OSError as e:
        print(f"❌ OS error occurred: {e}")

if __name__ == "__main__":
    source_drive = r'\\.\E:'         # Change to your source drive letter
    output_file = r'B:\disk_image_F.img'  # Change to your destination path
    
    # Check free space on destination drive
    dest_drive = os.path.splitdrive(output_file)[0]
    free_space = os.statvfs(dest_drive).f_bavail * os.statvfs(dest_drive).f_frsize if hasattr(os, 'statvfs') else None
    if free_space:
        print(f"Free space on {dest_drive}: {free_space / (1024*1024*1024):.2f} GB")

    create_disk_image(source_drive, output_file)
