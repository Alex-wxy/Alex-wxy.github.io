"""
锂电产业链数据看板 — 构建脚本
通过中台 API 获取数据，组装 JSON 并生成静态 HTML
"""
import json
import os
from shangjian_api.airworks.package_api import AirWorksApi
from build_common import generate_html

OUTPUT_HTML = "index.html"

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
    "default_page_size":  10000,
    "debug": False,
}

# ============================================================
# 硬编码导航结构
# ============================================================
CATEGORIES = [
    {
        "name": "新能源车销量",
        "api_structure": "electriccars__sales__structure",
        "api_value": "electriccars__sales__value",
        "sheets": [
            {"name": "全球销量-Marklines",      "source": "Marklines"},
            {"name": "中国销量-中汽协",         "source": "中汽协"},
            {"name": "中国销量-乘联会",          "source": "乘联会"},
            {"name": "欧洲九国销量-各国官网",    "source": "各国官网",
             "children": ["法国","英国","德国","意大利","挪威","瑞典","葡萄牙","西班牙","丹麦"],
             "children_source": "欧洲九国销量-分国家"},
            {"name": "欧洲九国销量-分国家",      "source": "各国官网", "hidden": True},
            {"name": "欧洲销量-Marklines",      "source": "Marklines"},
            {"name": "美国销量-Marklines",      "source": "Marklines"},
            {"name": "日韩销量-Marklines",      "source": "Marklines"},
        ],
    },
    {
        "name": "电池产销&装机数据",
        "api_structure": "batterysales__structure",
        "api_value": "batterysales__value",
        "sheets": [
            {"name": "国内电池产销",       "source": "动力电池创新联盟"},
            {"name": "国内动力电池装机量",       "source": "动力电池创新联盟"},
            {"name": "动力电池单车带电量", "source": "动力电池创新联盟"},
            {"name": "全球动力电池装机量", "source": "SNE Research"},
            {"name": "头部电池厂商排产",   "source": "鑫椤资讯"},
        ],
    },
    {
        "name": "锂电材料价格&排产数据",
        "api_structure": "lithiumprice__structure",
        "api_value": "lithiumprice__value",
        "sheets": [
            {"name": "价格变化展示格式",     "source": "鑫椤资讯"},
            {"name": "头部锂电材料厂商排产", "source": "鑫椤资讯"},
        ],
    },
]


# ============================================================
# 数据获取与组装
# ============================================================

def fetch_all(api_method, label):
    """翻页拉取全部数据，返回 items 列表"""
    page_size = 500        # 中台单页上限
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

        if len(all_items) >= total_num:
            break
        page_num += 1

    print(f"    {label} 完成，共 {len(all_items)} 条")
    return all_items



def assemble(meta_rows, data_rows):
    """
    将 meta + data 组装为前端 categories JSON 结构

    meta_rows:   [{sheet_name, pic_title, pic_type, legend_name, display_type, y_axis, unit}, ...]
    data_rows:   [{pic_title, legend_name, date, value}, ...]
    """
    # 1. 建立 meta 索引: (pic_title, legend_name) → {sheet_name, display_type, y_axis, unit, ...}
    meta_map = {}
    for m in meta_rows:
        key = (m["pic_title"], m["legend_name"])
        meta_map[key] = {
            "sheet_name":  m["sheet_name"],
            "pic_type":    m["pic_type"],
            "display_type":  m["display_type"],
            "y_axis":      m["y_axis"],
            "unit":        m["unit"],
            "sort_order":  m.get("sort_order"),
        }

    # 2. 补全 data 行: 合并 meta 信息
    enriched = []
    for d in data_rows:
        key = (d["pic_title"], d["legend_name"])
        if key in meta_map:
            d.update(meta_map[key])#补全操作，补上date和value
        enriched.append(d)

    # 3. 按 sheet_name 分组
    sheet_groups = {}
    for row in enriched:
        sn = row.get("sheet_name", "未知")
        sheet_groups.setdefault(sn, []).append(row)

    # 4. 按 CATEGORIES 硬编码结构组装 sheet_data
    sheet_data_all = {}

    for cat in CATEGORIES: #所有大类别下数据的sheet分类
        cat_all_dates = []  # 收集该分类下所有 sheet 的全部起止日期
        for sheet_info in cat["sheets"]:
            sheet_name = sheet_info["name"]
            rows = sheet_groups.get(sheet_name)
            if rows:
                pics, dr = _rows_to_pics(rows)
                sheet_data_all[sheet_name] = {"pics": pics, "source": sheet_info.get("source", "")}
                if dr:
                    parts = dr.split(" ~ ")
                    cat_all_dates.extend(parts)
                # 国家分组：用于二级侧边栏
                if sheet_info.get("children"):
                    country_map = {}
                    for p in pics:
                        c = _extract_country(p["title"], sheet_info["children"])
                        country_map.setdefault(c, []).append(p["title"])
                    sheet_data_all[sheet_name]["country_pics"] = country_map
                pic_info = [(p["type"], p["title"], len(p.get("dates", [])) or len(p.get("bars", [])) or len(p.get("series", []))) for p in pics]
                print(f"    [{sheet_name}] {len(pics)} pics: {pic_info}")
            else:
                sheet_data_all[sheet_name] = None
                print(f"    [{sheet_name}] 无数据")
        # 该分类日期范围 = 所有 sheet 中最早 ~ 最晚
        if cat_all_dates:
            cat["dateRange"] = f"{min(cat_all_dates)} ~ {max(cat_all_dates)}"

    # 5. 输出最终 JSON
    categories_out = []
    for cat in CATEGORIES:
        sheet_infos = [{"name": s["name"], "children": s.get("children", []),
                        "children_source": s.get("children_source", "")} for s in cat["sheets"] if not s.get("hidden")]
        sheet_names = [s["name"] for s in sheet_infos]
        all_data_names = sheet_names + [s.get("children_source", "") for s in cat["sheets"] if s.get("children_source")]
        categories_out.append({
            "name":      cat["name"],
            "sheets":    sheet_names,
            "sheetInfos": sheet_infos,
            "dateRange": cat.get("dateRange", ""),
            "sheetData": {sn: sheet_data_all.get(sn) for sn in set(all_data_names) if sn},
        })

    return {"categories": categories_out}


