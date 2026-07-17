"""
公共模块 — CSS、HTML 骨架、工具函数
"""
import sys, io

# 确保 stdout/stderr 使用 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# ============================================================
# CSS 样式
# ============================================================

CSS = '''<style>
:root{
  --bg:#E8F2F8; --panel:#ffffff; --panel2:#F2F7FA; --line:#D4E2EC;
  --txt:#367198; --sub:#5a7d99; --accent:#C00000; --accent2:#1a3a6b;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:linear-gradient(180deg,#F2F7FA 0%,#E8F2F8 45%,#F0F5F9 100%) fixed;color:var(--txt);font-family:"Microsoft YaHei","PingFang SC",-apple-system,Segoe UI,sans-serif;padding:24px 48px 60px}
h1{font-size:24px;font-weight:700;letter-spacing:.5px;color:var(--accent2)}
.meta{color:var(--sub);font-size:13px;margin-top:6px;line-height:1.7}
.meta b{color:var(--txt)}
.tnav{display:flex;gap:6px;margin:14px 0 4px;flex-wrap:wrap}
.tbtn{
  font-size:15px;font-weight:600;color:var(--sub);background:#ffffff;
  border:1px solid var(--line);border-radius:10px;padding:8px 18px;cursor:pointer;
  transition:.15s;box-shadow:0 2px 8px rgba(26,58,107,.06);font-family:inherit;
}
.tbtn:hover{color:var(--txt)}
.tbtn.active{color:#fff;background:linear-gradient(135deg,#367198,#FF8080);border-color:transparent;box-shadow:0 4px 14px rgba(54,113,152,.3)}
.main-area{display:flex;gap:18px;margin-top:10px;min-height:500px;width:100%}
.content-area{flex:1;min-width:0;width:0}
.sidebar{display:flex;flex-direction:column;gap:0;min-width:150px;max-width:170px;flex-shrink:0;padding-top:24px;position:sticky;top:10px;align-self:flex-start;max-height:calc(100vh - 20px);overflow-y:auto}
.sbtn{
  font-size:13px;font-weight:500;color:var(--sub);background:transparent;
  border:none;border-left:3px solid transparent;border-radius:0;padding:9px 14px;cursor:pointer;
  transition:.15s;font-family:inherit;text-align:left;white-space:nowrap;
}
.sbtn:hover{color:var(--txt);background:var(--panel2);border-left-color:#B4CAD8}
.sbtn.active{color:var(--accent2);background:var(--panel2);border-left-color:var(--accent);font-weight:600}
.schild{position:relative;display:none;padding:6px 12px 6px 32px!important;font-size:13px!important;font-weight:500!important;color:var(--sub);background:transparent;border:none;border-left:1px solid #d0dce6;border-radius:0;cursor:pointer;transition:.15s;font-family:inherit;text-align:left;white-space:nowrap;margin-left:14px}
.schild::before{content:'·';position:absolute;left:18px;color:#b0c0d0}
.schild.show{display:block}
.schild:hover{color:var(--txt);background:var(--panel2);border-left-color:#B4CAD8}
.schild.active{color:var(--accent2);background:var(--panel2);border-left-color:#FFB2B2!important;font-weight:600!important}
.schild:last-child{border-left:1px solid transparent;border-image:linear-gradient(to bottom,#d0dce6 0%,transparent 100%) 1}
.sec{font-size:18px;font-weight:700;margin:24px 0 8px;padding-left:11px;border-left:5px solid var(--accent2)}
.seclabel{font-size:14.5px;font-weight:700;color:var(--accent2);margin:20px 0 2px;padding-left:9px;border-left:4px solid var(--accent2)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:18px;margin-top:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px 8px;box-shadow:0 4px 16px rgba(26,58,107,.07)}
.card h2{font-size:16px;font-weight:600;margin-bottom:2px}
.card .ch{color:var(--sub);font-size:12.5px;margin-bottom:10px}
.chart{width:100%;height:380px}
.full{grid-column:1/-1}
footer{color:var(--sub);font-size:12px;margin-top:30px;line-height:1.8}
</style>'''


# ============================================================
# HTML 骨架
# ============================================================

HTML_HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
<title>锂电产业链数据跟踪</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
''' + CSS + '''
</head>
<body>
<script>if(screen.width<1024)document.write('<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#E8F1F7;z-index:99999;display:flex;align-items:center;justify-content:center;font:18px/1.8 sans-serif;color:#1a3a6b;text-align:center"><p>请使用电脑端访问<br>本页面仅支持电脑端浏览</p></div>'),document.close()</script>
<h1>【中信建投新能源】锂电产业链数据跟踪</h1>

<div class="tnav" id="tnav"></div>
<div class="meta" id="meta_info"></div>
<div class="main-area">
  <div class="sidebar" id="sidebar"></div>
  <div class="content-area" id="content"></div>
</div>

<footer>
  数据来源：<span id="footer_source"></span>，中信建投证券整理<br>
  注：本数据根据公开资料整理，不构成任何投资建议。
</footer>

<script>
// ===== 数据 =====
const RAW = __JSON__;

// ===== 全局 =====
const CHARTS_ARR = [];
const MONTHS = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
// 渗透率多年份折线配色（指定 5 色 + 蓝/粉系补充 5 色，共 10 色）
const PALETTE = [
  '#FF8080','#FFB2B2','#B4CAD8','#FF0000','#044E7E',
  '#6BA5C8','#FF9999','#4A8AB5','#DC143C','#FF7F7F'
];
const RENDER_MAP = {};

// ===== 渲染函数注册 =====
__RENDER_JS__

function mk(id, opt) {
  const el = document.getElementById(id);
  if (!el) return null;
  const ch = echarts.init(el);
  ch.setOption(opt);
  CHARTS_ARR.push(ch);
  return ch;
}

window.addEventListener('resize', function() { CHARTS_ARR.forEach(function(c) { c.resize(); }); });

