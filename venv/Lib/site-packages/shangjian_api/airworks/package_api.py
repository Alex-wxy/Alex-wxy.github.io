import json
import re
from functools import partial
from .base_api import BaseApi, ApiError


class AirWorksApi:
    def __init__(
        self,
        base_url="",
        access_key="",
        access_secret="",
        default_app_id=None,
        **kwargs,
    ):
        self.base_api = BaseApi(
            base_url=base_url,
            access_key=access_key,
            access_secret=access_secret,
            **kwargs,
        )
        #
        self.default_app_id = default_app_id
        self.default_api_method = kwargs.get("default_api_method", "GET")
        self.default_page_num = kwargs.get("default_page_num", 1)
        self.default_page_size = kwargs.get("default_page_size", 100)
        self.default_debug = kwargs.get("debug", False)

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def close(self):
        self.base_api.close()
        return

    def _call(self, api_url, **kwargs):
        app_id = kwargs.get("app_id", self.default_app_id)
        if not app_id:
            raise ApiError(
                error_code=40009, error_msg="app_id缺失，请先设置default_app_id或传入app_id"
            )
        api_url = self._url_transfer(api_url)

        kwargs.update(
            {
                "app_url": f"api_gateway/api/{app_id}/{api_url}",
                "api_method": kwargs.get("api_method") or self.default_api_method,
                "page_num": kwargs.get("page_num") or self.default_page_num,
                "page_size": kwargs.get("page_size") or self.default_page_size,
                "debug": kwargs.get("debug") or self.default_debug,
            }
        )
        return self.base_api.api_response(**kwargs)

    @classmethod
    def _url_transfer(cls, url):
        url_list = list()
        for index, item in enumerate(url.split("__")):
            if index == 0 and re.match(r"_[0-9]", item):
                item = item[1:]
            url_list.append(item.replace("_A", "/"))
        url = "_".join(url_list)
        return url

    def call(self, **kwargs):
        return self.base_api.api_response(**kwargs)

    def __getattr__(self, key):
        return partial(self._call, api_url=key)


if __name__ == "__main__":
    awp = AirWorksApi(
        base_url="aw-airworks-frontend:30000",
        access_key="kB85aqPMFZs_14",
        access_secret="lh66YHfiE7qL6TcOOvbLTg",
        default_app_id=49,
    )

    res = awp.mall(
        shop_id="", shop_name="", state="1", page_num=1, page_size=10, api_method="GET"
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))

    res = awp.call(
        app_url="api_gateway/api/49/mall",
        shop_id="",
        shop_name="",
        state="1",
        page_num=1,
        page_size=10,
        api_method="GET",
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))
