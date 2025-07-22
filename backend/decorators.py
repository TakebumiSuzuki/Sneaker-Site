from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from uuid import UUID
from backend.models.user import User
from backend.extensions import db

def require_same_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Kwargs in require_same_user: {kwargs}") # ここを追加
        user_id = get_jwt_identity()

        user_id_from_url = str(UUID(kwargs.get('user_id')))

        if not user_id_from_url: # このエラーは通常発生しないはずだが、念のため
            return jsonify({"message": "User ID not found in URL", "error_code": "MISSING_URL_PARAMETER"}), 400
        if user_id_from_url != user_id:
            return jsonify({"message": "Forbidden: You are not authorized to perform this action", "error_code": "FORBIDDEN"}), 403
        return fn(*args, **kwargs)
    return wrapper

def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('アドミンデコレータ~')
        user_id = get_jwt_identity()
        user = db.session.get(User, UUID(user_id))
        if not user.is_admin:
            return jsonify({"message": "Forbidden: You are not authorized to perform this action", "error_code": "FORBIDDEN"}), 403
        return fn(*args, **kwargs)
    return wrapper