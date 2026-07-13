# coding:utf8
import os
import sys


# 获取平台信息
platform_info = sys.platform
try:
    import platform

    platform_info = platform.platform()
except:
    pass


install_path = os.path.dirname(__file__)

notify_string_no_config = """请联系管理员获取配置文件，并告知如下信息。

\t操作系统：{os}
\tPython版本：{py_version}
\t包安装路径：{install_path}
""".format(
    os=platform_info, py_version=sys.version, install_path=install_path
)


class NoConfigError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(notify_string_no_config, *args, **kwargs)
