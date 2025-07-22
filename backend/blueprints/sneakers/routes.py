import os
import time
from uuid import uuid4
from flask import Blueprint, jsonify, request, url_for, current_app
from sqlalchemy import select, or_
from flask_jwt_extended import jwt_required

from backend.extensions import db
from backend.utils_image import validate_image, remove_old_image
from backend.models.sneaker import Sneaker
from backend.schemas.sneaker import CreateSneaker, ReadSneaker, PublicSneaker, UpdateSneaker
from backend.decorators import require_admin

sneakers_bp =  Blueprint('sneakers', __name__, url_prefix='/api/sneakers')


@sneakers_bp.get('/')
def get_items():

    time.sleep(1)

    q = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)

    stmt = select(Sneaker)
    if q:
        stmt = stmt.where(or_(
            Sneaker.name.ilike(f"%{q}%"),
            Sneaker.description.ilike(f"%{q}%"),
            Sneaker.category.ilike(f"%{q}%")
        ))
    stmt = stmt.order_by(Sneaker.id.desc())

    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    sneakers = pagination.items
    data = [ ReadSneaker.model_validate(sneaker).model_dump() for sneaker in sneakers ]
    response = {
        "items": data,
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
    }
    return jsonify(response), 200


@sneakers_bp.get('/<int:sneaker_id>')
@jwt_required()
def get_item(sneaker_id):

    time.sleep(1)

    sneaker = db.get_or_404(Sneaker, sneaker_id)
    data = ReadSneaker.model_validate(sneaker).model_dump()
    return jsonify(data), 200


@sneakers_bp.post('/')
@jwt_required()
@require_admin
def create_item():

    time.sleep(1)

    # request.formは、werkzeug.datastructures.ImmutableMultiDictという、辞書によく似た特別な型のオブジェクト
    input_data = request.form.to_dict()
    dto = CreateSneaker.model_validate(input_data)

    image_filename = None
    image = request.files.get('image')
    # 重要な点として、ユーザーがファイルを選択せずに送った時には、image自体は存在し、image.filenameが空文字となる。
    if image and image.filename:
        safe_basename = validate_image(image)
        name_part, extension = os.path.splitext(safe_basename)
        filename = f"{name_part}_{uuid4()}{extension}"
        save_dir = current_app.config['UPLOAD_FOLDER']
        save_path = os.path.join(save_dir, filename)
        image.save(save_path)
        image_filename = filename

    sneaker = Sneaker(**dto.model_dump(), image_filename=image_filename)

    db.session.add(sneaker)
    db.session.commit()

    data = PublicSneaker.model_validate(sneaker).model_dump()
    location = url_for('sneakers.get_item', sneaker_id=sneaker.id, _external=True)

    return jsonify(data), 201, {'Location': location }


# クライアント側でボディの中に'delete_image':'true'　か'false'かを含めること。
@sneakers_bp.patch('/<int:sneaker_id>')
@jwt_required()
@require_admin
def update_item(sneaker_id):

    time.sleep(1)

    sneaker = db.get_or_404(Sneaker, sneaker_id)

    input_data = request.form.to_dict()
    dto = UpdateSneaker.model_validate(input_data)
    update_data = dto.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(sneaker, key, value)

    old_image_filename = None

    # ユーザーが新しいイメージを選択した場合
    if image := request.files.get('image'):
        current_app.logger.error('imageキーがリクエストに存在します')
        # ファイルが選択されているか（filenameが空でないか）をチェック
        if image.filename:
            current_app.logger.error('imageキーがリクエストに存在し、さらに実際にイメージが送られてきているようです。')
            # ★重要: DBを更新する前に、後で削除するために古いファイル名を保持しておく
            old_image_filename = sneaker.image_filename

            # 新しい画像を保存し、モデルの属性を更新
            safe_basename = validate_image(image)
            name_part, extension = os.path.splitext(safe_basename)
            filename = f"{name_part}_{uuid4()}{extension}"
            save_dir = current_app.config['UPLOAD_FOLDER']
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            sneaker.image_filename = filename
        else:
            current_app.logger.error('imageキーがリクエストに存在しますが、実際にイメージが送られてきていないようです。')

    elif request.form.get('delete_image') == 'true':
        current_app.logger.error('imageキーがリクエストに存在しません、さらにdelete_imageフラッグがtrueになっています')
        old_image_filename = sneaker.image_filename or None
        sneaker.image_filename = None
        current_app.logger.error('ケース２')

    # ユーザーが新しいイメージを選択しておらず、なおかつdelete_imageフラッグが'trueではないの場合は何もしない
    else:
        current_app.logger.error('imageキーがリクエストに存在しません、さらにdelete_imageフラッグがtrueではありません。なので何もしない')

    db.session.commit()

    # ★コミットが成功した後に、保持しておいた古いファイル名の画像を削除する
    if old_image_filename:
        remove_old_image(old_image_filename)

    data = PublicSneaker.model_validate(sneaker).model_dump()

    return jsonify(data), 200


@sneakers_bp.delete('/<int:sneaker_id>')
@jwt_required()
@require_admin
def delete_item(sneaker_id):

    time.sleep(1)

    sneaker = db.get_or_404(Sneaker, sneaker_id)
    image_filename_to_delete = sneaker.image_filename
    db.session.delete(sneaker)
    db.session.commit()
    if image_filename_to_delete:
        remove_old_image(image_filename_to_delete)

    return '', 204


