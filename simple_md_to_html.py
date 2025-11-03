#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

def markdown_to_html(md_content):
    """
    简单的Markdown到HTML转换器
    """
    html = md_content
    
    # 转换标题
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 转换表格
    lines = html.split('\n')
    new_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                new_lines.append('<div class="table-container">')
                new_lines.append('<table border="1">')
                in_table = True
                # 检查是否是表头
                if i + 1 < len(lines) and '---' in lines[i + 1]:
                    # 这是表头
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    new_lines.append('<tr>')
                    for cell in cells:
                        new_lines.append(f'<th>{cell}</th>')
                    new_lines.append('</tr>')
                else:
                    # 这是普通行
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    new_lines.append('<tr>')
                    for cell in cells:
                        new_lines.append(f'<td>{cell}</td>')
                    new_lines.append('</tr>')
            elif '---' in line:
                # 跳过分隔符行
                continue
            else:
                # 表格数据行
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                new_lines.append('<tr>')
                for cell in cells:
                    new_lines.append(f'<td>{cell}</td>')
                new_lines.append('</tr>')
        else:
            if in_table:
                new_lines.append('</table>')
                new_lines.append('</div>')
                in_table = False
            
            # 转换段落 - 忽略空行和单独的换行
            if line.strip() and not line.startswith('<'):
                new_lines.append(f'<p>{line}</p>')
            elif line.strip() and line.startswith('<'):
                # 保留已转换的HTML标签（包括标题）
                new_lines.append(line)
            # 不再添加空的br标签或空行
    
    # 如果文件结束时还在表格中
    if in_table:
        new_lines.append('</table>')
        new_lines.append('</div>')
    
    return '\n'.join(new_lines)

def create_html_file(md_file_path, html_file_path=None):
    """
    创建HTML文件
    """
    if html_file_path is None:
        html_file_path = os.path.splitext(md_file_path)[0] + '.html'
    
    try:
        # 读取Markdown文件
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为HTML
        html_content = markdown_to_html(md_content)
        
        # 创建简单的HTML文档
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>第三方SDK共享清单</title>
    <style>
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        h2 {{
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        .table-container {{
            width: 100%;
            overflow-x: auto;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 800px; /* 设置表格最小宽度，确保内容可读 */
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
            vertical-align: top;
            white-space: nowrap; /* 防止文字换行，保持列宽一致 */
        }}
        th {{
            font-weight: bold;
        }}
        /* 对于信息范围列，允许文字换行以适应内容 */
        td:nth-child(4) {{
            white-space: normal;
            word-wrap: break-word;
            max-width: 300px;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # 写入HTML文件
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ 成功转换：{md_file_path} -> {html_file_path}")
        return html_file_path
        
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {md_file_path}")
        return None
    except Exception as e:
        print(f"❌ 转换失败：{str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python simple_md_to_html.py <markdown_file_path> [html_file_path]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    html_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = create_html_file(md_file, html_file)
    if result:
        print(f"HTML文件已生成：{result}") 