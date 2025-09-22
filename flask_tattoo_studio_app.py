
import os
import io
import tempfile
from datetime import datetime
from flask import Flask, request, render_template, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tattoo_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuração do env

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
FROM_EMAIL = os.getenv('FROM_EMAIL')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Banco de dados
class ClientRequest(db.Model):
    __tablename__ = 'client_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    tattoo = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'tattoo': self.tattoo,
            'created_at': self.created_at,
        }

# Criando tabelas
with app.app_context():
    db.create_all()

# Tatuagens
TATTOOS = [
    {'id': 't1', 'label': 'Rosa Tradicional', 'file': 't1.jpg'},
    {'id': 't2', 'label': 'Caveira Geométrica', 'file': 't2.jpg'},
    {'id': 't3', 'label': 'Águia Tribal', 'file': 't3.jpg'},
    {'id': 't4', 'label': 'Mandala', 'file': 't4.jpg'},
]

# Rota
@app.route('/')
def index():

    return render_template('pagina.html', tattoos=TATTOOS)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    tattoo = (data.get('tattoo') or '').strip()

    if not name or not email or not tattoo:
        return jsonify({'error': 'Nome, e-mail e escolha da tatuagem são obrigatórios.'}), 400

    req = ClientRequest(name=name, email=email, phone=phone, tattoo=tattoo)
    db.session.add(req)
    db.session.commit()

    df = pd.DataFrame([{
        'Nome': name,
        'E-mail': email,
        'Telefone': phone,
        'Tatuagem': tattoo,
        'Enviado em': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    }])

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    df.to_excel(tmp_path, index=False)

    try:
        send_email_with_attachment(
            to_email=ADMIN_EMAIL,
            subject='Novo pedido de tatuagem - {}'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
            body='Segue em anexo os dados do novo pedido de tatuagem.',
            attachment_path=tmp_path
        )
    except Exception as e:
        return jsonify({'error': f'Erro ao enviar e-mail: {e}'}), 500
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    return jsonify({'ok': True})

#  Função email SendGrid
def send_email_with_attachment(to_email, subject, body, attachment_path):
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode()

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    attachment = Attachment(
        FileContent(encoded_file),
        FileName(os.path.basename(attachment_path)),
        FileType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
        Disposition('attachment')
    )
    message.attachment = attachment

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)