import os
from PIL import Image, ImageDraw, ImageFont
import shutil

# Fungsi untuk resize gambar
def resize_image(image, size=(800, 600)):
    return image.resize(size, Image.Resampling.LANCZOS)  # Ganti Image.ANTIALIAS dengan Image.Resampling.LANCZOS

# Fungsi untuk menambahkan watermark teks
def add_watermark(image, text="Hak Cipta", position=(0, 0)):
    watermark_image = image.copy()
    draw = ImageDraw.Draw(watermark_image)

    # Load font, jika tidak ada bisa menggunakan default font
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()

    # Ganti textsize dengan textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # Lebar teks
    text_height = text_bbox[3] - text_bbox[1]  # Tinggi teks
    text_position = (image.width - text_width - 10, image.height - text_height - 10)

    draw.text(text_position, text, font=font, fill=(255, 255, 255, 128))  # Warna putih dengan transparansi
    return watermark_image

# Fungsi untuk konversi format dari PNG ke JPG
def convert_to_jpg(image):
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    return image

# Fungsi untuk memproses gambar dari sebuah folder
def process_images(input_folder, output_folder, size=(800, 600)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):  # Hanya proses file PNG
            input_path = os.path.join(input_folder, filename)
            image = Image.open(input_path)

            # Resize gambar
            resized_image = resize_image(image, size)

            # Tambahkan watermark
            watermarked_image = add_watermark(resized_image)

            # Konversi ke JPG
            jpg_image = convert_to_jpg(watermarked_image)

            # Simpan gambar yang telah diolah ke folder output
            output_filename = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(output_folder, output_filename)
            jpg_image.save(output_path, "JPEG", quality=90)

            print(f"Processed and saved {output_filename}")

# Main program
def main():
    input_folder = 'input_images'  # Folder input
    output_folder = 'output_images'  # Folder output

    # Pastikan folder input dan output ada
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"Folder '{input_folder}' dibuat. Tambahkan file PNG di folder ini lalu jalankan ulang script.")
        return

    # Proses gambar
    process_images(input_folder, output_folder)
    print(f"Semua gambar telah diproses dan disimpan di folder '{output_folder}'.")

    # Opsional: Kompres hasil output ke dalam file zip
    shutil.make_archive(output_folder, 'zip', output_folder)
    print(f"File zip output telah dibuat: {output_folder}.zip")

if __name__ == "__main__":
    main()

