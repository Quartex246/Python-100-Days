#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 Python-100-Days Obsidian 库建立关系图谱
- 为每篇文章添加 YAML frontmatter
- 在文末添加相关文章链接
- 创建 MOC (Map of Content) 索引页
- 修复 README 中的错误链接
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# 库的根目录
VAULT_ROOT = Path(r"C:\Users\Morphius\Documents\GitHub\Python-100-Days")

# 课程阶段定义
STAGES = {
    "Day01-20": {
        "name": "Python语言基础",
        "days": list(range(1, 21)),
        "tags": ["Python基础", "入门"],
    },
    "Day21-30": {
        "name": "Python语言应用",
        "days": list(range(21, 31)),
        "tags": ["Python应用", "文件处理"],
    },
    "Day31-35": {
        "name": "其他相关内容",
        "days": [31, 32, 33, 34, 35],
        "tags": ["进阶", "Web前端", "Linux"],
    },
    "Day36-45": {
        "name": "数据库基础和进阶",
        "days": list(range(36, 46)),
        "tags": ["数据库", "MySQL", "SQL"],
    },
    "Day46-60": {
        "name": "实战Django",
        "days": list(range(46, 61)),
        "tags": ["Django", "Web开发", "后端"],
    },
    "Day61-65": {
        "name": "网络数据采集",
        "days": list(range(61, 66)),
        "tags": ["爬虫", "数据采集"],
    },
    "Day66-80": {
        "name": "Python数据分析",
        "days": list(range(66, 81)),
        "tags": ["数据分析", "NumPy", "pandas", "可视化"],
    },
    "Day81-90": {
        "name": "机器学习",
        "days": list(range(81, 91)),
        "tags": ["机器学习", "AI"],
    },
    "Day91-100": {
        "name": "团队项目开发",
        "days": list(range(91, 101)),
        "tags": ["项目实战", "工程化"],
    },
}

# 文件映射：day number -> 实际文件名
FILE_MAP = {}


def build_file_map():
    """构建 day number 到文件名的映射"""
    for stage_dir, stage_info in STAGES.items():
        stage_path = VAULT_ROOT / stage_dir
        if not stage_path.exists():
            continue

        for md_file in stage_path.glob("*.md"):
            # 提取文件名中的数字
            match = re.match(r"(\d+)", md_file.stem)
            if match:
                day_num = int(match.group(1))
                # 处理同一天多个文件的情况（如 Day62, Day63）
                if day_num not in FILE_MAP:
                    FILE_MAP[day_num] = []
                FILE_MAP[day_num].append({
                    "path": md_file,
                    "stage": stage_dir,
                    "stage_name": stage_info["name"],
                    "tags": stage_info["tags"],
                })


def extract_title(file_path: Path) -> str:
    """从文件中提取标题"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 查找第一个 ## 标题
    match = re.search(r"^##\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # 如果没有 ## 标题，使用文件名
    return file_path.stem


def has_frontmatter(content: str) -> bool:
    """检查文件是否已有 frontmatter"""
    return content.strip().startswith("---")


def add_frontmatter(file_path: Path, frontmatter: Dict) -> str:
    """为文件添加或更新 frontmatter"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 如果已有 frontmatter，替换它
    if has_frontmatter(content):
        # 找到第二个 --- 之后的内容
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].lstrip("\n")

    # 构建 YAML frontmatter
    yaml_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            yaml_lines.append(f"{key}:")
            for item in value:
                yaml_lines.append(f"  - {item}")
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---")
    yaml_lines.append("")

    return "\n".join(yaml_lines) + content


