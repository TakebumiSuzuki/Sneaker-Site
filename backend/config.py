from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    # Flask本体および多くの拡張機能が（セッションの署名、CSRF トークン生成など）で利用する設定キー
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Flask-SQLAlchemy拡張が読み取って動作を制御するための設定キー
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-jwt-extended が内部で参照する設定キー
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_USER_LOOKUP = True # デフォルトでFalse
    JWT_BLOCKLIST_ENABLED = True # デフォルトでFalse
    JWT_BLOCKLIST_TOKEN_CHECKS = ["refresh"]

    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_CSRF_PROTECT = False # CSRF保護はユースケースによる。REST APIではFalseが多い

    # 本番環境ではTrueに設定し、HTTPS通信でのみクッキーが送信されるようにする
    # JWT_COOKIE_SECURE = app.config["ENV"] == "production"

    # クッキーのSameSite属性。CSRF対策に重要。'Strict'が最も安全。
    JWT_COOKIE_SAMESITE = "Lax"

    # リフレッシュトークンのクッキー名（デフォルトは'refresh_token_cookie'）
    # JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"

    # リフレッシュトークンのクッキーが有効なパス
    # APIのエンドポイント（例: /api/users/refresh）に限定するのがセキュア
    # JWT_REFRESH_COOKIE_PATH = "/api/users"



    # 特にパッケージに依存しないキー
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    # Werkzeugが、内部的に受信リクエストボディの最大バイト数をチェックするための設定キー
    # これを超えたリクエストで自動的に RequestEntityTooLarge（HTTP 413）が発生
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024




class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass