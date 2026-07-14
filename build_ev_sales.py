"""
新能源车销量模块 — JS 渲染函数
"""
# Excel 数据解析已迁移到 build.py 的 API 版本


# ============================================================
# JS 渲染函数
# ============================================================

def get_render_js():
    """返回此模块所有 sheet 的 JS 渲染函数 + 注册代码"""
    return '''
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
      var BAR_COLORS = ['#FF8080', '#B4CAD8', '#FFB2B2'];
      var LINE_COLORS = ['#FF0000', '#044E7E'];
      pic.bars.forEach(function(b, i) {
        series.push({ name: b.name, type: 'bar', stack: 'total', data: b.data, itemStyle: { color: BAR_COLORS[i % BAR_COLORS.length] }, emphasis: {} });
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
          { type: 'value', name: pic.left_unit || '万辆', splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } },
          { type: 'value', name: pic.right_unit || '%', splitLine: { show: false }, axisLabel: { color: '#5a7d99' } }
        ] : [
          { type: 'value', name: pic.left_unit || '万辆', splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } }
        ],
        dataZoom: [{ type: 'slider', start: 0, end: 100, height: 22, bottom: 10 }, { type: 'inside', start: 0, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true }],
        series: series
      });
      if (ch) { ch.on('datazoom', function(ev) { if (ev.batch) ev = ev.batch[0]; var v = ev.end - ev.start; var iv = v > 80 ? 11 : v > 40 ? 5 : v > 15 ? 2 : 0; ch.setOption({ xAxis: { axisLabel: { interval: iv } } }); }); }

    } else if (pic.type === 'penetration') {
      var penSeries = (pic.series || []).map(function(s, yi) {
        var hot = yi === (pic.series.length - 1);
        return { name: s.name, type: 'line', data: s.data, connectNulls: false, symbol: 'circle',
          symbolSize: hot ? 6 : 4,
          lineStyle: { width: hot ? 3.5 : 1.8, color: PALETTE[yi % PALETTE.length] },
          itemStyle: { color: PALETTE[yi % PALETTE.length] },
          emphasis: {}, z: hot ? 10 : 1 };
      });

      mk(cid, {
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
        grid: { left: 55, right: 15, top: 40, bottom: 28 },
        xAxis: { type: 'category', data: MONTHS, axisLine: { lineStyle: { color: '#B4CAD8' } }, axisLabel: { color: '#5a7d99' }, boundaryGap: false },
        yAxis: { type: 'value', name: pic.unit || '%', nameTextStyle: { color: '#5a7d99', padding: [0, 45, 0, 0] }, scale: true, splitLine: { lineStyle: { color: '#B5E1FD' } }, axisLabel: { color: '#5a7d99' } },
        series: penSeries
      });
    }
  });
}

// 所有 sheet 注册到同一个渲染函数
RENDER_MAP['全球销量-Marklines']      = renderPics;
RENDER_MAP['中国销量-中汽协']         = renderPics;
RENDER_MAP['中国销量-乘联会']         = renderPics;
RENDER_MAP['欧洲九国销量-各国官网']   = renderPics;
RENDER_MAP['欧洲九国销量-分国家']   = renderPics;
RENDER_MAP['欧洲销量-Marklines']      = renderPics;
RENDER_MAP['美国销量-Marklines']      = renderPics;
RENDER_MAP['日韩销量-Marklines']      = renderPics;
'''
