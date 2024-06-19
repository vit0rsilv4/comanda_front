import base64
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from passlib.context import CryptContext
import tempfile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Funcoes(object):
    @staticmethod
    def verify_password(plain_password, password):
        return pwd_context.verify(plain_password, password)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_pdf(filename, title, data, fields):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2.0, height - 50, title)

        c.setFont("Helvetica", 12)
        y_position = height - 100

        for item in data:
            for field in fields:
                if field == 'foto':  # Campo especial para imagem
                    image_data = item.get(field)
                    if image_data:
                        image_data = image_data.split(',')[1]  # Remove o prefixo data:image/jpeg;base64,
                        image = Image.open(BytesIO(base64.b64decode(image_data)))
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
                            image_path = temp.name
                            image.save(image_path)
                        c.drawImage(image_path, 100, y_position - 100, width=100, height=100)
                        y_position -= 120
                else:
                    value = item.get(field, 'Informação não disponível')
                    c.drawString(100, y_position, f"{field.capitalize()}: {value}")
                    y_position -= 20
            
            c.setStrokeColor(colors.red)
            c.line(100, y_position, 500, y_position)
            y_position -= 20

            if y_position < 100:
                c.showPage()
                y_position = height - 100
                c.setFont("Helvetica", 12)

        c.showPage()
        c.save()