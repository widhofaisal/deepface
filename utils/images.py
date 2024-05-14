import base64
from PIL import Image
import io
import os


def base64_to_jpg(base64_string, output_filename, output_directory):
   # Dekoder base64
    image_bytes = base64.b64decode(base64_string)

    # Buat objek Image dari data gambar
    image = Image.open(io.BytesIO(image_bytes))

    # Pastikan direktori sudah ada
    os.makedirs(output_directory, exist_ok=True)

    # Gabungkan jalur lengkap dengan nama file
    output_path = os.path.join(output_directory, output_filename)

    # Simpan gambar sebagai file .jpg
    image.save(output_path)


def image_to_base64(image_path):
    try:
        # Open the image file
        with open(image_path, "rb") as image_file:
            # Read the image file content
            image_content = image_file.read()

            # Encode the image content as base64
            base64_encoded = base64.b64encode(image_content).decode('utf-8')

            return base64_encoded

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def delete_image_file(filename):
    images_directory = "images"
    file_path = os.path.join(images_directory, filename)

    try:
        os.remove(file_path)
        print(f"File '{filename}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred while deleting '{filename}': {e}")
