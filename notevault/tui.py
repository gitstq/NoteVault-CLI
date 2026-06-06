#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NoteVault TUI Dashboard
终端用户界面仪表板 - 提供美观的可视化界面
"""

import os
import sys
import shutil
from datetime import datetime
from .core import NoteVaultEngine


class TUIDashboard:
    """终端仪表板 - 使用纯 ANSI 控制码实现 TUI"""

    def __init__(self, engine: NoteVaultEngine):
        self.engine = engine
        self.term_width = shutil.get_terminal_size().columns
        self.term_height = shutil.get_terminal_size().lines

    def _clear(self):
        """清屏"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def _color(self, text: str, color: str) -> str:
        """添加颜色"""
        colors = {
            'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
            'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m',
            'white': '\033[97m', 'gray': '\033[90m', 'bold': '\033[1m',
            'dim': '\033[2m', 'reset': '\033[0m'
        }
        return f"{colors.get(color, '')}{text}\033[0m"

    def _center(self, text: str, width: int = None, fill: str = ' ') -> str:
        """居中"""
        width = width or self.term_width
        return text.center(width, fill)

    def _box_line(self, text: str, width: int = None) -> str:
        """绘制带边框的行"""
        width = width or min(70, self.term_width - 4)
        padding = width - len(text) - 2
        left = padding // 2
        right = padding - left
        return f"│{' ' * left}{text}{' ' * right}│"

    def render_dashboard(self):
        """渲染主仪表板"""
        self._clear()
        stats = self.engine.get_stats()
        notes = self.engine.list_notes(limit=5)

        w = min(76, self.term_width - 2)

        # 标题
        print(self._color('┌' + '─' * w + '┐', 'cyan'))
        title = "📓 NoteVault Dashboard"
        print(self._color(self._box_line(title, w), 'cyan'))
        print(self._color('├' + '─' * w + '┤', 'cyan'))

        # 统计卡片
        stat_line = f"  📓 {stats['total_notes']} 笔记  │  📝 {stats['total_words']} 字  │  🔗 {stats['total_links']} 链接  │  🏷️ {stats['total_tags']} 标签  "
        print(self._color(self._box_line(stat_line, w), 'cyan'))
        print(self._color('├' + '─' * w + '┤', 'cyan'))

        # 最近笔记
        print(self._color(self._box_line("🕐 最近更新", w), 'cyan'))
        if notes:
            for note in notes:
                title_short = note['title'][:30] + '...' if len(note['title']) > 30 else note['title']
                line = f"  • {title_short:<35} {note['updated_at'][:10]}  {note['word_count']}字"
                print(self._color(self._box_line(line, w), 'gray'))
        else:
            print(self._color(self._box_line("  (暂无笔记)", w), 'dim'))

        print(self._color('├' + '─' * w + '┤', 'cyan'))

        # 热门标签
        if stats['tags']:
            tag_str = ' '.join([f"#{t}" for t in stats['tags'][:8]])
            print(self._color(self._box_line(f"🏷️ {tag_str}", w), 'yellow'))
        else:
            print(self._color(self._box_line("🏷️ 暂无标签", w), 'dim'))

        print(self._color('└' + '─' * w + '┘', 'cyan'))

        # 快捷操作提示
        print()
        print(self._color("  快捷操作:", 'bold'))
        print(self._color("    notevault -n \"标题\"     快速创建笔记", 'green'))
        print(self._color("    notevault -s \"关键词\"   搜索笔记", 'green'))
        print(self._color("    notevault -l            列出所有笔记", 'green'))
        print(self._color("    notevault --stats       查看统计", 'green'))
        print()

    def render_note_graph(self):
        """渲染简单的笔记关系图 (ASCII)"""
        self._clear()
        stats = self.engine.get_stats()

        print(self._color("╔══════════════════════════════════════════════╗", 'cyan'))
        print(self._color("║         🕸️ 笔记关系图谱 (ASCII)              ║", 'cyan'))
        print(self._color("╚══════════════════════════════════════════════╝", 'cyan'))
        print()

        notes = self.engine.list_notes(limit=15)
        if not notes:
            print(self._color("  暂无笔记可展示", 'yellow'))
            return

        # 简单的星形布局
        center = self._color("★ 知识库核心", 'yellow')
        print(f"\n{' ' * 20}{center}")
        print(f"{' ' * 22}│")

        for i, note in enumerate(notes[:10]):
            prefix = "├─" if i < len(notes[:10]) - 1 else "└─"
            title = note['title'][:20]
            color = 'green' if note.get('link_count', 0) > 0 else 'white'
            print(f"{' ' * 20}{prefix} {self._color(title, color)}")

        print()
        print(self._color(f"  共 {len(notes)} 条笔记，{stats['total_links']} 个链接关系", 'gray'))


def launch_dashboard(engine: NoteVaultEngine):
    """启动仪表板"""
    dashboard = TUIDashboard(engine)
    dashboard.render_dashboard()
