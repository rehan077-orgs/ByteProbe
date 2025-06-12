import pytsk3
import os

# Disk image path
image_path = r"B:\disk_image_E.img"
output_dir = r"C:\Users\rehan\Desktop\ByteProbe\arved_files"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Common file signatures
SIGNATURES = {
    "jpg": {
        "header": b'\xff\xd8\xff',  # JPEG start
        "footer": b'\xff\xd9',       # JPEG end
    },
    "pdf": {
        "header": b'%PDF-',          # PDF start
        "footer": b'%%EOF',          # PDF end (may appear multiple times, take last)
    }
    # Add more file types here if needed
}

def carve_files(img, start_offset=0, chunk_size=1024*1024*10):
    """
    Carve files from raw image data based on signatures.
    :param img: pytsk3 Img_Info object
    :param start_offset: offset in bytes to start carving
    :param chunk_size: how many bytes to read per iteration
    """
    img_size = img.get_size()
    print(f"Disk image size: {img_size / (1024*1024):.2f} MB")

    with open(image_path, 'rb') as f:
        f.seek(start_offset)
        data = f.read(chunk_size)

        for filetype, sig in SIGNATURES.items():
            header = sig['header']
            footer = sig['footer']

            start = 0
            while True:
                # Find header
                header_pos = data.find(header, start)
                if header_pos == -1:
                    break

                # Find footer after header_pos
                footer_pos = data.find(footer, header_pos)
                if footer_pos == -1:
                    break

                # For PDFs, footer might have multiple, so find the last one within chunk
                if filetype == "pdf":
                    while True:
                        next_footer = data.find(footer, footer_pos + 1)
                        if next_footer == -1:
                            break
                        footer_pos = next_footer

                file_data = data[header_pos:footer_pos + len(footer)]

                # Save carved file
                output_path = os.path.join(output_dir, f"carved_{filetype}_{header_pos}.{'jpg' if filetype == 'jpg' else 'pdf'}")
                with open(output_path, 'wb') as out_file:
                    out_file.write(file_data)
                print(f"Carved {filetype.upper()} file saved at offset {header_pos}: {output_path}")

                start = footer_pos + len(footer)

if __name__ == "__main__":
    img = pytsk3.Img_Info(image_path)
    carve_files(img)
