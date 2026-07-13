import requests
import pandas as pd
from urllib.parse import urljoin
from . import settings

TOP_PACKAGE = settings.TOP_PACKAGE

session = requests.Session()


def get_indicator_values(
    indicator_ids,
    host="",
    username="",
    password="",
    api_path="/api/v1/indicator_v2/export/dataframe_json",
):
    """

    Args:
        indicator_ids: ["indicator_id", ...]
        host: 例如 "localhost:8888"
        username:
        password:
        api_path:

    Returns:

    """
    host = host or settings.INDICATOR_SERVICE_HOST
    username = username or settings.INDICATOR_SERVICE_USERNAME
    password = password or settings.INDICATOR_SERVICE_PASSWORD

    if not host:
        raise TOP_PACKAGE.exceptions.NoConfigError

    if not host.startswith("http"):
        host = "http://{}".format(host)

    url = urljoin(host, api_path)
    #
    auth = ()
    if username and password:
        auth = (username, password)
    #
    response = session.post(url, json=dict(indicator_ids=indicator_ids), auth=auth)
    response.close()
    response.raise_for_status()
    #
    res = []
    j_response = response.json()
    # 此处保证顺序 找不到的数据返回None
    for indicator_id in indicator_ids:
        indicator_data = j_response.get(indicator_id, None)
        if not indicator_data:
            # yh 需求 返回存在任意两列的空 DataFrame
            empty_df = pd.DataFrame()
            empty_df["_default_1"] = []
            empty_df["_default_2"] = []
            res.append(empty_df)
        else:
            df = pd.DataFrame.from_dict(indicator_data)
            df.name = indicator_id
            res.append(df)
    return res


if __name__ == "__main__":
    indicator_ids = ["all_indexpv_chain_rank_app_by_week_all"]
    result = get_indicator_values(indicator_ids)
    print(result)
