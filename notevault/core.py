#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NoteVault Core Engine
核心引擎模块 - 笔记存储、搜索、标签管理
"""

import os
import re
import json
import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Optional


class NoteVaultEngine:
    """NoteVault 核心引擎 - 管理笔记的CRUD、搜索和关联"""

    def __init__(self, vault_path: str = None):
        """初始化笔记库

        Args:
            vault_path: 笔记库路径，默认 ~/.notevault
        """
        self.vault_path = Path(vault_path or os.path.expanduser("~/.notevault"))
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.db_path = str(self.vault_path / "notevault.db")
        self.notes_dir = self.vault_path / "notes"
        self.notes_dir.mkdir(exist_ok=True)
        self._conn = None
        self._init_db()

    def _get_conn(self):
        """获取数据库连接 (单连接模式避免锁冲突)"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, timeout=30.0)
            self._conn.execute("PRAGMA foreign_keys = ON")
        return self._conn

    def _init_db(self):
        """初始化 SQLite 数据库"""
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                word_count INTEGER DEFAULT 0,
                link_count INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS note_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_note_id INTEGER NOT NULL,
                to_note_title TEXT NOT NULL,
                FOREIGN KEY (from_note_id) REFERENCES notes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS search_index (
                note_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                frequency REAL DEFAULT 1.0,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_notes_title ON notes(title);
            CREATE INDEX IF NOT EXISTS idx_notes_tags ON notes(tags);
            CREATE INDEX IF NOT EXISTS idx_search_word ON search_index(word);
            CREATE INDEX IF NOT EXISTS idx_links_from ON note_links(from_note_id);
        """)
        conn.commit()

    def _extract_tags(self, content: str) -> str:
        """从内容中提取标签 (#tag)"""
        tags = re.findall(r'#(\w+)', content)
        return ','.join(sorted(set(tags)))

    def _extract_links(self, content: str) -> List[str]:
        """从内容中提取双向链接 ([[Note Title]])"""
        return re.findall(r'\[\[(.*?)\]\]', content)

    def _compute_word_count(self, content: str) -> int:
        """计算字数"""
        text = re.sub(r'[#*`\[\]\(\)|\-!>]', '', content)
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        en_words = len(re.findall(r'[a-zA-Z]+', text))
        return cn_chars + en_words

    def _build_search_index(self, note_id: int, title: str, content: str):
        """构建搜索索引 (TF-IDF)"""
        text = f"{title} {content}".lower()
        cn_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        en_words = re.findall(r'[a-z]{2,}', text)
        all_words = cn_words + en_words

        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        conn = self._get_conn()
        conn.execute("DELETE FROM search_index WHERE note_id = ?", (note_id,))
        for word, freq in word_freq.items():
            conn.execute(
                "INSERT INTO search_index (note_id, word, frequency) VALUES (?, ?, ?)",
                (note_id, word, freq)
            )
        conn.commit()

    def create_note(self, title: str, content: str) -> int:
        """创建新笔记"""
        now = datetime.datetime.now().isoformat()
        tags = self._extract_tags(content)
        word_count = self._compute_word_count(content)
        links = self._extract_links(content)

        conn = self._get_conn()
        cursor = conn.execute(
            """INSERT INTO notes (title, content, tags, created_at, updated_at, word_count, link_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, content, tags, now, now, word_count, len(links))
        )
        note_id = cursor.lastrowid

        # 保存到文件
        note_file = self.notes_dir / f"{note_id:06d}_{self._safe_filename(title)}.md"
        note_file.write_text(content, encoding='utf-8')

        # 保存链接关系
        for link in links:
            conn.execute(
                "INSERT INTO note_links (from_note_id, to_note_title) VALUES (?, ?)",
                (note_id, link.strip())
            )

        # 构建搜索索引
        self._build_search_index(note_id, title, content)
        conn.commit()

        return note_id

    def update_note(self, note_id: int, title: str = None, content: str = None) -> bool:
        """更新笔记"""
        conn = self._get_conn()
        row = conn.execute(
            "SELECT title, content FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
        if not row:
            return False

        old_title, old_content = row
        new_title = title if title is not None else old_title
        new_content = content if content is not None else old_content

        now = datetime.datetime.now().isoformat()
        tags = self._extract_tags(new_content)
        word_count = self._compute_word_count(new_content)
        links = self._extract_links(new_content)

        conn.execute(
            """UPDATE notes SET title=?, content=?, tags=?, updated_at=?,
               word_count=?, link_count=? WHERE id=?""",
            (new_title, new_content, tags, now, word_count, len(links), note_id)
        )

        # 更新文件
        for f in self.notes_dir.glob(f"{note_id:06d}_*.md"):
            f.unlink()
        note_file = self.notes_dir / f"{note_id:06d}_{self._safe_filename(new_title)}.md"
        note_file.write_text(new_content, encoding='utf-8')

        # 更新链接
        conn.execute("DELETE FROM note_links WHERE from_note_id = ?", (note_id,))
        for link in links:
            conn.execute(
                "INSERT INTO note_links (from_note_id, to_note_title) VALUES (?, ?)",
                (note_id, link.strip())
            )

        # 重建搜索索引
        self._build_search_index(note_id, new_title, new_content)
        conn.commit()

        return True

    def delete_note(self, note_id: int) -> bool:
        """删除笔记"""
        conn = self._get_conn()
        row = conn.execute("SELECT title FROM notes WHERE id = ?", (note_id,)).fetchone()
        if not row:
            return False

        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))

        # 删除文件
        for f in self.notes_dir.glob(f"{note_id:06d}_*.md"):
            f.unlink()

        conn.commit()
        return True

    def get_note(self, note_id: int) -> Optional[Dict]:
        """获取单个笔记详情"""
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
        conn.row_factory = None
        if not row:
            return None
        return dict(row)

    def list_notes(self, tag: str = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        """列出笔记"""
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        if tag:
            rows = conn.execute(
                """SELECT id, title, tags, created_at, updated_at, word_count, link_count
                   FROM notes WHERE tags LIKE ? ORDER BY updated_at DESC LIMIT ? OFFSET ?""",
                (f"%{tag}%", limit, offset)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT id, title, tags, created_at, updated_at, word_count, link_count
                   FROM notes ORDER BY updated_at DESC LIMIT ? OFFSET ?""",
                (limit, offset)
            ).fetchall()
        conn.row_factory = None
        return [dict(r) for r in rows]

    def search_notes(self, query: str, limit: int = 20) -> List[Dict]:
        """搜索笔记 (TF-IDF + 标题匹配)"""
        query = query.lower()
        keywords = re.findall(r'[\u4e00-\u9fff]{2,}|[a-z]{2,}', query)

        if not keywords:
            return []

        conn = self._get_conn()
        conn.row_factory = sqlite3.Row

        scores = {}
        for kw in keywords:
            rows = conn.execute(
                "SELECT note_id, frequency FROM search_index WHERE word = ?",
                (kw,)
            ).fetchall()
            for row in rows:
                nid = row[0]
                freq = row[1]
                scores[nid] = scores.get(nid, 0) + freq

            # 标题匹配加分
            title_rows = conn.execute(
                "SELECT id FROM notes WHERE lower(title) LIKE ?",
                (f"%{kw}%",)
            ).fetchall()
            for row in title_rows:
                scores[row[0]] = scores.get(row[0], 0) + 5.0

        if not scores:
            conn.row_factory = None
            return []

        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        ids = [x[0] for x in sorted_ids]

        placeholders = ','.join('?' * len(ids))
        rows = conn.execute(
            f"""SELECT id, title, tags, created_at, updated_at, word_count, link_count
                FROM notes WHERE id IN ({placeholders})""",
            ids
        ).fetchall()

        note_map = {r['id']: dict(r) for r in rows}
        result = []
        for nid, score in sorted_ids:
            if nid in note_map:
                note_map[nid]['score'] = round(score, 2)
                result.append(note_map[nid])

        conn.row_factory = None
        return result

    def get_backlinks(self, title: str) -> List[Dict]:
        """获取指向某标题的反向链接"""
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT n.id, n.title, n.updated_at
               FROM notes n JOIN note_links l ON n.id = l.from_note_id
               WHERE l.to_note_title = ?""",
            (title,)
        ).fetchall()
        conn.row_factory = None
        return [dict(r) for r in rows]

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        conn = self._get_conn()
        rows = conn.execute("SELECT tags FROM notes WHERE tags != ''").fetchall()
        all_tags = set()
        for row in rows:
            all_tags.update(row[0].split(','))
        return sorted(t for t in all_tags if t)

    def get_stats(self) -> Dict:
        """获取笔记库统计信息"""
        conn = self._get_conn()
        total = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        total_words = conn.execute("SELECT COALESCE(SUM(word_count), 0) FROM notes").fetchone()[0]
        total_links = conn.execute("SELECT COUNT(*) FROM note_links").fetchone()[0]
        tags = self.get_all_tags()
        return {
            "total_notes": total,
            "total_words": total_words,
            "total_links": total_links,
            "total_tags": len(tags),
            "tags": tags
        }

    def export_note(self, note_id: int, fmt: str = "html") -> str:
        """导出笔记为指定格式"""
        note = self.get_note(note_id)
        if not note:
            return ""

        content = note['content']
        title = note['title']

        if fmt == "html":
            return self._markdown_to_html(content, title)
        elif fmt == "json":
            return json.dumps(note, ensure_ascii=False, indent=2)
        elif fmt == "txt":
            return f"{title}\n{'=' * len(title)}\n\n{content}"
        else:
            return content

    def _markdown_to_html(self, md: str, title: str) -> str:
        """简单的 Markdown 转 HTML"""
        html = md
        html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.M)
        html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.M)
        html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.M)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.S)
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        html = re.sub(r'\[\[(.*?)\]\]', r'<a href="#note-\1">[[\1]]</a>', html)
        html = re.sub(r'^- (.*)$', r'<li>\1</li>', html, flags=re.M)

        paragraphs = html.split('\n\n')
        new_paras = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<'):
                p = f'<p>{p}</p>'
            new_paras.append(p)
        html = '\n\n'.join(new_paras)

        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{title}</title>
<style>
body {{ max-width: 800px; margin: 40px auto; padding: 20px; font-family: system-ui; line-height: 1.6; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
pre {{ background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
a {{ color: #0366d6; }}
</style>
</head>
<body>
<h1>{title}</h1>
{html}
</body>
</html>"""

    def _safe_filename(self, title: str) -> str:
        """生成安全的文件名"""
        safe = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', title)
        return safe[:50]

    def import_from_directory(self, dir_path: str, pattern: str = "*.md") -> int:
        """从目录导入 Markdown 文件"""
        count = 0
        path = Path(dir_path)
        for md_file in path.glob(pattern):
            content = md_file.read_text(encoding='utf-8')
            title = md_file.stem
            self.create_note(title, content)
            count += 1
        return count

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None
