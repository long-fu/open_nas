from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import file as crud
from fastapi import File,UploadFile
from minio import Minio
import os
import mimetypes
import hashlib
from io import BytesIO
from minio.error import S3Error
from fastapi import HTTPException
from app.models.file import MinioFile
import piexif
import json
from io import BytesIO
from datetime import datetime

client = Minio(
    "localhost:9000",  # MinIO 服务地址
    access_key="minio",
    secret_key="minio123",
    secure=False  # 如果使用 HTTPS，设置为 True
)

# 计算文件的 md5 哈希值
def calculate_file_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

def calc_md5_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

# 存储文件到本地 storage，返回相对路径
def save_upload_picture(uid: str,upload_file: UploadFile):
    # try:
    file_data = BytesIO(upload_file.read())
    # file_name = upload_file.filename
    file_name:str = os.path.basename(upload_file.filename).decode("utf-8")   # hello.jpg
    if(len(file_name) <= 0):
        raise HTTPException(status_code=404, detail="File not found")
    file_size = len(file_data)
    if(file_size <= 0):
        raise HTTPException(status_code=404, detail="File not found")
    content_type = upload_file.content_type
    print(upload_file.content_type)
    print(upload_file.headers)
    bucket_name = uid
    file_hash = calc_md5_bytes(file_data)
    filename = f'{uid}_{file_hash}_{file_name}'
    object_name = f"pictures/{filename}"  # MinIO 存储路径
    
    # 创建桶
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    # ✅ 上传文件（内存流）
    client.put_object(
        file_name=filename,
        bucket_name=bucket_name,
        object_name=object_name,
        data=BytesIO(file_data),
        length=file_size,
        content_type=content_type
    )
    upload_file.close()
    file_url = f"http://localhost:9000/{bucket_name}/{object_name}"
    minio_file = MinioFile(url=file_url,bucket_name=bucket_name,object_name=object_name,size=file_size, content_type=content_type, hash=hash)
    return minio_file


def exif_to_dict(exif_dict):
    """
    将 piexif 读取的 EXIF 转成可序列化字典
    遇到 bytes 类型会 decode 成字符串
    """
    result = {}

    # 0th IFD (主信息)
    if "0th" in exif_dict:
        result["0th"] = {}
        for k, v in exif_dict["0th"].items():
            tag_name = piexif.TAGS["0th"][k]["name"]
            if isinstance(v, bytes):
                # 将 bytes 解码为可读字符串
                tag_value = v.decode("utf-8", errors="ignore")
            else:
                tag_value = str(v)
            result["0th"][tag_name] = tag_value

    # Exif IFD (拍摄信息)
    if "Exif" in exif_dict:
        result["Exif"] = {}
        for k, v in exif_dict["Exif"].items():
            tag_name = piexif.TAGS["Exif"][k]["name"]
            if isinstance(v, bytes):
                tag_value = v.decode("utf-8", errors="ignore")
            else:
                tag_value = str(v)
            result["Exif"][tag_name] = tag_value

    # GPS IFD
    if "GPS" in exif_dict:
        result["GPS"] = {}
        for k, v in exif_dict["GPS"].items():
            tag_name = piexif.TAGS["GPS"][k]["name"]
            if isinstance(v, bytes):
                tag_value = v.decode("utf-8", errors="ignore")
            else:
                tag_value = str(v)
            result["GPS"][tag_name] = tag_value

    # 1st IFD
    if "1st" in exif_dict:
        result["1st"] = {}
        for k, v in exif_dict["1st"].items():
            tag_name = piexif.TAGS["1st"][k]["name"]
            if isinstance(v, bytes):
                tag_value = v.decode("utf-8", errors="ignore")
            else:
                tag_value = str(v)
            result["1st"][tag_name] = tag_value

    return result

def read_image_exif_from_bytes(image_bytes: bytes):
    """
    从图片字节数据解析 EXIF 并返回 JSON
    """
    exif_dict = piexif.load(image_bytes)
    data_dict = exif_to_dict(exif_dict)
    return data_dict

from app.models.file import File
class FileService:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_directory(self, owner_id: str, name: str, parent_id: int = None):
        return await crud.create_directory(self.db, owner_id, name, parent_id)
    
    async def upload_file(self, owner_id: str, upload_file: UploadFile):
        file_info = read_image_exif_from_bytes(BytesIO(upload_file.file.read()))
        print(file_info)
        
        print(file_info["Exif"]["DateTimeOriginal"])
        dt_obj = datetime.strptime(file_info["Exif"]["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
        print(dt_obj.year, dt_obj.month, dt_obj.year)
        file_:File = crud.create_directory(db=self.db, owner_id=owner_id,name=dt_obj.year, parent_id=None)
        # file_.id
        
        # 图片补充中间路径
        
        # 可以解析出存储路径
        # 解析出数据
        file_data = save_upload_picture(owner_id, upload_file)
    
        
        # 分割时间 年 月 日 文件夹创建
        # 查询 文件id
        parent_id = None
        
        #
        
        return await crud.upload_file(self.db, owner_id, parent_id ,file_data)

    async def list_children(self, owner_id: str, dir_id: int):
        return await crud.list_children(self.db, owner_id, dir_id)

    async def get_path(self, file_id: int):
        return await crud.get_full_path(self.db, file_id)

    async def move(self, node_id: int, new_parent_id: int):
        return await crud.move_node(self.db, node_id, new_parent_id)