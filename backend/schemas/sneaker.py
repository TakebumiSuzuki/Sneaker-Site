from typing import Annotated
from flask import url_for, current_app
from pydantic import BaseModel, Field, ConfigDict, computed_field

from backend.enums import CategoryEnum
from decimal import Decimal
from datetime import datetime


class CreateSneaker(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field('', max_length=1000)
    category: CategoryEnum
    price: Annotated[
        Decimal,
        Field(ge=0, max_digits=10, decimal_places=2)
    ] | None = None
    stock: int|None = Field(None, ge=0, le=10000)
    featured: bool = Field(False)

# このスキーマにより、model_validateの直後はキーバリューが存在しないフィールドは強引にNoneが設定される。
# そのかとでmodel_dump()において、exclude_unset=Trueが有効になっているので、それらは再度消去される。 
# これにより、Patchがうまく働くことになる。
class UpdateSneaker(BaseModel):
    name: str|None = Field(None, max_length=50)
    description: str|None = Field(None, max_length=1000)
    category: CategoryEnum|None = Field(None)
    price: Annotated[
        Decimal,
        Field(ge=0, max_digits=10, decimal_places=2)
    ] | None = None
    stock: int|None = Field(None, ge=0, le=10000)
    featured: bool|None = Field(None)


class SneakerWithImageUrl(BaseModel):
    """
    image_urlを動的に生成するロジックを持つベーススキーマ。
    このスキーマを継承するクラスは、元のオブジェクト（例: Sneakerモデル）に
    'image_filename'属性が存在することを期待します。
    """

    # このデコレータが、シリアライズ時にimage_urlフィールドを動的に生成する
    @computed_field
    @property
    def image_url(self) -> str | None:
        # from_attributes=True を介してオブジェクトから生成されたPydanticインスタンスは、スキーマに明示的に定義されていない属性であっても、元のオブジェクトの情報を内部的に保持（またはアクセス可能に）しています。
        # つまり、image_urlメソッド内のselfは、idやnameといった定義済みのフィールドを持っているだけでなく、データソースとなったsneakerオブジェクトが持っていた**image_filename属性にもアクセスできる状態**になっているのです。
        image_filename = getattr(self, 'image_filename', None)
        if image_filename:
            # UPLOAD_FOLDER内のファイルへの静的URLを生成
            return url_for('static', filename=f'uploads/{image_filename}', _external=True)
        return None

    # この設定は継承先のスキーマにも引き継がれます
    model_config = ConfigDict(from_attributes=True)


class ReadSneaker(SneakerWithImageUrl):
    id: int
    name: str
    description: str
    category: CategoryEnum
    price: Decimal|None
    stock: int|None
    featured: bool
    image_filename: str | None = None
    created_at: datetime
    updated_at: datetime
    # model_configも継承されるため、再定義は不要


class PublicSneaker(SneakerWithImageUrl):
    name: str
    description: str
    category: CategoryEnum
    price: Decimal|None
    stock: int|None
    featured: bool
    image_filename: str | None = None
    # model_configも継承されるため、再定義は不要