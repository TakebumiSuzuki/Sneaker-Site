import os
from flask import Flask, render_template, send_from_directory
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
    # origins = ["http://localhost:5173", ]
    # CORS(app, origins=origins, supports_credentials=True)

    register_error_handlers(app)
    app.register_blueprint(sneakers_bp)
    app.register_blueprint(users_bp)


    # --- Faviconを返すためのルート ---
    @app.route('/favicon.ico')
    def favicon():
        # app.root_path は 'backend' フォルダを指すため、このコードで正しく動作します
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # --- Vueフロントエンドを配信するためのキャッチオールルート ---
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        # APIブループリントで定義されたルート以外のすべてのリクエストをここで捕捉し、
        # Vueアプリの起点となる index.html を返します。
        # (このコードは前の回答と同じですが、Flaskインスタンスの生成方法がシンプルになったことで
        #  正しく 'backend/templates/index.html' を参照します)
        return render_template("index.html")


    return app