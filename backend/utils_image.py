import os
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
from flask import current_app

# 許可する拡張子とフォーマット、ファイルサイズ上限
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_FORMATS = {'JPEG', 'JPG', 'PNG', 'GIF', 'MPO'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
# 画像の最大幅・高さ制限
MAX_WIDTH = 10000  # 例: 10000px
MAX_HEIGHT = 10000  # 例: 10000px

class ImageValidationError(Exception):
    """バリデーションエラー用例外"""
    pass

class FileSystemError(Exception):
    """A custom exception for file system related errors within the application."""
    pass


def validate_image(file):
    """
    Validates an uploaded image file against a set of rules.

    Args:
        file: A file object from Flask's request (e.g., request.files['image']).

    Raises:
        ImageValidationError: If the file fails any validation check.

    Returns:
        str: A sanitized, safe filename if validation is successful.
    """
    # 1. Check for file existence  # これは、view関数の中ですでに弾いているので必要ない。エラーにはしないということ。
    # if not file or not file.filename:
    #     raise ImageValidationError('No file selected.')

    # 2. Generate a secure filename
    filename = secure_filename(file.filename)
    if not filename:
        raise ImageValidationError('Invalid filename.')

    # 3. Check file extension
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    if ext not in ALLOWED_EXTENSIONS:
        raise ImageValidationError(f'File extension not allowed: .{ext}')

    # 4. Check MIME type (as reported by the browser)
    # This is a good first-pass check but can be spoofed.
    allowed_mimes = {'image/jpeg', 'image/png', 'image/gif'}
    if file.content_type not in allowed_mimes:
        raise ImageValidationError(f'Disallowed MIME type: {file.content_type}')

    # 5. Check file size
    # Prefer content_length header, but fall back to reading the stream if not available.
    try:
        file.stream.seek(0, os.SEEK_END)
        size = file.stream.tell()
    except (AttributeError, OSError):
        # In-memory streams might not support seek/tell, rely on content_length
        size = getattr(file, 'content_length', 0)

    if size > MAX_FILE_SIZE:
        size_mb = size / (1024 * 1024)
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise ImageValidationError(f'File size ({size_mb:.1f}MB) exceeds the maximum allowed size of {max_mb:.1f}MB.')
    file.stream.seek(0)

    # 6. Check image content using Pillow (format, dimensions, and integrity)
    try:
        # Use a single `with` block to open the image once.
        # This also implicitly checks for corruption.
        with Image.open(file.stream) as img:
            img_format = img.format
            width, height = img.size

            if img_format not in ALLOWED_FORMATS:
                raise ImageValidationError(f'Image format not allowed: {img_format}')

            if width > MAX_WIDTH or height > MAX_HEIGHT:
                raise ImageValidationError(
                    f'Image dimensions ({width}px x {height}px) exceed the maximum allowed dimensions of {MAX_WIDTH}px x {MAX_HEIGHT}px.'
                )

            # This is a more thorough check than just verify().
            # It loads the image data into memory, detecting truncated files.
            img.load()

    except UnidentifiedImageError:
        # This happens if the file is not a recognizable image format.
        raise ImageValidationError('The file is not a valid or recognizable image.')
    except Exception as e:
        # Catch any other Pillow-related errors (e.g., decompression bombs, memory errors).
        # We re-raise it as our custom validation error for a consistent API response.
        current_app.logger.error(f"Unexpected error during image processing: {e}", exc_info=True)
        raise ImageValidationError('An unexpected error occurred during image processing.')
    finally:
        # IMPORTANT: Always reset the stream pointer for subsequent operations (e.g., saving the file).
        file.stream.seek(0)

    return filename



def remove_old_image(filename: str):
    """
    Deletes an old image from the UPLOAD_FOLDER using its filename.
    """
    if not filename:
        return

    try:
        # セキュリティのため、渡されたファイル名が不正なパスを含んでいないか再度確認
        # (DBから取得しているので基本的には安全だが、二重の防御として有効)
        safe_filename = secure_filename(filename)
        if safe_filename != filename:
            # ファイル名に'../'などが含まれていた場合
            current_app.logger.error(f"Attempted to delete a file with an insecure path: {filename}")
            # エラーを発生させるか、単に処理を中断するかは設計による
            # ここでは何もしないことで安全を確保
            return

        # configからUPLOAD_FOLDERの絶対パスを取得
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # ファイル名と結合して完全なローカルファイルパスを作成
        file_path = os.path.join(upload_folder, safe_filename)

        # ファイルが存在すれば削除
        os.remove(file_path)
        current_app.logger.info(f"Successfully deleted old image: {file_path}")

    except FileNotFoundError:
        # ファイルが存在しない場合は、すでに目的は達成されているので警告ログのみでOK
        current_app.logger.warning(f"Attempted to delete non-existent file: {file_path}")
        pass
    except PermissionError as e:
        # これはサーバーの設定ミス（権限不足）に起因するエラー
        current_app.logger.error(f"Permission denied while trying to delete image {file_path}: {e}")
        raise FileSystemError("Failed to delete the image due to a permission error.") from e
    except OSError as e:
        # その他のOSレベルのエラー
        current_app.logger.error(f"An OS error occurred while deleting image {file_path}: {e}")
        raise FileSystemError("An unexpected OS error occurred while trying to delete the image.") from e