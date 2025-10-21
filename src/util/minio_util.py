import configparser
import os

from minio import Minio
from minio.error import S3Error

'''
/app/conf/config.ini ：
[minio]
endpoint = ip:port
access_key = admin
secret_key = admin
bucket = excel-mcp-server
secure = false
'''

class MinioClient:
    def __init__(self, config_path: str = '/app/conf/config.ini'):
        """
        初始化 MinIO 客户端，支持从 config.ini 读取配置
        :param config_path: 可选配置文件路径
        """
        self.config = self._load_config(config_path)

        self.client = Minio(
            endpoint=self.config["endpoint"],
            access_key=self.config["access_key"],
            secret_key=self.config["secret_key"],
            secure=self.config["secure"],
        )

        # 检查桶是否存在，不存在则创建
        if not self.client.bucket_exists(self.config["bucket"]):
            raise ValueError(f"指定的桶不存在: {self.config['bucket']}")

    def _load_config(self, config_path: str = None) -> dict:
        """
        从 config.ini 文件中读取 MinIO 配置信息
        """
        if not config_path or not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        if not config_path.endswith(".ini"):
            raise ValueError("配置文件必须是 .ini 格式")

        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")

        if "minio" not in parser:
            raise ValueError("配置文件中缺少 [minio] 节")

        cfg = parser["minio"]
        config = {
            "endpoint": cfg.get("endpoint"),
            "access_key": cfg.get("access_key"),
            "secret_key": cfg.get("secret_key"),
            "bucket": cfg.get("bucket"),
            "secure": cfg.getboolean("secure", False),
        }

        for k, v in config.items():
            if v is None:
                raise ValueError(f"配置项 '{k}' 缺失或为空")

        return config

    def minio_upload(self, object_name: str, file_path: str) -> str:
        """
        上传文件到 MinIO
        :param object_name: 对象名称
        :param file_path: 本地文件路径
        :return: 上传后的对象名
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            self.client.fput_object(self.config["bucket"], object_name, file_path)
            return object_name

        except S3Error as e:
            raise RuntimeError(f"MinIO 上传失败: {e}")
        except Exception as e:
            raise RuntimeError(f"上传文件时发生未知错误: {e}")

    def minio_download(self, object_name: str, file_path: str) -> str:
        """
        从 MinIO 下载文件（覆盖式下载）
        :param object_name: 对象名称
        :param file_path: 本地保存路径
        :return: 下载文件的本地路径
        """
        try:
            # 如果目标文件存在，则先删除以实现覆盖式下载
            if os.path.exists(file_path):
                os.remove(file_path)

            self.client.fget_object(self.config["bucket"], object_name, file_path)
            return file_path

        except S3Error as e:
            raise RuntimeError(f"MinIO 下载失败: {e}")
        except Exception as e:
            raise RuntimeError(f"下载文件时发生未知错误: {e}")

    def minio_is_exists(self, object_name: str) -> bool:
        """
        检查对象是否存在
        :param object_name: 对象名称
        :return: True 表示存在，False 表示不存在
        """
        try:
            self.client.stat_object(self.config["bucket"], object_name)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise RuntimeError(f"检查对象存在性时出错: {e}")
        except Exception as e:
            raise RuntimeError(f"检查对象存在性时发生未知错误: {e}")

    def minio_get_download_url(self, object_name: str) -> str:
        """
        获取对象的预签名下载 URL
        :param object_name: 对象名称
        :return: 可直接下载的 URL （有效期默认7天）
        """
        try:
            url = self.client.presigned_get_object(
                self.config["bucket"],
                object_name,
            )
            return url
        except S3Error as e:
            raise RuntimeError(f"获取下载链接失败: {e}")
        except Exception as e:
            raise RuntimeError(f"生成下载链接时发生未知错误: {e}")


# minio_client = MinioClient(config_path=r'E:\Myself\deepexi\fastagi\excel-mcp-server\excel-mcp-server-mydefine\config.ini')
# print(minio_client.minio_upload('aa/bb/aa.txt', r'C:\Users\Hualiuliu\Desktop\aa.txt'))
# print(minio_client.minio_is_exists('aa/bb/aa.txt'))
# print(minio_client.minio_is_exists('aa/bb/dd.txt'))
# print(minio_client.minio_download('aa/bb/aa.txt', r'C:\Users\Hualiuliu\Desktop\bb.txt'))
# print(minio_client.minio_get_download_url('aa/bb/aa.txt'))

