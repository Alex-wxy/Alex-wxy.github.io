# build.py（临时版，纯验证流水线）

# 造假数据，什么都不依赖
fake_data = {
    "sites": [
        {"name": "测试", "url": "https://example.com", "score": 85},
        {"name": "测试网站B", "url": "https://example.org", "score": 72},
    ]
}
#test

# 把 JSON 数据转成 HTML 表格行
def build_table(sites):
    rows = ""
    for site in sites:
        rows += f"""
        <tr>
            <td>{site['name']}</td>
            <td><a href="{site['url']}" target="_blank">{site['url']}</a></td>
            <td>{site['score']}</td>
        </tr>"""
    return rows

# 生成 HTML
html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>网站对比</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
        }}
        h1 {{ text-align: center; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: 600;
        }}
        tr:hover {{ background-color: #fafafa; }}
        .update-time {{
            text-align: center;
            color: #999;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>网站对比结果</h1>
    <p class="update-time">最后更新：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <table>
        <thead>
            <tr>
                <th>网站名称</th>
                <th>网址</th>
                <th>评分</th>
            </tr>
        </thead>
        <tbody>
            {build_table(fake_data["sites"])}
        </tbody>
    </table>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 已生成")