def get_related_files(day_num: int, stage: str) -> List[Dict]:
    """获取相关文章"""
    related = []

    # 同阶段的前后文章
    stage_info = STAGES.get(stage, {})
    stage_days = stage_info.get("days", [])

    if day_num in stage_days:
        idx = stage_days.index(day_num)
        # 前一篇文章
        if idx > 0:
            prev_day = stage_days[idx - 1]
            if prev_day in FILE_MAP:
                for f in FILE_MAP[prev_day]:
                    related.append({**f, "relation": "prev"})
        # 后一篇文章
        if idx < len(stage_days) - 1:
            next_day = stage_days[idx + 1]
            if next_day in FILE_MAP:
                for f in FILE_MAP[next_day]:
                    related.append({**f, "relation": "next"})

    # 跨阶段的关联文章
    cross_refs = get_cross_references(day_num)
    related.extend(cross_refs)

    return related


def get_cross_references(day_num: int) -> List[Dict]:
    """获取跨阶段的相关文章"""
    refs = []

    # 定义跨阶段关联规则
    cross_rules = {
        # Day21 (文件读写) -> Day30 (正则表达式)
        21: [30],
        # Day30 (正则表达式) -> Day62 (爬虫解析)
        30: [62],
        # Day44 (Python接入MySQL) -> Day46-60 (Django)
        44: [46, 47],
        # Day54-55 (RESTful) -> Day94 (API设计)
        54: [94],
        55: [94],
        # Day58 (异步任务) -> Day95 (商业项目)
        58: [95],
        # Day59 (单元测试) -> Day95, Day96 (测试)
        59: [95, 96],
        # Day60 (项目上线) -> Day98 (部署)
        60: [98],
        # Day62-63 (爬虫) -> 番外篇:常见反爬策略
        62: [999],  # 特殊标记，表示番外篇
        63: [999],
        # Day68-71 (NumPy) -> Day72-77 (pandas)
        71: [72],
        # Day77 (pandas索引) -> Day78-80 (可视化)
        77: [78],
        # Day81-89 (机器学习算法) -> Day90 (实战)
        89: [90],
        # Day92 (Docker) -> Day98 (部署)
        92: [98],
        # Day93 (MySQL优化) -> Day36 (MySQL概述)
        93: [36],
        # Day95 (Django商业项目) -> Day46-60 (Django)
        95: [46, 60],
        # Day96 (测试) -> Day59 (单元测试)
        96: [59],
        # Day98 (部署) -> Day60, Day92
        98: [60, 92],
    }

    if day_num in cross_rules:
        for ref_day in cross_rules[day_num]:
            if ref_day == 999:
                # 番外篇特殊处理
                fanwai_path = VAULT_ROOT / "番外篇" / "常见反爬策略及应对方案.md"
                if fanwai_path.exists():
                    refs.append({
                        "path": fanwai_path,
                        "stage": "番外篇",
                        "stage_name": "番外篇",
                        "tags": ["爬虫", "反爬"],
                        "relation": "related",
                    })
            elif ref_day in FILE_MAP:
                for f in FILE_MAP[ref_day]:
                    refs.append({**f, "relation": "related"})

    return refs


def add_related_section(file_path: Path, related: List[Dict]) -> str:
    """在文件末尾添加相关文章区块（从文件读取）"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return add_related_section_to_content(content, related)


def add_related_section_to_content(content: str, related: List[Dict]) -> str:
    """在内容末尾添加相关文章区块（操作字符串）"""
    if not related:
        # 如果没有相关文章但有旧区块，删除它
        if "## 相关文章" in content:
            idx = content.index("## 相关文章")
            content = content[:idx].rstrip() + "\n"
        return content

    # 如果已有相关文章区块，先删除它
    if "## 相关文章" in content:
        idx = content.index("## 相关文章")
        content = content[:idx].rstrip()

    # 构建相关文章区块
    lines = ["", "", "## 相关文章", ""]

    # 按关系类型分组
    prev_files = [r for r in related if r.get("relation") == "prev"]
    next_files = [r for r in related if r.get("relation") == "next"]
    other_files = [r for r in related if r.get("relation") == "related"]

    if prev_files:
        lines.append("**上一篇：**")
        for f in prev_files:
            rel_path = str(f["path"].relative_to(VAULT_ROOT)).replace("\\", "/")
            title = extract_title(f["path"])
            lines.append(f"- [[{rel_path}|{title}]]")
        lines.append("")

    if next_files:
        lines.append("**下一篇：**")
        for f in next_files:
            rel_path = str(f["path"].relative_to(VAULT_ROOT)).replace("\\", "/")
            title = extract_title(f["path"])
            lines.append(f"- [[{rel_path}|{title}]]")
        lines.append("")

    if other_files:
        lines.append("**相关推荐：**")
        for f in other_files:
            rel_path = str(f["path"].relative_to(VAULT_ROOT)).replace("\\", "/")
            title = extract_title(f["path"])
            lines.append(f"- [[{rel_path}|{title}]]")
        lines.append("")

    return content + "\n".join(lines)


def create_moc_files():
    """创建 MOC (Map of Content) 索引文件"""

    # 1. 创建总导航页
    main_moc_path = VAULT_ROOT / "Python学习路线图.md"
    main_moc_content = """---
