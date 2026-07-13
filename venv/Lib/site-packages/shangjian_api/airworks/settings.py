# coding:utf8
import os
import sys

# 获取包名
TOP_PACKAGE_NAME = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
TOP_PACKAGE = sys.modules[TOP_PACKAGE_NAME]

# Airworks API
# "localhost:8888"
BASE_URL = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

# 获取本地配置
local_config = TOP_PACKAGE.settings.local_config
if (
    "airworks" in local_config
    and "api" in local_config["airworks"]
    and isinstance(local_config["airworks"]["api"], dict)
):
    BASE_URL = local_config["airworks"]["api"]["host"]
    ACCESS_KEY = local_config["airworks"]["api"]["access_key"]
    ACCESS_SECRET = local_config["airworks"]["api"]["access_secret"]