// ===== 通用渲染函数（遍历 gd.pics，按 type 渲染） =====
function renderPics(gd) {
  var content = document.getElementById('content');
  var html = '';
  gd.pics.forEach(function(pic, bi) {
    html += '<div class="sec" style="border-color:var(--accent)">' + pic.title + '</div>';
    html += '<div class="grid"><div class="card full">';
    html += '<div class="ch">悬停图表显示具体数值</div>';
    html += '<div id="pic_' + bi + '" class="chart" style="height:420px"></div>';
    html += '<div class="ch" style="text-align:right;margin-top:2px;margin-bottom:0">来源：' + (gd.source || '') + '</div>';
    html += '</div></div>';
  });
  content.innerHTML = html;
  gd.pics.forEach(function(pic, bi) {
    var cid = 'pic_' + bi;
    if (pic.type === 'mixed') {
      var hasLines = pic.lines && pic.lines.length > 0;
      var series = [];
      var BAR_COLORS = pic.bars.length <= 3
        ? ['#FF8080','#B4CAD8','#FFB2B2']
        : ['#D4A5A5','#367198','#FF9999','#4A8AB5','#FFB2B2','#6BA5C8','#FFCCCC','#B4CAD8','#FFE5E5'];
      var LINE_COLORS = ['#044E7E', '#FF0000'];
      pic.bars.forEach(function(b, i) {
        var isStacked = b.display_type === 'bar_stacked';
        series.push({ name: b.name, type: 'bar', stack: isStacked ? 'total' : undefined, data: b.data, itemStyle: { color: BAR_COLORS[i % BAR_COLORS.length] }, emphasis: {} });
      });
      if (hasLines) {
        pic.lines.forEach(function(l, i) {
          series.push({ name: l.name, type: 'line', yAxisIndex: 1, data: l.data, smooth: true, showSymbol: false, lineStyle: { width: 1.5, color: LINE_COLORS[i % LINE_COLORS.length] }, itemStyle: { color: LINE_COLORS[i % LINE_COLORS.length] }, emphasis: {} });
        });
      }
      var ch = mk(cid, {
        color: PALETTE,
        tooltip: { trigger: 'axis', backgroundColor: '#ffffff', borderColor: '#B4CAD8', textStyle: { color: '#367198' },
          formatter: function(ps) {
            if (!ps.length) return '';
            var s = ps[0].axisValue + '<br>';
            ps.forEach(function(p) {
              if (p.value != null) {
                var unit = (p.seriesName.indexOf('同比') >= 0 || p.seriesName.indexOf('环比') >= 0) ? (pic.right_unit || '%') : ' ' + (pic.left_unit || '万辆');
                s += p.marker + p.seriesName + '：' + p.value.toFixed(2) + unit + '<br>';
              }
            });
            return s;
          }
        },
        legend: { top: 5, left: 'center', textStyle: { color: '#5a7d99' }, itemWidth: 18, itemHeight: 10 },
        grid: { left: 60, right: hasLines ? 65 : 20, top: 50, bottom: 45 },
        xAxis: { type: 'category', data: pic.dates, axisLine: { lineStyle: { color: '#B4CAD8' } }, axisLabel: { color: '#5a7d99', interval: 11 } },
        yAxis: hasLines ? [
          { type: 'value', name: pic.left_unit || '万辆', min: 0, splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } },
          { type: 'value', name: pic.right_unit || '%', min: 0, splitLine: { show: false }, axisLabel: { color: '#5a7d99' } }
        ] : [
          { type: 'value', name: pic.left_unit || '万辆', min: 0, splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } }
        ],
        dataZoom: [{ type: 'slider', start: 0, end: 100, height: 22, bottom: 10 }, { type: 'inside', start: 0, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true }],
        series: series
      });
      if (ch) { ch.on('datazoom', function(ev) { if (ev.batch) ev = ev.batch[0]; var v = ev.end - ev.start; var iv = v > 80 ? 11 : v > 40 ? 5 : v > 15 ? 2 : 0; ch.setOption({ xAxis: { axisLabel: { interval: iv } } }); }); }
    } else if (pic.type === 'bar') {
      var series = [];
      var BAR_COLORS = pic.bars.length <= 3
        ? ['#FF8080','#B4CAD8','#FFB2B2']
        : ['#D4A5A5','#367198','#FF9999','#4A8AB5','#FFB2B2','#6BA5C8','#FFCCCC','#B4CAD8','#FFE5E5'];
      pic.bars.forEach(function(b, i) {
        var isStacked = b.display_type === 'bar_stacked';
        series.push({ name: b.name, type: 'bar', stack: isStacked ? 'total' : undefined, data: b.data, itemStyle: { color: BAR_COLORS[i % BAR_COLORS.length] }, emphasis: {} });
      });
      var ch = mk(cid, {
        color: PALETTE,
        tooltip: { trigger: 'axis', backgroundColor: '#ffffff', borderColor: '#B4CAD8', textStyle: { color: '#367198' },
          formatter: function(ps) {
            if (!ps.length) return '';
            var s = ps[0].axisValue + '<br>';
            ps.forEach(function(p) {
              if (p.value != null) s += p.marker + p.seriesName + '：' + p.value.toFixed(2) + ' ' + (pic.left_unit || '') + '<br>';
            });
            return s;
          }
        },
        legend: { top: 5, left: 'center', textStyle: { color: '#5a7d99' }, itemWidth: 18, itemHeight: 10 },
        grid: { left: 60, right: 20, top: 50, bottom: 45 },
        xAxis: { type: 'category', data: pic.dates, axisLine: { lineStyle: { color: '#B4CAD8' } }, axisLabel: { color: '#5a7d99', interval: 11 } },
        yAxis: { type: 'value', name: pic.left_unit || '', min: 0, splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } },
        dataZoom: [{ type: 'slider', start: 0, end: 100, height: 22, bottom: 10 }, { type: 'inside', start: 0, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true }],
        series: series
      });
      if (ch) { ch.on('datazoom', function(ev) { if (ev.batch) ev = ev.batch[0]; var v = ev.end - ev.start; var iv = v > 80 ? 11 : v > 40 ? 5 : v > 15 ? 2 : 0; ch.setOption({ xAxis: { axisLabel: { interval: iv } } }); }); }
    } else if (pic.type === 'line') {
      var penSeries = (pic.series || []).map(function(s, yi) {
        var hot = yi === (pic.series.length - 1);
        return { name: s.name, type: 'line', data: s.data, connectNulls: false, symbol: 'circle',
          symbolSize: hot ? 6 : 4,
          lineStyle: { width: hot ? 3.5 : 1.8, color: PALETTE[yi % PALETTE.length] },
          itemStyle: { color: PALETTE[yi % PALETTE.length] },
          emphasis: {}, z: hot ? 10 : 1 };
      });
      var lineOpt = {
        color: PALETTE,
        tooltip: { trigger: 'axis', backgroundColor: '#ffffff', borderColor: '#B4CAD8', textStyle: { color: '#367198' },
          formatter: function(ps) {
            if (!ps.length) return '';
            var s = ps[0].axisValue + '<br>';
            ps.forEach(function(p) { s += p.marker + p.seriesName + '：' + (p.value != null ? p.value.toFixed(2) + (pic.unit || '%') : '-') + '<br>'; });
            return s;
          }
        },
        legend: { top: 5, left: 'center', textStyle: { color: '#5a7d99', fontSize: 11 }, inactiveColor: '#B4CAD8', itemWidth: 16, itemHeight: 8 },
        grid: { left: 55, right: 15, top: 40, bottom: pic.dates && pic.dates.length > 12 ? 45 : 28 },
        xAxis: { type: 'category', data: pic.dates || MONTHS, axisLine: { lineStyle: { color: '#B4CAD8' } }, axisLabel: { color: '#5a7d99', interval: pic.dates && pic.dates.length > 12 ? 11 : 0 } },
        yAxis: { type: 'value', name: pic.unit || '%', nameTextStyle: { color: '#5a7d99', padding: [0, 45, 0, 0] }, min: 0, splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } },
        series: penSeries
      };
      if (pic.dates && pic.dates.length > 12) {
        lineOpt.dataZoom = [{ type: 'slider', start: 0, end: 100, height: 22, bottom: 10 }, { type: 'inside', start: 0, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true }];
      }
      var ch = mk(cid, lineOpt);
      if (ch && pic.dates && pic.dates.length > 12) { ch.on('datazoom', function(ev) { if (ev.batch) ev = ev.batch[0]; var v = ev.end - ev.start; var iv = v > 80 ? 11 : v > 40 ? 5 : v > 15 ? 2 : 0; ch.setOption({ xAxis: { axisLabel: { interval: iv } } }); }); }
    }
  });
}

