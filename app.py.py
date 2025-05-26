from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # (evita erro de CORS)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'barberclick83@gmail.com'
SMTP_PASSWORD = 'egxe lhds yexm qepd'  
EMAIL_BARB = 'flawlexx00@gmail.com'

@app.route('/')
def index():
    return 'API da Barbearia está online'

@app.route('/agendar', methods=['POST'])
def agendar():
    data = request.get_json()

    nome = data.get('nome')
    email_cliente = data.get('emailCliente')
    horario = data.get('horario')

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_BARB
    msg['Subject'] = f'Novo agendamento de {nome}'
    msg.add_header('Reply-To', email_cliente)

    corpo = f"""
    Novo agendamento recebido:

    Nome: {nome}
    Email: {email_cliente}
    Horário: {horario}
    """

    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, EMAIL_BARB, msg.as_string())
        server.quit()
        return jsonify({"mensagem": "Agendamento enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