title: Python学习路线图
tags:
  - MOC
  - 导航
---

# Python学习路线图

> 本文是 Python-100天从新手到大师 课程的学习路线图，帮助你系统地学习 Python。

## 课程概览

本课程分为以下阶段：

### 第一阶段：Python语言基础
- **时间**：Day01-20
- **内容**：Python 基础语法、数据类型、控制结构、函数、面向对象
- **MOC**：[[Day01-20/MOC|Python语言基础 MOC]]

### 第二阶段：Python语言应用
- **时间**：Day21-30
- **内容**：文件处理、异常处理、正则表达式、常用库
- **MOC**：[[Day21-30/MOC|Python语言应用 MOC]]

### 第三阶段：其他相关内容
- **时间**：Day31-35
- **内容**：Python 进阶、Web 前端、Linux 基础
- **MOC**：[[Day31-35/MOC|其他相关内容 MOC]]

### 第四阶段：数据库基础和进阶
- **时间**：Day36-45
- **内容**：MySQL、SQL 语法、索引、Python 操作数据库
- **MOC**：[[Day36-45/MOC|数据库基础和进阶 MOC]]

### 第五阶段：实战Django
- **时间**：Day46-60
- **内容**：Django 框架、Web 开发、RESTful API
- **MOC**：[[Day46-60/MOC|实战Django MOC]]

### 第六阶段：网络数据采集
- **时间**：Day61-65
- **内容**：爬虫基础、数据抓取、并发编程、Scrapy
- **MOC**：[[Day61-65/MOC|网络数据采集 MOC]]

### 第七阶段：Python数据分析
- **时间**：Day66-80
- **内容**：NumPy、pandas、数据可视化
- **MOC**：[[Day66-80/MOC|Python数据分析 MOC]]

### 第八阶段：机器学习
- **时间**：Day81-90
- **内容**：机器学习算法、神经网络、NLP
- **MOC**：[[Day81-90/MOC|机器学习 MOC]]

### 第九阶段：团队项目开发
- **时间**：Day91-100
- **内容**：项目实战、Docker、性能优化、部署
- **MOC**：[[Day91-100/MOC|团队项目开发 MOC]]

## 补充资源

- [[Python学习资源汇总]]
- [[番外篇/Python参考书籍]]
- [[更新日志]]

## 公开课