// ===== 一级导航（大分类） =====
(function() {
  var tnav = document.getElementById('tnav');
  var sidebar = document.getElementById('sidebar');
  var content = document.getElementById('content');
  var metaInfo = document.getElementById('meta_info');
  var currentTopCat = null;
  var currentSheet = null;

  // 渲染一级导航按钮
  RAW.categories.forEach(function(cat, i) {
    var btn = document.createElement('button');
    btn.className = 'tbtn' + (i === 0 ? ' active' : '');
    btn.textContent = cat.name;
    btn.addEventListener('click', function() {
      document.querySelectorAll('.tbtn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      switchCategory(cat);
    });
    tnav.appendChild(btn);
  });

  // 默认选中第一个大分类
  switchCategory(RAW.categories[0]);

  function switchCategory(cat) {
    currentTopCat = cat;
    metaInfo.innerHTML = cat.name + ' · 数据区间：<b>' + (cat.dateRange || '待录入') + '</b>';

    // 底部来源：收集该分类下所有 sheet 的 source 去重
    var sources = [];
    cat.sheets.forEach(function(sn) {
      var sd = cat.sheetData[sn];
      if (sd && sd.source && sources.indexOf(sd.source) < 0) sources.push(sd.source);
    });
    document.getElementById('footer_source').textContent = sources.join('、') || '';

    // 渲染二级导航（sheet 侧边栏 + 子项）
    sidebar.innerHTML = '';
    var infos = cat.sheetInfos || cat.sheets.map(function(s) { return {name: s, children: []}; });
    var isFirst = true;
    if (infos.length > 0) {
      infos.forEach(function(info) {
        var hasKids = info.children && info.children.length > 0;
        var btn = document.createElement('button');
        btn.className = 'sbtn' + (isFirst ? ' active' : '');
        btn.textContent = info.name + (hasKids ? ' ▸' : '');
        sidebar.appendChild(btn);

        var children = [];
        (info.children || []).forEach(function(child) {
          var cbtn = document.createElement('button');
          cbtn.className = 'schild';
          cbtn.textContent = child;
          cbtn.addEventListener('click', function(e) {
            e.stopPropagation();
            document.querySelectorAll('.sbtn,.schild').forEach(function(b) { b.classList.remove('active'); });
            btn.classList.add('active');
            cbtn.classList.add('active');
            var src = info.children_source || info.name;
            switchSheet(src, child);
          });
          children.push(cbtn);
          sidebar.appendChild(cbtn);
        });

        btn.addEventListener('click', function() {
          var showing = children.length > 0 && children[0].classList.contains('show');
          document.querySelectorAll('.sbtn,.schild').forEach(function(b) { b.classList.remove('active'); });
          document.querySelectorAll('.schild').forEach(function(b) { b.classList.remove('show'); });
          btn.classList.add('active');
          if (children.length > 0 && !showing) {
            btn.textContent = info.name + ' ▾';
            children.forEach(function(c) { c.classList.add('show'); });
            switchSheet(info.name);
          } else {
            btn.textContent = hasKids ? info.name + ' ▸' : info.name;
            switchSheet(info.name);
          }
        });
        isFirst = false;
      });
      switchSheet(infos[0].name);
    } else {
      content.innerHTML = '<div class="sec" style="margin-top:24px">' + cat.name + '</div><p style="color:var(--sub);margin-top:12px">数据模块正在建设中，敬请期待。</p>';
    }
  }

  function switchSheet(name, country) {
    currentSheet = name;
    // 清理旧图表
    CHARTS_ARR.forEach(function(c) { c.dispose(); });
    CHARTS_ARR.length = 0;

    var gd = currentTopCat.sheetData[name];
    var renderFn = RENDER_MAP[name] || (gd && gd.pics ? renderPics : null);
    if (renderFn && gd) {
      // 按国家过滤 pics
      if (country && gd.pics) {
        var filtered = {pics: gd.pics.filter(function(p) { return p.title.indexOf(country) >= 0; }), source: gd.source};
        renderFn(filtered);
      } else {
        renderFn(gd);
      }
    } else {
      content.innerHTML = '<div class="sec" style="margin-top:24px">' + name + '</div><p style="color:var(--sub);margin-top:12px">该模块正在建设中，敬请期待。</p>';
    }
  }
})();


</script>
</body>
</html>'''


# ============================================================
# HTML 生成
# ============================================================

def generate_html(json_str, render_js):
    """注入 JSON 数据和渲染 JS，返回完整 HTML"""
    html = HTML_HEAD.replace('__JSON__', json_str).replace('__RENDER_JS__', render_js)
    return html
