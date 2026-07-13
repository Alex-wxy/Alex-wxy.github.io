# import json
# from shangjian_api.airworks.package_api import AirWorksApi

# awp = AirWorksApi(
#     base_url="https://rds.csc.com.cn",
#     access_key="FAg8RbHVuXk_1603",
#     access_secret="fLKDbadecsAIx9pnaibZzg",
#     default_app_id=43,
#     default_api_method="GET",
#     default_page_num=1,
#     default_page_size=100,
#     debug=False
# )

# # ── 对比第 1 页和第 2 页的前 3 条，确认 page_num 是否生效 ──
# p1 = awp.electriccars__sales__value(api_method="GET", page_num=1, page_size=500)
# p2 = awp.electriccars__sales__value(api_method="GET", page_num=2, page_size=500)

# print("=== 第 1 页前 3 条 ===")
# for item in p1["data"]["items"][:3]:
#     print(f"  {item['pic_title']} | {item['series_name']} | {item['date']} | {item.get('value', 'N/A')}")

# print("\n=== 第 2 页前 3 条 ===")
# for item in p2["data"]["items"][:3]:
#     print(f"  {item['pic_title']} | {item['series_name']} | {item['date']} | {item.get('value', 'N/A')}")

# print(f"\ntotal_num: {p1['data']['total_num']}")
# print(f"第 1 页 items 数: {len(p1['data']['items'])}")
# print(f"第 2 页 items 数: {len(p2['data']['items'])}")
from shangjian_api.airworks.package_api import AirWorksApi

# ============================================================
# API 配置
# ============================================================
API_CONFIG = {
    "base_url":        "https://rds.csc.com.cn",
    "access_key":      "FAg8RbHVuXk_1603",
    "access_secret":   "fLKDbadecsAIx9pnaibZzg",
    "default_app_id":  43,
    "default_api_method": "GET",
    "default_page_num":   1,
    "default_page_size":  500,
    "debug": False,
}


def fetch_all(api_method, label):
    """翻页拉取全部数据，返回 items 列表"""
    page_size = 500     # 中台单页上限
    all_items = []
    page_num = 1

    while True:
        res = api_method(
            api_method="GET",
            page_num=page_num,
            page_size=page_size,
        )
        if res.get("error_code") != 0:
            raise Exception(f"获取{label}失败: {res.get('error_message')}")

        data = res["data"]
        items = data["items"]
        total_num = data["total_num"]
        all_items.extend(items)

        print(f"    {label} 第{page_num}页: {len(items)}条, 累计 {len(all_items)}/{total_num}")
        for i, item in enumerate(items[:3]):
            print(f"      [{i+1}] {item['pic_title']} | {item['series_name']} | {item['date']} | {item.get('value', 'N/A')}")
            # print(f"      [{i+1}] {item['pic_title']} | {item['series_name']} | {item['sheet_name']} | {item['unit']}")

        if len(all_items) >= total_num:
            break
        page_num += 1

    print(f"    {label} 完成，共 {len(all_items)} 条")
    return all_items

api = AirWorksApi(**API_CONFIG)
fetch_all(api.electriccars__sales__value, "data_points")
#electriccars__sales__structure
#electriccars__sales__value