def _extract_country(title, countries):
    """从 pic_title 中提取国家名。如“法国新能源车销量” → “法国”"""
    for c in countries:
        if c in title:
            return c
    return title  # 兜底：整个 title 作为组名


def _rows_to_pics(rows):
    """
    将同一个 sheet 的扁平行按 pic_title 分组 → 转成前端 pics 结构
    返回: (pics_list, date_range_str)
    """
    groups = {}
    for r in rows:
        key = r["pic_title"]
        if key not in groups:
            groups[key] = {"type": r["pic_type"], "title": key, "rows": []}
        groups[key]["rows"].append(r)

    pics = []
    global_dates = None

    for title, g in groups.items():
        pic = {"type": g["type"], "title": title}
        pic_rows = g["rows"]

        if g["type"] == "mixed":
            # 收集唯一日期并排序
            dates = sorted(set(r["date"] for r in pic_rows))
            pic["dates"] = dates
            if global_dates is None:
                global_dates = dates

            # 拆分 bars 和 lines（同比/环比值需 ×100 转百分比）
            # 按 sort_order 排序，无 sort_order 则按字母
            def _sort_key(name):
                order = next((r.get("sort_order") for r in pic_rows if r["legend_name"] == name and r.get("sort_order") is not None), None)
                return (order if order is not None else 999, name)

            # 区分 bar 和 line
            bar_names = sorted(set(r["legend_name"] for r in pic_rows if r["display_type"] != "line"), key=_sort_key)
            line_names = sorted(set(r["legend_name"] for r in pic_rows if r["display_type"] == "line"), key=_sort_key)

            bars = []
            bar_disp = {}  # legend_name → display_type
            for r in pic_rows:
                if r["display_type"] != "line":
                    bar_disp[r["legend_name"]] = r["display_type"]
            for name in bar_names:
                data_map = {r["date"]: r["value"] for r in pic_rows if r["legend_name"] == name}
                bars.append({"name": name, "display_type": bar_disp.get(name, "bar_stacked"),
                             "data": [data_map.get(d) for d in dates]})
            pic["bars"] = bars

            lines = []
            for name in line_names:
                data_map = {r["date"]: r["value"] for r in pic_rows if r["legend_name"] == name}
                lines.append({"name": name, "data": [round(data_map[d] * 100, 1) if data_map.get(d) is not None else None for d in dates]})
            pic["lines"] = lines

            # 提取左右轴的单位
            bar_units = set(r["unit"] for r in pic_rows if r["display_type"] != "line")
            line_units = set(r["unit"] for r in pic_rows if r["display_type"] == "line")
            pic["left_unit"] = bar_units.pop() if bar_units else "万辆"
            pic["right_unit"] = line_units.pop() if line_units else "%"

        elif g["type"] == "bar":
            # 纯柱状图（堆积/簇状/单柱），无折线，单 Y 轴
            dates = sorted(set(r["date"] for r in pic_rows))
            pic["dates"] = dates
            if global_dates is None:
                global_dates = dates

            def _sort_key(name):
                order = next((r.get("sort_order") for r in pic_rows if r["legend_name"] == name and r.get("sort_order") is not None), None)
                return (order if order is not None else 999, name)

            bar_names = sorted(set(r["legend_name"] for r in pic_rows if r["display_type"] != "line"), key=_sort_key)
            bar_disp = {}
            for r in pic_rows:
                if r["display_type"] != "line":
                    bar_disp[r["legend_name"]] = r["display_type"]
            bars = []
            for name in bar_names:
                data_map = {r["date"]: r["value"] for r in pic_rows if r["legend_name"] == name}
                bars.append({"name": name, "display_type": bar_disp.get(name, "bar_stacked"),
                             "data": [data_map.get(d) for d in dates]})
            pic["bars"] = bars

            bar_units = set(r["unit"] for r in pic_rows if r["display_type"] != "line")
            pic["left_unit"] = bar_units.pop() if bar_units else ""

        elif g["type"] == "line":
            # 纯折线，x 轴按 date 字段（月份格式自动按 1,2,3...12 排序）
            pen_units = set(r["unit"] for r in pic_rows)
            pic["unit"] = pen_units.pop() if pen_units else "%"
            dates = sorted(set(r["date"] for r in pic_rows),
                           key=lambda d: int(d.replace("月", "")) if d.endswith("月") else d)
            pic["dates"] = dates
            if global_dates is None:
                global_dates = dates
            legend_names = sorted(set(r["legend_name"] for r in pic_rows))
            series_list = []
            need_pct = pic["unit"] == "%"  # 仅渗透率等比率数据 ×100
            for name in legend_names:
                data_map = {r["date"]: r["value"] for r in pic_rows if r["legend_name"] == name}
                if need_pct:
                    series_list.append({"name": name, "data": [round(data_map[d] * 100, 2) if data_map.get(d) is not None else None for d in dates]})
                else:
                    series_list.append({"name": name, "data": [data_map.get(d) for d in dates]})
            pic["series"] = series_list

        pics.append(pic)

    # mixed → bar → line 排序
    type_order = {"mixed": 0, "bar": 1, "line": 2}
    pics.sort(key=lambda p: type_order.get(p.get("type"), 9))

    # 日期范围
    if global_dates:
        date_range = f"{global_dates[0]} ~ {global_dates[-1]}"
    else:
        date_range = ""

    return pics, date_range


