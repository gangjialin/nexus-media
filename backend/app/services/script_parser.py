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

        def save_scene():
            """保存当前场景并开启新场景"""
            nonlocal current_scene
            if current_scene is not None:
                script.scenes.append(current_scene)
                current_scene = None

        def is_scene_title(line: str) -> bool:
            """判断是否为场景标题行"""
            # ## 第N场 ...
            if re.match(r"^#{1,3}\s*第?\s*\d+\s*场", line):
                return True
            # ## S01 ...
            if re.match(r"^#{1,3}\s*[Ss]?\d+[：:\s]", line):
                return True
            # --- 分隔线 也算场景分隔
            if re.match(r"^---+", line.strip()):
                return True
            return False

        for line in lines:
            # 跳过空行
            if not line.strip():
                continue

            # 作者声明
            author_match = re.match(r"^作者[:：]\s*(.+)", line)
            if author_match:
                script.author = author_match.group(1).strip()
                continue

            # 检测场景分隔线
            if re.match(r"^---+$", line.strip()):
                save_scene()
                continue

            # 检测新场景标题
            if is_scene_title(line):
                save_scene()
                current_scene = ParsedScene()
                # 尝试提取场景信息
                scene_info = re.match(
                    r"^#{1,3}\s*第?\s*(\d+)\s*场[：:]*\s*(内景|外景|室内|室外)?\s*(.+?)?\s*(日|夜|黄昏|晨|傍晚)?\s*$",
                    line
                )
                if not scene_info:
                    scene_info = re.match(r"^#{1,3}\s*[Ss]?(\d+)[：:\s]+(.+)", line)
                if scene_info:
                    if len(scene_info.groups()) >= 1 and scene_info.group(1):
                        current_scene.scene_number = scene_info.group(1)
                    if len(scene_info.groups()) >= 3 and scene_info.group(3):
                        current_scene.title = scene_info.group(3).strip()
                    if len(scene_info.groups()) >= 4 and scene_info.group(4):
                        current_scene.time_of_day = scene_info.group(4)
                continue

            # 累积到当前场景内容
            if current_scene is not None:
                current_scene.content += line + "\n"

                # 提取角色名: 【角色A】 或 角色A：
                char_match = re.findall(r"【(.+?)】", line)
                for char_name in char_match:
                    if char_name and char_name not in current_scene.characters:
                        current_scene.characters.append(char_name)

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
