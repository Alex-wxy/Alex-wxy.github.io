# 锂电产业链数据看板

通过中台 API 获取新能源车销量、电池产销及装机、锂电材料价格及排产数据，自动生成静态 HTML 看板，部署于 GitHub Pages。

## 项目结构

```
Website/
├── build.py              # 入口：API 配置、CATEGORIES 导航、数据拉取组装、RENDER_MAP 生成
├── build_common.py       # 公共：CSS 样式、HTML 骨架、导航 JS、renderPics 通用渲染
├── data/                 # Excel 数据源（历史，已废弃）
├── requirements.txt      # 依赖
├── index.html            # 构建输出（GitHub Pages 部署）
└── README.md
```

新增 sheet 只需在 `build.py` 的 `CATEGORIES` 加一行，侧边栏和图表自动生效。

## 环境要求

- Python 3.10 / 3.11（3.12 的 OpenSSL 3.0 与中信建投内网不兼容）
- 公司 VPN（API 为内网地址 `rds.csc.com.cn`）

## 快速开始

```bash
# 创建虚拟环境
py -3.10 -m venv venv
source venv/Scripts/activate

# 安装依赖
pip install -r requirements.txt

# 运行构建
python build.py
```

构建完成后打开 `index.html` 即可在浏览器中查看。

## 数据流

```
中台 API (三个分类各一对接口)
  │  structure + value
  │  series_meta + data_points
  ▼
build.py
  │  join by (pic_title, legend_name)
  │  按 sheet_name → pic_title 分组
  │  按 pic_type + display_type 组装
  ▼
JSON → 注入 HTML 模板
  │
  ▼
index.html (静态文件，GitHub Pages 部署)
  │  renderPics() 按 type 渲染 ECharts
  │  mixed → 堆积/簇状柱 + 折线
  │  bar   → 纯柱状图
  │  line  → 纯折线（月份/日期）
```

## 技术栈

- **后端**：Python + 中信建投中台 API（`shangjian_api`）
- **前端**：ECharts 5.5（CDN 加载）
- **部署**：GitHub Pages / 静态 HTML

## 数据来源

| 模块 | 来源 |
|------|------|
| 新能源车销量 | Marklines / 中汽协 / 乘联会 / 欧洲各国官网 |
| 电池产销及装机 | 暂未给出 |
| 锂电材料价格及排产 | 暂未给出 |
