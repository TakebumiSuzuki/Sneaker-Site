import struct
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from PIL import UnidentifiedImageError

from backend.extensions import db, jwt
from backend.models.user import TokenBlocklist
from backend.utils_image import ImageValidationError, FileSystemError

def register_error_handlers(app):
    """Registers custom error handlers for the Flask application."""

    # --- 4xx Client Errors ---

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError):
        """Handles Pydantic's ValidationError (400 Bad Request)."""
        db.session.rollback()
        # Pydantic v2では error.errors() で詳細なエラーリストが取得できる
        current_app.logger.warning(f"Pydantic validation failed: {error.errors()}")
        response = {
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed.",
            "details": error.errors()
        }
        return jsonify(response), 400

    @app.errorhandler(IntegrityError)
    def handle_database_integrity_error(error: IntegrityError):
        """Handles database integrity errors (e.g., duplicate unique keys) (409 Conflict)."""
        db.session.rollback()
        # origは "original exception" の略で、SQLAlchemyが自身のエラー（IntegrityError）を発生させる
        # 起源（きっかけ）となった、下位レイヤー（DBAPIドライバ）の元の例外を指します。
        current_app.logger.error(f"Database integrity error: {error.orig}", exc_info=True)
        response = {
            "error_code": "DATABASE_CONFLICT",
            "message": "The request could not be completed due to a conflict with the current state of the resource. This is often caused by a duplicate unique key."
        }
        return jsonify(response), 409

    @app.errorhandler(NotFound)
    def handle_not_found_error(error: NotFound):
        """Handles resource not found errors (404 Not Found)."""
        db.session.rollback()
        # werkzeug's NotFound has a description attribute.
        message = error.description or "The requested resource was not found."
        current_app.logger.warning(f"Resource not found: {message}")
        response = {
            "error_code": "RESOURCE_NOT_FOUND",
            "message": message
        }
        return jsonify(response), 404

    @app.errorhandler(BadRequest)
    def handle_bad_request_error(error: BadRequest):
        """Handles generic bad requests (400 Bad Request)."""
        db.session.rollback()
        message = error.description or "The request was malformed or invalid."
        current_app.logger.warning(f"Bad request: {message}")
        response = {
            "error_code": "BAD_REQUEST",
            "message": message
        }
        return jsonify(response), 400

    @app.errorhandler(ImageValidationError)
    def handle_image_validation_error(error: ImageValidationError):
        """Handles custom image validation errors (400 Bad Request)."""
        db.session.rollback()
        current_app.logger.warning(f"Image validation failed: {error}")
        return jsonify({
            "error_code": "IMAGE_VALIDATION_ERROR",
            "message": str(error)
        }), 400

    @app.errorhandler(UnidentifiedImageError)
    def handle_unidentified_image_error(error: UnidentifiedImageError):
        """Handles cases where Pillow cannot identify the image format (400 Bad Request)."""
        db.session.rollback()
        current_app.logger.warning(f"Unidentified image error: {error}")
        return jsonify({
            "error_code": "INVALID_IMAGE_FORMAT",
            "message": "The provided file could not be identified as an image."
        }), 400

    # UnidentifiedImageError is a subclass of OSError, so defining this handler after it is intuitive.
    @app.errorhandler(OSError)
    def handle_image_os_error(error: OSError):
        """Handles OS-level errors from Pillow, e.g., reading a corrupted image (400 Bad Request)."""
        db.session.rollback()
        current_app.logger.warning(f"Image processing OSError: {error}")
        return jsonify({
            "error_code": "CORRUPTED_IMAGE_DATA",
            "message": "The image data may be corrupted or in an unsupported format."
        }), 400


    # --- 5xx Server Errors ---

    @app.errorhandler(struct.error)
    def handle_image_struct_error(error: struct.error):
        """Handles low-level errors during image parsing (500 Internal Server Error)."""
        db.session.rollback()
        # This error is best treated as a server-side issue.
        current_app.logger.error(f"Image parsing struct.error: {error}", exc_info=True)
        return jsonify({
            "error_code": "IMAGE_PARSING_ERROR",
            "message": "An internal server error occurred during image parsing."
        }), 500

    @app.errorhandler(FileSystemError)
    def handle_file_system_error(error: FileSystemError):
        """Handles custom file system errors (500 Internal Server Error)."""
        db.session.rollback()
        # The full traceback is already logged in the remove_old_image function,
        # but we can log again here to indicate it was caught at the top level.
        current_app.logger.critical(f"A critical file system error was caught: {error}")
        return jsonify({
            "error_code": "FILE_SYSTEM_ERROR",
            "message": str(error) or "A server-side error occurred while managing files."
        }), 500


    # --- The Ultimate Fallback: Generic Exception Handler ---

    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        """Catches all unhandled exceptions."""
        db.session.rollback()
        if isinstance(error, HTTPException):
            # For standard HTTP errors from Werkzeug, use their properties.
            code = error.code
            error_code = error.name.upper().replace(" ", "_")
            message = error.description
            current_app.logger.warning(f"HTTPException caught: {code} - {error.name}")
        else:
            # For unexpected, non-HTTP errors, return a generic 500.
            code = 500
            error_code = "INTERNAL_SERVER_ERROR"
            message = "An unexpected internal server error occurred. Please contact the administrator."
            # Log the full stack trace for debugging.
            current_app.logger.exception("An unhandled exception occurred")

        response = {
            "error_code": error_code,
            "message": message
        }
        return jsonify(response), code


    # user_lookup_loaderの結果、ユーザーが見つからなかった時(None)のエラーを処理するローダー
    # user_lookup_callbackがNoneを返した時に自動的に呼ばれる
    @jwt.user_lookup_error_loader
    def user_lookup_error_callback(_jwt_header, jwt_data):
        current_app.logger.error(f"user_lookup_loaderでユーザーが見つからなかったようです")
        return jsonify({
            "message": "User not found.",
            "error_code": "USER_NOT_FOUND"
        }), 404 # 404ステータスコードを返すこともできる


    # アクセストークンだけでなくリフレッシュトークンが期限切れになったときにも呼び出されます。
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        user_identity = jwt_payload.get('sub', 'Unknown user')
        current_app.logger.info(f"トークンが期限切れのようです。TOKEN_EXPIREDのコードを返します。 User: {user_identity}")
        return jsonify({
            "message": "The token has expired",
            "error_code": "TOKEN_EXPIRED"
        }), 401


    # トークンが不正な形式の場合（署名改ざんなど）
    @jwt.invalid_token_loader
    def invalid_token_callback(error): # error引数は必須
        current_app.logger.info(f"正しくないトークンです: {error}")
        return jsonify({
            "message": "Signature verification failed. The token is invalid.",
            "error_code": "INVALID_TOKEN"
        }), 401


    # トークンが提供されなかった場合
    @jwt.unauthorized_loader
    def missing_token_callback(reason): # error引数は必須
        current_app.logger.info(f"トークンが存在しないようです: {reason}")
        return jsonify({
            "message": "Request does not contain an access token.",
            "error_code": "AUTHORIZATION_REQUIRED"
        }), 401


    # 失効済みのトークンが使用された場合
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        current_app.logger.info(f"トークンがブロックリストの中に入っているようです")
        return jsonify({
            "message": "The token has been revoked.",
            "error_code": "TOKEN_REVOKED"
        }), 401

