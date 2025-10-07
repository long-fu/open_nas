import piexif
import json
from io import BytesIO

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
    # print(type())
    data_dict = exif_to_dict(exif_dict)
    return data_dict

import datetime 
import time
from datetime import datetime


from datetime import datetime, timedelta, timezone
ACCESS_TOKEN_EXPIRE_MINUTES = 60
expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
print(expire)
# if __name__ == "__main__":
#     # 例子：读取文件为 bytes
#     with open("/home/haoshuai/code/open_nas/test_hello/test.jpeg", "rb") as f:
#         img_bytes = f.read()

#     exif_json = read_image_exif_from_bytes(img_bytes)
#     # print(exif_json)
#     # print(type(exif_json["Exif"]["DateTimeOriginal"]))
#     # decode('utf-8')
    
#     # print(exif_json["Exif"]["DateTimeOriginal"])
#     time_str = exif_json["Exif"]["DateTimeOriginal"]
#     # time_str = "2016:07:22 10:04:28"
#     dt_obj = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
#     # print(dt_obj.year)
#     # from datetime import datetime

#     # datetime_str = '09/19/18 13:55:26'

#     # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

#     # print(type(datetime_object))
#     # print(datetime_object)  # printed in default format
#     # date = datetime.for
#     # print(time_ddatetimedatetime_objectobjectate)