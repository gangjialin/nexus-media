"""剧本文件导入解析器

支持格式：Markdown(.md), 纯文本(.txt), Word(.docx), PDF(.pdf)
"""

import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ParsedScene:
    """解析后的场景"""
    scene_number: str = ""          # 如 "S01", "1"
    title: str = ""                 # 场景标题
    location_type: str = ""         # 室内/室外
    location: str = ""              # 地点描述
    time_of_day: str = ""           # 日/夜/黄昏
    content: str = ""               # 场景正文内容
    characters: list[str] = field(default_factory=list)


@dataclass
class ParsedScript:
    """解析后的剧本"""
    title: str = ""
    author: str = ""
    scenes: list[ParsedScene] = field(default_factory=list)
    raw_text: str = ""
    word_count: int = 0


class ScriptParser:
    """剧本解析器基类"""

    def parse(self, file_path: str, filename: str) -> ParsedScript:
        """根据文件扩展名选择解析器"""
        ext = Path(filename).suffix.lower()
        content = self._read_file(file_path, ext)

        if ext in (".md", ".txt"):
            return self._parse_markdown(content, filename)
        elif ext == ".docx":
            return self._parse_docx(file_path, filename)
        elif ext == ".pdf":
            return self._parse_pdf(file_path, filename)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _read_file(self, file_path: str, ext: str) -> str:
        """读取文件内容"""
        if ext in (".md", ".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    # ==================== Markdown / 纯文本 ====================

    def _parse_markdown(self, content: str, filename: str) -> ParsedScript:
        """解析 Markdown/纯文本剧本

        支持的格式约定：
        - # 标题 = 剧本名称（第一个一级标题）
        - ## 标题 = 场景/场次
        - 作者: xxx = 作者声明

        示例：
            # 追光者
            作者: 张小明

            ## 第 1 场  内景  火车站候车大厅  日

            角色A拖着行李箱走进来...

            【角色A】
            人呢？不是说好了在这里等吗？
        """
        script = ParsedScript()
        script.title = Path(filename).stem
        script.raw_text = content
        script.word_count = len(content)

        lines = content.split("\n")

        # 匹配一级标题作为剧本名称
        title_match = re.match(r"^#\s+(.+)", lines[0]) if lines else None
        if title_match:
            script.title = title_match.group(1).strip()

        current_scene: ParsedScene | None = None

        for line in lines:
            line = line.rstrip()

            # 跳过空行
            if not line.strip():
                continue

            # 作者声明
            author_match = re.match(r"^作者[:：]\s*(.+)", line)
            if author_match:
                script.author = author_match.group(1).strip()
                continue

            # 场景标题：## 第N场 内景/外景 地点 时间
            scene_match = re.match(
                r"^#{1,3}\s*第?\s*(\d+)\s*场[：:]*\s*(内景|外景|室内|室外)?\s*(.+?)?\s*(日|夜|黄昏|晨|傍晚)?\s*$",
                line
            )
            if scene_match and current_scene is None:
                current_scene = ParsedScene()
                current_scene.scene_number = scene_match.group(1)
                current_scene.location_type = scene_match.group(2) or ""
                current_scene.location = scene_match.group(3) or ""
                current_scene.time_of_day = scene_match.group(4) or ""
                continue

            # 简化场景匹配：## S01 火车站
            alt_scene_match = re.match(r"^#{1,3}\s*(?:第?\d+场\s*)?[S|s]?(\d+)[：:\s]+(.+)", line)
            if alt_scene_match and current_scene is None:
                current_scene = ParsedScene()
                current_scene.scene_number = alt_scene_match.group(1)
                current_scene.title = alt_scene_match.group(2).strip()
                continue

            # 更宽松的场景匹配
            if line.strip().startswith("## ") and current_scene is None:
                current_scene = ParsedScene()
                remaining = line.strip()[3:].strip()
                # 尝试提取数字
                num_match = re.match(r"(\d+)", remaining)
                if num_match:
                    current_scene.scene_number = num_match.group(1)
                current_scene.title = remaining
                continue

            # 累积到当前场景内容
            if current_scene is not None:
                current_scene.content += line + "\n"

                # 提取角色名: 【角色A】 或 角色A：
                char_match = re.findall(r"【(.+?)】|(\S+)[：:]", line)
                for match in char_match:
                    char_name = match[0] or match[1]
                    if char_name and char_name not in current_scene.characters:
                        current_scene.characters.append(char_name)

            # 下一个场景开始 → 保存当前场景
            # (场景结束时由下一场景标题触发，在循环顶部处理)

        # 如果有未关闭的场景
        if current_scene is not None:
            script.scenes.append(current_scene)

        # 如果没有解析到场景，把全文当作一个场景
        if not script.scenes:
            script.scenes = [
                ParsedScene(
                    scene_number="1",
                    title="全文",
                    content=content,
                )
            ]

        return script

    # ==================== Word 文档 ====================

    def _parse_docx(self, file_path: str, filename: str) -> ParsedScript:
        """解析 .docx 文件"""
        try:
            from docx import Document
        except ImportError:
            raise ImportError("python-docx is required for .docx parsing")

        doc = Document(file_path)
        content = "\n".join(p.text for p in doc.paragraphs)
        script = self._parse_markdown(content, filename)

        # 尝试从文档属性获取标题
        if doc.core_properties.title:
            script.title = doc.core_properties.title
        if doc.core_properties.author:
            script.author = doc.core_properties.author

        return script

    # ==================== PDF ====================

    def _parse_pdf(self, file_path: str, filename: str) -> ParsedScript:
        """解析 PDF 文件"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("PyMuPDF is required for PDF parsing")

        doc = fitz.open(file_path)
        content_parts = []
        for page in doc:
            content_parts.append(page.get_text())
        doc.close()

        content = "\n".join(content_parts)
        return self._parse_markdown(content, filename)


# 全局单例
script_parser = ScriptParser()
