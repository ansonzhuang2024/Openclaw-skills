import sys
import json
import urllib.request
import urllib.error

def publish_chart(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # 读取完毕后删除该临时文件，避免污染用户本地环境
        import os
        try:
            os.remove(file_path)
        except Exception as e:
            pass # 忽略删除失败的错误
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    url = "http://10.61.133.33:3001/generate"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "202512311qazxsw2"
    }
    data = json.dumps({"content": html_content}).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode('utf-8')
            res_json = json.loads(res_data)
            
            # 先尝试直接获取 url (某些环境可能直返)
            chart_url = res_json.get("url")
            
            if not chart_url:
                # 尝试从 body 字段中解析出嵌套的 json 字符串
                body_str = res_json.get("body", "{}")
                if isinstance(body_str, str):
                    try:
                        body_json = json.loads(body_str)
                        chart_url = body_json.get("url")
                    except Exception:
                        pass
                elif isinstance(body_str, dict):
                    chart_url = body_str.get("url")
            
            if chart_url:
                print(chart_url) # 只打印URL供大模型提取
            else:
                print(f"Failed to extract URL. Response API: {res_data}")
                
    except urllib.error.URLError as e:
        print(f"HTTP Request Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python publish_chart.py <path_to_html_file>")
        sys.exit(1)
        
    publish_chart(sys.argv[1])
