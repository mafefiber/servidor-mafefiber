import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db
from blueprints import register_blueprints
from flasgger import Swagger
from swagger_config import swagger_config, template


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PGURL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app,db)
    CORS(app, resources={r"*": {"origins": "*"}})

    register_blueprints(app)
    Swagger(app, config=swagger_config, template=template)

    @app.get("/health")
    def health():
        """
        Verificar el estado del servicio
        ---
        responses:
          200:
            description: Servicio activo
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: ok
        """
        return {"status": "ok"}
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    
    print(f"Swagger UI disponible en: http://{host}:{port}/apidocs")
    app.run(host=host, port=port, debug=debug)

