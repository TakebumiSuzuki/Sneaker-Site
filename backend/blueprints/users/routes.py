from functools import wraps
from uuid import UUID
from datetime import datetime, timezone
import time

from flask import Blueprint, jsonify, request, url_for, current_app, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,get_jwt, set_refresh_cookies, unset_jwt_cookies
from sqlalchemy import or_, select

from backend.extensions import db, jwt
from backend.models.user import User, TokenBlocklist
from backend.schemas.user import CreateUser, ReadUser, ChangeUsernameUser, ChangePasswordUser, LoginUser
from backend.decorators import require_same_user


users_bp =Blueprint('users', __name__, url_prefix='/api/users')

# 使っていない本来admin用のエンドポイント
# @users_bp.get('/all')
# def get_users():
#     stmt = select(User)
#     users = db.session.execute(stmt).scalars().all()
#     data = [ ReadUser.model_validate(user).model_dump() for user in users]
#     return jsonify(data), 200


@users_bp.get('/<string:user_id>')
@jwt_required()
@require_same_user
def get_user(user_id: str):
    user_id_uuid = UUID(user_id)
    user = db.get_or_404(User, user_id_uuid)
    data = ReadUser.model_validate(user).model_dump()
    return jsonify(data), 200


@users_bp.post('/')
def create_user():

    time.sleep(1)

    data = request.get_json()
    dto = CreateUser.model_validate(data)

    stmt = db.select(User).where(
        or_(User.username == dto.username, User.email == dto.email)
    )
    # .scalar_one_or_none() は、結果が1つもない場合はNone、1つだけの場合はそのオブジェクトを返す
    # 複数見つかった場合はエラーになるため、unique制約のあるカラムのチェックに最適
    existing_user = db.session.execute(stmt).scalar_one_or_none()

    if existing_user:
        return jsonify({"message": "Username or email already exists", "error_code":"RESOURCE_ALREADY_EXISTS"}), 409

    password_hash = User.create_password_hash(dto.raw_password)
    user = User(username=dto.username, email=dto.email, password=password_hash)

    db.session.add(user)
    db.session.commit()
    output = ReadUser.model_validate(user).model_dump()

    # ここでuser.idはUUID型になるので、str(user.id)としないといけないのでは？
    location = url_for('users.get_user', user_id=user.id, _external=True)

    return jsonify(output), 201, {'Location': location}


@users_bp.patch('/<string:user_id>/username')
@jwt_required()
@require_same_user
def change_username(user_id: str):

    time.sleep(1)

    user_id_uuid = UUID(user_id)
    user = db.get_or_404(User, user_id_uuid)
    data = request.get_json()
    dto = ChangeUsernameUser.model_validate(data)

    # 変更後のユーザー名が、自分以外のユーザーに使われていないかチェック
    # Usernameが既に存在するかチェック
    stmt = db.select(User).where(User.username == dto.username, User.id != user_id_uuid)
    existing_user = db.session.execute(stmt).scalar_one_or_none()

    if existing_user:
        return jsonify({"message": "Username already exists", "error_code":"USERNAME_ALREADY_EXISTS"}), 409

    user.username = dto.username
    db.session.commit()
    output = ReadUser.model_validate(user).model_dump()

    return jsonify({'user_data': output}), 200


@users_bp.patch('/<string:user_id>/password')
@jwt_required()
@require_same_user
def change_password(user_id: str):

    time.sleep(1)

    user_id_uuid = UUID(user_id)

    data = request.get_json()
    dto = ChangePasswordUser.model_validate(data)

    user = db.get_or_404(User, user_id_uuid)
    if not user.check_password(dto.old_raw_password):
        return jsonify({"message": "Old password is not correct", "error_code":"INVALID_CREDENTIALS"}), 400
    password_hash = User.create_password_hash(dto.new_raw_password)
    user.password = password_hash

    current_app.logger.info('Userテーブルのtokens_valid_fromを書き換えています')
    # tokens_valid_from は、「この時刻以降に発行された JWT トークンのみ有効とする」ためのタイムスタンプ。
    user.tokens_valid_from = datetime.now(timezone.utc)

    db.session.commit()

    # ボディなし 204 を返しつつ、JWT クッキーを削除
    response = make_response('', 204)
    unset_jwt_cookies(response)
    current_app.logger.info('cookieの中にあるリフレッシュトークンが削除されます')

    return response


