#Definición de las librerías que se usarán
from flask import Flask, request
import json
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Creamos objeto Flask y creará nuestros servicios web
app = Flask(__name__)

#Cargamos la informacion de nuestro archivo config.json, con open se abre el archivo "config.json" y con "json.loads" se lee el archivo
f = open("config.json", "r") 
env = json.loads(f.read())

#Creamos nuestro primer servicio web (Con esta instrución es como se crea un servicio web en Python)
@app.route('/test', methods=['GET'])
def test():
    return "hello world"

#Envio del SMS  
@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        #Capturo las variables de la configuración
        account_sid = env['TWILIO_ACCOUNT_SID']
        auth_token = env['TWILIO_AUTH_TOKEN']
        origen = env['TWILIO_PHONE_NUMBER']
        #Crea el mensaje o notificacón
        client = Client(account_sid, auth_token)
        #Captura la información del envio
        data = request.json
        contenido = data["contenido"]
        destino = data["destino"]
        #Crea el mensaje como tal y se envía
        message = client.messages.create(
                            body=contenido,
                            from_=origen,
                            to='+57' + destino
                        )
        print(message)
        return "send success"
    except Exception as e:
        print(e)
        return "error"

#Envio de e-mail
@app.route('/send_email', methods=['POST'])
def send_email():
    #Capturar la info de la solicitud
    data = request.json
    contenido = data["contenido"]
    destino = data["destino"]
    asunto = data["asunto"]
    print(contenido, destino, asunto)
    #Creo el mensaje de correo electronico
    message = Mail(
    from_email= env['SENDGRID_FROM_EMAIL'],
    to_emails= destino,
    subject= asunto,
    html_content= contenido)
    try:
        sg = SendGridAPIClient(env['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "send success"
    except Exception as e:
        print(e)
        return "error"


#Ejecutamos el servidor
if __name__ == '__main__':
    app.run()
