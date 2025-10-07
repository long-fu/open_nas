from io import BytesIO
from datetime import datetime
from minio import Minio
import os
client = Minio(
    "localhost:9000",  # MinIO 服务地址
    access_key="haoshuai",
    secret_key="19920105",
    secure=False  # 如果使用 HTTPS，设置为 True
)
bucket_name="773279fbb337babbc59ef1a1639cdcda"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
# client.fput_object(
#     bucket_name=bucket_name,
#     object_name="2020/12/01/test.jpg",
#     file_path="/home/haoshuai/code/open_nas/test_hello/test.jpeg",)

file = open("/home/haoshuai/code/open_nas/test_hello/test.jpeg",mode="rb")
# data =file.read()
file_size = os.path.getsize("/home/haoshuai/code/open_nas/test_hello/test.jpeg")
client.put_object(bucket_name=bucket_name, object_name="2022/12/01/tes.jpg",data=file,length=file_size)
# client.put_object()

# async def save_upload_picture(uid: str,upload_file: UploadFile):
#     # try:
#     file_data = await upload_file.read()
#     # print(type(file_data))
#     # file_name = upload_file.filename
#     print(upload_file.filename)
#     file_name:str = os.path.basename(upload_file.filename)   # hello.jpg
#     # if(len(file_name) <= 0):
#     #     raise HTTPException(status_code=404, detail="File not found")
#     # # print(filename)
#     # file_size = upload_file.size
#     # if(file_size <= 0):
#     #     raise HTTPException(status_code=404, detail="File not found")
#     content_type = upload_file.content_type
#     print(upload_file.content_type)
#     print(upload_file.headers)
#     bucket_name = uid
#     file_hash = calc_md5_bytes(file_data)
#     filename = f'{uid}_{file_hash}_{file_name}'
#     object_name = f"pictures/{filename}"  # MinIO 存储路径
    
#     # 创建桶
#     if not client.bucket_exists(bucket_name):
#         client.make_bucket(bucket_name)
#     # ✅ 上传文件（内存流）
#     client.put_object(
#         file_name=filename,
#         bucket_name=bucket_name,
#         object_name=object_name,
#         data=BytesIO(file_data),
#         length=file_size,
#         content_type=content_type
#     )
#     print("上传完成")
#     upload_file.close()
#     file_url = f"http://localhost:9000/{bucket_name}/{object_name}"
#     # minio_file = MinioFile(url=file_url,bucket_name=bucket_name,object_name=object_name,size=file_size, content_type=content_type, hash=hash)
#     return file_url