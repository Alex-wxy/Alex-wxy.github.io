# 锂电产业链数据看板

通过中台 API 获取新能源车销量、电池产销及装机、锂电材料价格及排产数据，自动生成静态 HTML 看板，部署于 GitHub Pages。

## 项目结构

```
Website/
├── build.py              # 入口：拉取 API → 组装 JSON → 生成 index.html
├── build_common.py       # 公共：CSS 样式、HTML 骨架、导航 JS
├── build_ev_sales.py     # 新能源车销量 JS 渲染函数
├── build_battery.py      # 电池产销及装机数据（占位）
├── build_material.py     # 锂电材料价格及排产数据（占位）
├── data/                 # Excel 数据源（历史，已废弃）
├── requirements.txt      # 依赖
├── index.html            # 构建输出（GitHub Pages 部署）
└── README.md
```

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

## 技术栈

- **后端**：Python + 中信建投中台 API（`shangjian_api`）
- **前端**：ECharts 5.5（CDN 加载）
- **部署**：GitHub Pages / 静态 HTML

## 数据来源

| 模块 | 来源 |
|------|------|
| 新能源车销量 | Marklines / 中汽协 / 乘联会 / 欧洲各国官网 |
| 电池产销及装机 | 待补充 |
| 锂电材料价格及排产 | 待补充 |
