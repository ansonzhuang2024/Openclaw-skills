---
name: echarts-tools
description: 根据用户需求和提供的数据，生成包含完整业务数据的 ECharts HTML 图表代码，并将 HTML 文件保存在本地。当用户提供数据并要求制作可视化图表（折线图、柱状图、饼图、地图等）、生成ECharts图表时触发。
---

# ECharts 图表生成工具 (echarts-tools)

本技能用于根据用户提供的数据生成对应的 ECharts HTML 代码，将文件保存在本地，并返回绝对路径供用户在浏览器中直接打开。

## 1. 生成 ECharts HTML 代码

在生成 HTML 源码时，必须严格遵守以下要求：

1. **数据集必须完整**，呈现所有符合用户要求的原始记录，禁止使用省略符或示例数据占位。
2. 使用 **ECharts 5.4.3 版本**，请使用公网 CDN 数据源，支持 ES Modules 模块化引入（如官网示例）或传统的 `<script>` 引入：
   - **ES Modules 方式（推荐）**:
     ```html
     <script type="importmap">
       {
         "imports": {
           "echarts": "https://fastly.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.esm.min.js"
         }
       }
     </script>
     <script type="module">
       import * as echarts from 'echarts';
       var chartDom = document.getElementById('main');
       var myChart = echarts.init(chartDom);
       // ... 图表配置
     </script>
     ```
   - **传统引入方式**: `<script src="https://fastly.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>`
3. 如需引用词云图JS文件，请使用以下公网数据源：
   - `https://fastly.jsdelivr.net/npm/echarts-wordcloud@2.1.0/dist/echarts-wordcloud.min.js`
4. 如需引用水滴图JS文件，请使用以下公网数据源：
   - `https://fastly.jsdelivr.net/npm/echarts-liquidfill@3.1.0/dist/echarts-liquidfill.min.js`
5. 如需引用3D图表JS文件，请使用以下公网数据源：
   - `https://fastly.jsdelivr.net/npm/echarts-gl@2.0.9/dist/echarts-gl.min.js`
6. 如需使用 jQuery，请使用以下公网数据源（对应 jQuery 3.2.1）：
   - `https://fastly.jsdelivr.net/npm/jquery@3.2.1/dist/jquery.min.js`
   - **务必**在 HTML 的 `<head>` 标签内引用 jQuery 文件。
7. 如需使用 SheetJS，请使用以下公网数据源（对应 sheetjs 0.18.5）：
   - `https://fastly.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js` 
8. 如需引用世界地图、中国地图或中国省市地图，请使用 JSON 方式异步加载地图数据（ECharts 4 版本遗留的开源地图文件），数据源如下：
   - `https://fastly.jsdelivr.net/npm/echarts@4.9.0/map/json/world.json`
   - `https://fastly.jsdelivr.net/npm/echarts@4.9.0/map/json/china.json`
   - `https://fastly.jsdelivr.net/npm/echarts@4.9.0/map/json/province/{中国省份}.json`（其中中国省份的拼音如“广东省”对应的文件名称为 `guangdong.json`）
9. 图表必须包含所有符合用户需求的数据，**不得只展示部分示例数据**。
10. 图表中需要文字展示的地方，**默认使用中文**。
11. 图表应 **自适应大小**。
12. 生成的图表大小应 **适中**。
13. 生成地图代码时，`data` 参数中的名称 `name` 必须按以下规则转换为地图能识别的标准名称：
    - 世界地图中，国家名称需转换为标准英文名称，例如：'日本' 转换为 'Japan'。
    - 中国地图中，省份名称需转换为标准简称，例如：'广东省' 转换为 '广东'。
    - 各省级地图中，市名称需转换为标准中文全称，例如：'深圳' 转换为 '深圳市'。
14. 使用世界地图生成代码时，地图上国家的名称 **默认不展示**。
15. JavaScript代码中不要使用中文变量名。
16. 容器高度必须固定（px）或百分比且 `html`, `body` 都必须设置高度百分比，避免图表空白。
17. 处理 Excel、CSV 或其他表格中的中文数据时，优先使用脚本在程序内部直接完成解析、聚合、JSON构造和 HTML 写入；**禁止依赖终端打印结果后再人工抄写回图表代码**，因为终端显示可能乱码但底层字符串仍然正确。
18. 模型生成的水球图的 `series` 必须参考以下结构：
```javascript
series: [{
  type: 'liquidFill',
  data: [0.8],
  radius: '70%',
  backgroundStyle: { color: '#E8F4FF' },
  itemStyle: { shadowBlur: 0, opacity: 0.95 },
  outline: { show: false },
  label: {
    fontSize: 28,
    color: '#1890FF',
    formatter: function(param) {
      return (param.value * 100).toFixed(0) + '%';
    }
  }
}]
```

⚠️ **重要异常处理**：
如用户提供的数据无法生成图表代码，请停止后续操作，并**直接回复**：
“提供的数据格式无法生成对应的图表，请检查后重新提供。”

## 2. 本地保存 HTML 文件

1. 将生成的完整 HTML 代码保存在本地当前工作区（即 `C:\Users\z00021142\.openclaw\workspace\`）或用户指定的目录中。
2. 为文件指定一个直观且具有辨识度的名字（例如：`echarts_饼图_汇总.html`）。
3. **绝对不要**调用原有的发布脚本将其推送到云端。保证数据和文件完全留在本地电脑上，组件直接依赖公网 CDN。

## 3. 响应用户

向用户输出该本地 HTML 文件的绝对路径（使用 `file:///` 格式，便于直接点击），并告知图表文件已成功生成并保存在本地，双击即可在浏览器中打开预览。