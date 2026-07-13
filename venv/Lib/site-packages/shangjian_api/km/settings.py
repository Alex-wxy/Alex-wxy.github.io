# coding:utf8
import os
import sys

# 获取包名
TOP_PACKAGE_NAME = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
TOP_PACKAGE = sys.modules[TOP_PACKAGE_NAME]

# 指标数据API
# "http://10.1.185.2:8888"
INDICATOR_SERVICE_HOST = ""
INDICATOR_SERVICE_USERNAME = ""
INDICATOR_SERVICE_PASSWORD = ""

# 获取本地配置
local_config = TOP_PACKAGE.settings.local_config
if (
    "km" in local_config
    and "indicator" in local_config["km"]
    and isinstance(local_config["km"]["indicator"], dict)
):
    INDICATOR_SERVICE_HOST = local_config["km"]["indicator"]["host"]
    INDICATOR_SERVICE_USERNAME = local_config["km"]["indicator"]["username"]
    INDICATOR_SERVICE_PASSWORD = local_config["km"]["indicator"]["password"]