- [[公开课/年薪50W+的Python程序员如何写代码/年薪50W+的Python程序员如何写代码]]
- [[公开课/第04次公开课-好玩的Python/好玩的Python]]
- [[公开课/第05次公开课-算法入门系列1-周而复始/算法入门系列1-周而复始]]
- [[公开课/第06次公开课-算法入门系列2-在水一方/算法入门系列2 - 在水一方]]
"""

    with open(main_moc_path, "w", encoding="utf-8") as f:
        f.write(main_moc_content)
    print(f"Created: {main_moc_path}")

    # 2. 为每个阶段创建 MOC
    for stage_dir, stage_info in STAGES.items():
        moc_path = VAULT_ROOT / stage_dir / "MOC.md"

        # 收集该阶段的所有文件
        stage_files = []
        for day_num in stage_info["days"]:
            if day_num in FILE_MAP:
                for f in FILE_MAP[day_num]:
                    stage_files.append(f)

        # 构建 MOC 内容
        lines = [
            "---",
            f"title: {stage_info['name']} MOC",
            "tags:",
            f"  - MOC",
        ]
        for tag in stage_info["tags"]:
            lines.append(f"  - {tag}")
        lines.extend([
            "---",
            "",
            f"# {stage_info['name']}",
            "",
            f"> 本阶段包含 Day{min(stage_info['days'])}-Day{max(stage_info['days'])} 的内容",
            "",
            "## 文章列表",
            "",
        ])

        for f in sorted(stage_files, key=lambda x: x["path"].name):
            rel_path = f["path"].relative_to(VAULT_ROOT)
            title = extract_title(f["path"])
            lines.append(f"- [[{rel_path}|{title}]]")

        lines.append("")
        lines.append("## 返回")
        lines.append("")
        lines.append("- [[Python学习路线图]]")
        lines.append("")

        with open(moc_path, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(lines))
        print(f"Created: {moc_path}")


def fix_readme_links():
    """修复 README.md 中的错误链接"""
    readme_path = VAULT_ROOT / "README.md"

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 修复 Day23 的链接（缺少目录前缀）
    content = re.sub(
        r"\[Python读写CSV文件\]\(23\.Python读写CSV文件\.md\)",
        r"[Python读写CSV文件](./Day21-30/23.Python读写CSV文件.md)",
        content
    )

    # 修复 Day24 的链接（文件名不匹配）
    content = re.sub(
        r"\[Python读写Excel文件-1\]\(\./Day21-30/24\.用Python读写Excel文件-1\.md\)",
        r"[Python读写Excel文件-1](./Day21-30/24.Python读写Excel文件-1.md)",
        content
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed: {readme_path}")


def process_all_files():
    """处理所有文件"""
    build_file_map()

    total = 0
    for day_num, files in FILE_MAP.items():
        for file_info in files:
            file_path = file_info["path"]
            stage = file_info["stage"]
            tags = file_info["tags"]

            # 提取标题
            title = extract_title(file_path)

            # 获取相关文章
            related = get_related_files(day_num, stage)

            # 构建 frontmatter
            frontmatter = {
                "title": title,
                "tags": tags,
                "up": f"[[{stage}/MOC|{STAGES[stage]['name']} MOC]]",
            }

            # 添加 prev/next
            prev_files = [r for r in related if r.get("relation") == "prev"]
            next_files = [r for r in related if r.get("relation") == "next"]

            if prev_files:
                prev_path = str(prev_files[0]["path"].relative_to(VAULT_ROOT)).replace("\\", "/")
                frontmatter["prev"] = f"[[{prev_path}]]"

            if next_files:
                next_path = str(next_files[0]["path"].relative_to(VAULT_ROOT)).replace("\\", "/")
                frontmatter["next"] = f"[[{next_path}]]"

            # 添加 frontmatter
            content = add_frontmatter(file_path, frontmatter)

            # 添加相关文章区块
            content = add_related_section_to_content(content, related)

            # 写回文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            total += 1
            print(f"Processed: {file_path.name}")

    print(f"\nTotal files processed: {total}")


if __name__ == "__main__":
    print("=" * 60)
    print("开始为 Python-100-Days 建立 Obsidian 关系图谱")
    print("=" * 60)
    print()

    # 1. 处理所有文章
    print("步骤 1: 为所有文章添加 frontmatter 和相关链接...")
    process_all_files()
    print()

    # 2. 创建 MOC 文件
    print("步骤 2: 创建 MOC 索引文件...")
    create_moc_files()
    print()

    # 3. 修复 README 链接
    print("步骤 3: 修复 README 中的错误链接...")
    fix_readme_links()
    print()

    print("=" * 60)
    print("完成！请在 Obsidian 中打开图谱视图查看效果。")
    print("=" * 60)
