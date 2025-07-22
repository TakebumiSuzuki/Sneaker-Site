from flask import Flask
from backend.config import DevelopmentConfig, ProductionConfig
from backend.extensions import db, migrate, jwt
from backend.blueprints.sneakers.routes import sneakers_bp
from backend.blueprints.users.routes import users_bp
from backend.errors import register_error_handlers
from flask_cors import CORS


def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORSにより、クロスオリジンでの通信ができるようになるとともに、origins=origins, supports_credentials=True
    # の設定により、cookieもやりとりできるようなる。フロント側ではaxiosのリクエストに{withCredentials: true}を含める　
    origins = ["http://localhost:5173", ]
    CORS(app, origins=origins, supports_credentials=True)

    register_error_handlers(app)
    app.register_blueprint(sneakers_bp)
    app.register_blueprint(users_bp)


    return app