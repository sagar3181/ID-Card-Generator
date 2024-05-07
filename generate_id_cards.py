from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import csv
import os

ID_WIDTH, ID_HEIGHT = 85.60 * 2.83465, 53.98 * 2.83465
template_path = 'ute_id_template.png'
csv_path = "employee_data.csv"
output_pdf_path = 'employee_id_cards.pdf'
font_path = 'Helvetica-Bold.ttf'

def draw_id_card(template_path, photo_path, name, title):
    template_image = Image.open(template_path)
    try:
        photo_image = Image.open(photo_path)
    except Exception as e:
        print(f"Error opening photo image: {e}")
        return None
    photo_image = photo_image.resize((100, 100))  
    template_image.paste(photo_image, (185, 30))
    draw = ImageDraw.Draw(template_image)
    font_size_name = 20
    font_size_title = 15
    try:
        font = ImageFont.truetype(font_path, font_size_name)
    except OSError:
        print(f"Font file not found at {font_path}. Using default font.")
        font = ImageFont.load_default()
    draw.text((10, 165), name, font=font, fill=(0, 0, 0))
    try:
        font = ImageFont.truetype(font_path, font_size_title)
    except OSError:
        print(f"Font file not found at {font_path}. Using default font.")
        font = ImageFont.load_default()
    draw.text((180, 185), title, font=font, fill=(0, 0, 0))  
    return template_image

output_directory = 'Output_Images'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

c = canvas.Canvas(output_pdf_path, pagesize=(ID_WIDTH, ID_HEIGHT))
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        photo_filename = os.path.basename(row['Photo_name'])
        photo_path = f'Images/{photo_filename}'  
        id_image = draw_id_card(template_path, photo_path, row['Name '], row['Title'])
        if id_image is not None:
            id_image_path = os.path.join(output_directory, f'{photo_filename}.png')
            id_image.save(id_image_path)
            c.drawImage(id_image_path, 0, 0, width=ID_WIDTH, height=ID_HEIGHT)
            c.showPage()
c.save()
