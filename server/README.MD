# 服务端设计

## minio

```sh

docker run -itd \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=haoshuai \
  -e MINIO_ROOT_PASSWORD=19920105 \
  -v /home/haoshuai/data/minio-data:/data \
  --restart=always \
  --name minio \
  quay.io/minio/minio server /data --console-address ":9001"

```

## postgresql

```sh
# POSTGRESQL_USERNAME  | PostgreSQL 默认用户名 postgres
# POSTGRESQL_PASSWORD | PostgreSQL 创建用户的密码
# POSTGRESQL_POSTGRES_PASSWORD PostgreSQL postgres 用户的密码

# docker run -itd \
#     -u root \
#     -v /home/haoshuai/data/postgresql-persistence:/bitnami/postgresql \
#     -p 5432:5432 \
#     -e POSTGRESQL_PASSWORD=Haoshuai9291. \
#     -e POSTGRESQL_POSTGRES_PASSWORD=Haoshuai9291. \
#     --restart=always \
#     --name postgresql \
#     bitnami/postgresql:17.6.0

docker run -itd \
    -u root \
    -v /home/haoshuai/data/postgresql-persistence:/bitnami/postgresql \
    -p 5432:5432 \
    -e POSTGRESQL_PASSWORD=Haoshuai9291. \
    --restart=always \
    --name postgresql \
    bitnami/postgresql:17.6.0

```


## 数据库

1. id
2. md5
3. url {}
4. thm
5. type
6. size
7. w,h
8. exif info
9. 