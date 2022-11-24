from flask import Flask
from decouple import config
from  routes.docente import docente_bp

app = Flask(__name__)


app.register_blueprint(docente_bp)


if __name__ == '__main__':
    app.run(port= config('API_PORT'), debug=True)

          