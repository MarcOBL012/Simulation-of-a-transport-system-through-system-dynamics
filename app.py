import ssl
import mysql.connector
from flask import Flask

from src.Routes.route import modelRoute

from pyngrok import ngrok

ssl._create_default_https_context = ssl._create_unverified_context
ngrok.set_auth_token('35Rw5XJhEjlSdbyQf3aIuzIP13b_bHGZBYah2RPvQq7GCrFc')
app = Flask(__name__)
modelRoute(app)

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    # Obtener la URL pública generada por Ngrok
    public_url_str = str(public_url)
    print('URL pública de Ngrok:', public_url_str)
    app.run()



'''if __name__ == "__main__":
    app.run('0.0.0.0',port=5000)'''