@users_bp.delete('/<string:user_id>')
@jwt_required()
@require_same_user
def delete_user(user_id: str):

    time.sleep(1)

    user_id_uuid = UUID(user_id)
    user = db.get_or_404(User, user_id_uuid)
    db.session.delete(user)
    db.session.commit()

    # ボディなし 204 を返しつつ、JWT クッキーを削除
    response = make_response('', 204)
    unset_jwt_cookies(response)
    return response


@users_bp.post('/login')
def login_user():

    time.sleep(1)

    data = request.get_json()
    dto = LoginUser.model_validate(data)
    stmt = select(User).where(User.email == dto.email)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user or not user.check_password(dto.raw_password):
        return jsonify({"message": "Invalid email or password", "error_code": "INVALID_CREDENTIALS"}), 401

    user_data = ReadUser.model_validate(user).model_dump()
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    response = jsonify({
        "user_data": user_data,
        "access_token": access_token,
    })

    set_refresh_cookies(response, refresh_token)

    return response, 200

# ログアウト以外でも、TokenBlocklistに書き込まないといけないケースがあるんじゃないの？例えばpasswrod changeやdelete userの場合。

# ログアウト。クライアント側はアクセストークン、リフレッシュトークン両方を削除する必要がある。
@users_bp.post('/logout')
@jwt_required(refresh=True)
def logout():

    time.sleep(1)

    jti = get_jwt()["jti"]
    current_app.logger.info('古いトークンをブロックリストに入れます')
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    response = jsonify({"message": "Successfully logged out."})
    unset_jwt_cookies(response)
    current_app.logger.info('古いトークンがcookieから削除されます')
    return response, 200


@users_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    old_token_payload = get_jwt()
    old_jti = old_token_payload["jti"]
    current_app.logger.info('古いトークンをブロックリストに入れます')
    db.session.add(TokenBlocklist(jti=old_jti))
    db.session.commit()

    identity = UUID(get_jwt_identity())

    user = db.session.get(User, identity)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = ReadUser.model_validate(user).model_dump()

    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    response_body = { "access_token": access_token, "user_data": user_data }

    response = jsonify(response_body)

    # app.configの設定を自動で読み取ってくれる
    set_refresh_cookies(response, refresh_token)
    current_app.logger.info('新しいaccessTokenがresponse bodyに渡され、新しrefreshTokenがcookieにセットされます。')

    return response, 200


# JWT_USER_LOOKUP = True の設定により、保護されたエンドポイントへのアクセスのたびに自動で呼ばれます。
# ここで返されたオブジェクトは get_current_user() で取得できます。
# 役割：見つかればオブジェクトを、見つからなければNoneを返す
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"] # get_jwt_identity()よりこちらが推奨。なぜなら引数として既にjwt_dataをもらっているから。
    # 404を発生させず、見つからなければNoneを返す
    user = db.session.get(User, UUID(identity)) #同期的に動く
    current_app.logger.info('ユーザーデータが付与されました。get_current_user()で取得できますが、Noneの可能性もあります。')
    return user


# @jwt_required() や @jwt_optional()、@jwt_refresh_token_required() など、JWT 検証を行うデコレーターが付いたすべての
# エンドポイントのリクエスト時にトークンの妥当性（有効期限やブロックリスト登録の有無など）をチェックする過程で必ず呼び出されます。
# 名前に「blocklist」とありますが、中身は「このトークンは OK／NG？」の判定機能です。ブロックリスト判定に限らず、
# ここで任意の“無効化条件”を実装できると考えて差し支えありません。
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    current_app.logger.info('Tokenがブロックリストに含まれていないかチェックしています。')
    stmt = select(TokenBlocklist).where(TokenBlocklist.jti == jti)
    token_in_blocklist = db.session.execute(stmt).scalar_one_or_none()
    if token_in_blocklist is not None:
        return True # ブロックリストにあれば無効

    # ユーザーモデルに問い合わせて、tokens_valid_fromで照合
    user_id = jwt_payload["sub"]
    user = db.session.get(User, UUID(user_id))
    current_app.logger.info('Tokenに記述されているユーザーが存在するかチェックしています。')
    if not user:
        return True # ユーザーが存在しない場合、そのトークンは無効
    current_app.logger.info('Tokenが妥当な発行日なのかチェックしています')
    # トークンの発行日時(iat)を取得
    token_issued_at = datetime.fromtimestamp(jwt_payload["iat"], tz=timezone.utc)

    # トークンの発行日時が、ユーザーに設定された有効日時より古い場合は無効
    tokens_valid_from_aware = user.tokens_valid_from.replace(tzinfo=timezone.utc)
    if token_issued_at < tokens_valid_from_aware:

        return True # トークンは古いので無効

    return False # トークンは有効

