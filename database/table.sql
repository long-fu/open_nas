CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    -- 主键ID，自增
    uid VARCHAR(64) UNIQUE NOT NULL,
    -- 用户唯一标识（可生成UUID）
    name VARCHAR(100) NOT NULL,
    -- 用户名
    email VARCHAR(150) UNIQUE,
    -- 邮箱，唯一
    phone VARCHAR(20) UNIQUE,
    -- 手机号，唯一
    password VARCHAR(255) NOT NULL,
    -- 密码（建议存储hash值，比如bcrypt/argon2）
    gender SMALLINT,
    -- 性别（0=未知, 1=男, 2=女）
    age INT,
    -- 年龄
    status SMALLINT DEFAULT 1,
    -- 状态（1=正常, 0=禁用）
    created_at TIMESTAMP DEFAULT NOW(),
    -- 注册时间
    updated_at TIMESTAMP DEFAULT NOW() -- 最后更新时间
);
CREATE TABLE file_directory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_file BOOLEAN NOT NULL,
    file_size BIGINT DEFAULT NULL,
    owner_id INT NOT NULL,
    -- 拥有者用户ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE directory_closure (
    ancestor_id INT NOT NULL,
    descendant_id INT NOT NULL,
    depth INT NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id),
    FOREIGN KEY (ancestor_id) REFERENCES file_directory(id) ON DELETE CASCADE,
    FOREIGN KEY (descendant_id) REFERENCES file_directory(id) ON DELETE CASCADE
);
-- 基础文件表（通用文件信息）
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    -- 主键ID
    owner_id BIGINT NOT NULL,
    -- 所属用户
    parent_id BIGINT,
    -- 父目录ID（树形结构）
    name VARCHAR(255) NOT NULL,
    -- 文件名
    size BIGINT NOT NULL,
    -- 文件大小（字节）
    mime_type VARCHAR(100),
    -- 文件MIME类型 (image/jpeg, image/png 等)
    storage_url TEXT NOT NULL,
    -- 文件存储路径 (NAS/MinIO/S3等)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_owner FOREIGN KEY(owner_id) REFERENCES users(id)
);
-- 照片表（扩展元数据）
CREATE TABLE photos (
    id BIGSERIAL PRIMARY KEY,
    -- 主键ID
    file_id BIGINT NOT NULL UNIQUE,
    -- 对应文件表的ID (一对一)
    width INT,
    -- 分辨率 - 宽
    height INT,
    -- 分辨率 - 高
    format VARCHAR(20),
    -- 格式 (jpg, png, heic, raw 等)
    taken_at TIMESTAMP,
    -- 拍摄时间（Exif提取）
    camera_make VARCHAR(100),
    -- 相机厂商 (Exif 可选)
    camera_model VARCHAR(100),
    -- 相机型号
    focal_length VARCHAR(50),
    -- 焦距
    aperture VARCHAR(20),
    -- 光圈
    iso INT,
    -- ISO
    gps_latitude DECIMAL(10, 7),
    -- 拍摄地纬度
    gps_longitude DECIMAL(10, 7),
    -- 拍摄地经度
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_file FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
);
-- Live Photo 表：把 "静态图" 和 "视频" 关联起来
CREATE TABLE live_photos (
    id BIGSERIAL PRIMARY KEY,
    -- 所属用户
    photo_id BIGINT NOT NULL,
    -- 对应 photos.id
    video_file_id BIGINT NOT NULL,
    -- 对应 files.id (存MOV视频)
    asset_id VARCHAR(100),
    -- 苹果的 Live Photo 资源标识
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_photo FOREIGN KEY(photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    CONSTRAINT fk_video FOREIGN KEY(video_file_id) REFERENCES files(id) ON DELETE CASCADE
);
CREATE TABLE videos (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT NOT NULL UNIQUE,
    -- 对应文件表 (files.id)
    format VARCHAR(20),
    -- 格式 (mp4, mov, mkv, avi 等)
    width INT,
    -- 分辨率 - 宽
    height INT,
    -- 分辨率 - 高
    duration_seconds DECIMAL(10, 2),
    -- 时长（秒）
    bitrate BIGINT,
    -- 比特率（bps）
    codec_video VARCHAR(50),
    -- 视频编码 (h264, hevc, vp9, av1 等)
    codec_audio VARCHAR(50),
    -- 音频编码 (aac, mp3, opus 等)
    frame_rate DECIMAL(5, 2),
    -- 帧率 (fps)
    rotation SMALLINT,
    -- 旋转角度 (0,90,180,270)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_file FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
);
-- 音乐表（音频文件的元数据）
CREATE TABLE audios (
    id BIGSERIAL PRIMARY KEY,
    file_id BIGINT NOT NULL UNIQUE,
    -- 对应 files.id
    lyrics_file_id BIGINT,
    -- 歌词文件
    format VARCHAR(20),
    -- 格式 (mp3, flac, wav, aac, ogg, m4a 等)
    duration_seconds DECIMAL(10, 2),
    -- 时长（秒）
    bitrate BIGINT,
    -- 比特率 (bps)
    sample_rate INT,
    -- 采样率 (Hz)
    channels SMALLINT,
    -- 声道数 (1=单声道, 2=立体声, 5=5.1 等)
    -- 音乐标签（ID3/FLAC/APE 标签解析）
    title VARCHAR(255),
    -- 歌曲标题
    artist VARCHAR(255),
    -- 艺术家
    album VARCHAR(255),
    -- 专辑
    genre VARCHAR(100),
    -- 流派
    track_number INT,
    -- 专辑中的曲目号
    release_year INT,
    -- 发行年份
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_file FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE,
    CONSTRAINT fk_lyrics_file FOREIGN KEY(lyrics_file_id) REFERENCES files(id) ON DELETE
    SET NULL
);