# coding:utf8
import os
import toml

# 读取本地配置文件
local_config = {}
config_path = os.path.join(os.path.dirname(__file__), "sdk_config.toml")
if os.path.exists(config_path):
    local_config = toml.load(config_path)