# ============================================================
# 主流程
# ============================================================

def _build_render_js(categories):
    """从 CATEGORIES 自动生成所有 sheet 的 RENDER_MAP 注册 JS"""
    lines = []
    for cat in categories:
        for s in cat.get("sheets", []):
            lines.append(f"RENDER_MAP['{s['name']}'] = renderPics;")
    return "\n".join(lines)


def main():
    # ---------- 1. 连接 API ----------
    print("[1/4] 连接 API...")
    api = AirWorksApi(**API_CONFIG)

    # ---------- 2. 获取数据 ----------
    print("[2/4] 获取数据...")
    all_meta = []
    all_data = []

    for cat in CATEGORIES:
        if not cat.get("sheets"):
            continue
        print(f"  [{cat['name']}]")
        if cat.get("api_structure"):
            meta = fetch_all(getattr(api, cat["api_structure"]), f"{cat['name']}-meta")
            all_meta.extend(meta)
        if cat.get("api_value"):
            data = fetch_all(getattr(api, cat["api_value"]), f"{cat['name']}-data")
            all_data.extend(data)

    print(f"\n  合计: {len(all_meta)} 条元数据, {len(all_data)} 条数据点")

    # ---------- 3. 组装 JSON ----------
    print("[3/4] 组装数据...")
    json_data = assemble(all_meta, all_data)
    json_str = json.dumps(json_data, ensure_ascii=False)

    # 打印各分类统计
    for cat in json_data["categories"]:
        sheet_count = sum(1 for v in cat["sheetData"].values() if v is not None)
        print(f"  {cat['name']}: {len(cat['sheets'])} sheets, {sheet_count} 已上线")

    # ---------- 4. 生成 HTML ----------
    print("[4/4] 生成 HTML...")
    render_js = _build_render_js(CATEGORIES)
    html = generate_html(json_str, render_js)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    file_size = os.path.getsize(OUTPUT_HTML)
    print(f"\n[Done] Output: {OUTPUT_HTML}")
    print(f"   Size: {file_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
