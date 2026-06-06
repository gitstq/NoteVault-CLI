#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NoteVault CLI Interface
命令行界面模块 - 提供交互式终端操作
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

from .core import NoteVaultEngine


class Colors:
    """终端颜色定义"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'


def print_banner():
    """打印欢迎横幅"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║  📓 NoteVault-CLI v1.0.0                                      ║
║  轻量级终端 Markdown 笔记与知识库管理引擎                      ║
║  Lightweight Terminal Markdown Note & Knowledge Base Engine   ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_note_preview(note: dict, index: int = None):
    """打印笔记预览"""
    prefix = f"{Colors.GREEN}[{index}]{Colors.RESET} " if index is not None else ""
    tags_str = ""
    if note.get('tags'):
        tags = [f"{Colors.YELLOW}#{t}{Colors.RESET}" for t in note['tags'].split(',') if t]
        tags_str = " ".join(tags)

    title = note.get('title', 'Untitled')
    note_id = note.get('id', '?')
    updated = note.get('updated_at', '')[:19]
    words = note.get('word_count', 0)
    links = note.get('link_count', 0)
    score = note.get('score', '')
    score_str = f" {Colors.CYAN}[匹配度: {score}]{Colors.RESET}" if score else ""

    print(f"{prefix}{Colors.BOLD}{Colors.WHITE}{title}{Colors.RESET}{score_str}")
    print(f"   {Colors.GRAY}ID:{note_id} | 📝 {words}字 | 🔗 {links}链接 | 🕐 {updated}{Colors.RESET}")
    if tags_str:
        print(f"   {tags_str}")
    print()


def interactive_menu(engine: NoteVaultEngine):
    """交互式主菜单"""
    print_banner()

    while True:
        print(f"\n{Colors.CYAN}┌──────────────── 主菜单 ────────────────┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GREEN}[1]{Colors.RESET} 📝 新建笔记        {Colors.GREEN}[2]{Colors.RESET} 📋 列出笔记")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GREEN}[3]{Colors.RESET} 🔍 搜索笔记        {Colors.GREEN}[4]{Colors.RESET} 🏷️  标签浏览")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GREEN}[5]{Colors.RESET} 📊 统计信息        {Colors.GREEN}[6]{Colors.RESET} 📥 导入笔记")
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GREEN}[7]{Colors.RESET} 📤 导出笔记        {Colors.GREEN}[0]{Colors.RESET} ❌ 退出")
        print(f"{Colors.CYAN}└────────────────────────────────────────┘{Colors.RESET}")

        choice = input(f"{Colors.YELLOW}➤ 请选择操作: {Colors.RESET}").strip()

        if choice == '1':
            create_note_interactive(engine)
        elif choice == '2':
            list_notes_interactive(engine)
        elif choice == '3':
            search_notes_interactive(engine)
        elif choice == '4':
            browse_tags_interactive(engine)
        elif choice == '5':
            show_stats(engine)
        elif choice == '6':
            import_notes_interactive(engine)
        elif choice == '7':
            export_note_interactive(engine)
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 感谢使用 NoteVault，再见！{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}⚠️ 无效选项，请重新选择{Colors.RESET}")


def create_note_interactive(engine: NoteVaultEngine):
    """交互式创建笔记"""
    print(f"\n{Colors.CYAN}📝 新建笔记{Colors.RESET}")
    title = input(f"{Colors.YELLOW}标题: {Colors.RESET}").strip()
    if not title:
        print(f"{Colors.RED}⚠️ 标题不能为空{Colors.RESET}")
        return

    print(f"{Colors.GRAY}请输入笔记内容 (Markdown 格式支持):")
    print(f"  - 使用 #标签 添加标签")
    print(f"  - 使用 [[笔记标题]] 创建双向链接")
    print(f"  - 输入空行后按 Enter 结束{Colors.RESET}")
    print(f"{Colors.YELLOW}内容:{Colors.RESET}")

    lines = []
    while True:
        line = input()
        if line == '' and lines and lines[-1] == '':
            lines.pop()
            break
        lines.append(line)

    content = '\n'.join(lines)
    if not content.strip():
        print(f"{Colors.RED}⚠️ 内容不能为空{Colors.RESET}")
        return

    note_id = engine.create_note(title, content)
    print(f"\n{Colors.GREEN}✅ 笔记创建成功！ID: {note_id}{Colors.RESET}")


def list_notes_interactive(engine: NoteVaultEngine):
    """交互式列出笔记"""
    print(f"\n{Colors.CYAN}📋 笔记列表{Colors.RESET}")
    notes = engine.list_notes(limit=20)
    if not notes:
        print(f"{Colors.YELLOW}📭 暂无笔记{Colors.RESET}")
        return

    for i, note in enumerate(notes, 1):
        print_note_preview(note, i)

    print(f"{Colors.GRAY}输入编号查看详情，或按 Enter 返回{Colors.RESET}")
    choice = input(f"{Colors.YELLOW}➤ {Colors.RESET}").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(notes):
            view_note_detail(engine, notes[idx]['id'])


def view_note_detail(engine: NoteVaultEngine, note_id: int):
    """查看笔记详情"""
    note = engine.get_note(note_id)
    if not note:
        print(f"{Colors.RED}⚠️ 笔记不存在{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{note['title']}{Colors.RESET}")
    print(f"{Colors.GRAY}ID: {note_id} | 创建于: {note['created_at'][:19]} | 更新于: {note['updated_at'][:19]}{Colors.RESET}")
    if note.get('tags'):
        tags = [f"{Colors.YELLOW}#{t}{Colors.RESET}" for t in note['tags'].split(',') if t]
        print(f"标签: {' '.join(tags)}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(note['content'])
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

    # 反向链接
    backlinks = engine.get_backlinks(note['title'])
    if backlinks:
        print(f"\n{Colors.MAGENTA}🔗 反向链接 ({len(backlinks)}):{Colors.RESET}")
        for bl in backlinks:
            print(f"   ← {Colors.CYAN}{bl['title']}{Colors.RESET}")

    print(f"\n{Colors.GRAY}[e] 编辑 | [d] 删除 | [Enter] 返回{Colors.RESET}")
    choice = input(f"{Colors.YELLOW}➤ {Colors.RESET}").strip().lower()

    if choice == 'e':
        edit_note_interactive(engine, note_id)
    elif choice == 'd':
        confirm = input(f"{Colors.RED}确认删除? (y/N): {Colors.RESET}").strip().lower()
        if confirm == 'y':
            engine.delete_note(note_id)
            print(f"{Colors.GREEN}✅ 已删除{Colors.RESET}")


def edit_note_interactive(engine: NoteVaultEngine, note_id: int):
    """交互式编辑笔记"""
    note = engine.get_note(note_id)
    if not note:
        return

    print(f"\n{Colors.CYAN}✏️ 编辑笔记{Colors.RESET}")
    print(f"{Colors.GRAY}当前标题: {note['title']}{Colors.RESET}")
    new_title = input(f"{Colors.YELLOW}新标题 (留空保持不变): {Colors.RESET}").strip()

    print(f"{Colors.GRAY}当前内容:{Colors.RESET}")
    print(note['content'][:200] + "..." if len(note['content']) > 200 else note['content'])
    print(f"\n{Colors.YELLOW}新内容 (留空保持不变, 输入空行结束):{Colors.RESET}")

    lines = []
    while True:
        line = input()
        if line == '' and lines and lines[-1] == '':
            lines.pop()
            break
        lines.append(line)

    new_content = '\n'.join(lines) if lines else None
    title = new_title if new_title else None

    if title or new_content:
        engine.update_note(note_id, title=title, content=new_content)
        print(f"{Colors.GREEN}✅ 笔记已更新{Colors.RESET}")


def search_notes_interactive(engine: NoteVaultEngine):
    """交互式搜索笔记"""
    print(f"\n{Colors.CYAN}🔍 搜索笔记{Colors.RESET}")
    query = input(f"{Colors.YELLOW}搜索关键词: {Colors.RESET}").strip()
    if not query:
        return

    results = engine.search_notes(query, limit=20)
    if not results:
        print(f"{Colors.YELLOW}📭 未找到匹配笔记{Colors.RESET}")
        return

    print(f"\n{Colors.GREEN}找到 {len(results)} 条结果:{Colors.RESET}\n")
    for i, note in enumerate(results, 1):
        print_note_preview(note, i)

    print(f"{Colors.GRAY}输入编号查看详情，或按 Enter 返回{Colors.RESET}")
    choice = input(f"{Colors.YELLOW}➤ {Colors.RESET}").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(results):
            view_note_detail(engine, results[idx]['id'])


def browse_tags_interactive(engine: NoteVaultEngine):
    """交互式标签浏览"""
    tags = engine.get_all_tags()
    if not tags:
        print(f"{Colors.YELLOW}📭 暂无标签{Colors.RESET}")
        return

    print(f"\n{Colors.CYAN}🏷️ 所有标签 ({len(tags)}):{Colors.RESET}")
    for i, tag in enumerate(tags, 1):
        print(f"  {Colors.GREEN}[{i}]{Colors.RESET} {Colors.YELLOW}#{tag}{Colors.RESET}")

    print(f"\n{Colors.GRAY}输入编号或标签名筛选，或按 Enter 返回{Colors.RESET}")
    choice = input(f"{Colors.YELLOW}➤ {Colors.RESET}").strip()

    tag_filter = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(tags):
            tag_filter = tags[idx]
    elif choice:
        tag_filter = choice.lstrip('#')

    if tag_filter:
        notes = engine.list_notes(tag=tag_filter, limit=50)
        print(f"\n{Colors.CYAN}标签 #{tag_filter} 的笔记 ({len(notes)}):{Colors.RESET}\n")
        for i, note in enumerate(notes, 1):
            print_note_preview(note, i)


def show_stats(engine: NoteVaultEngine):
    """显示统计信息"""
    stats = engine.get_stats()
    print(f"\n{Colors.CYAN}📊 笔记库统计{Colors.RESET}")
    print(f"{Colors.CYAN}┌────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  📓 笔记总数: {Colors.GREEN}{stats['total_notes']:>6}{Colors.RESET}        {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  📝 总字数:   {Colors.GREEN}{stats['total_words']:>6}{Colors.RESET}        {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  🔗 链接总数: {Colors.GREEN}{stats['total_links']:>6}{Colors.RESET}        {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  🏷️ 标签总数: {Colors.GREEN}{stats['total_tags']:>6}{Colors.RESET}        {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}└────────────────────────────────────┘{Colors.RESET}")

    if stats['tags']:
        print(f"\n{Colors.YELLOW}热门标签:{Colors.RESET}")
        for tag in stats['tags'][:15]:
            print(f"  #{tag}", end="  ")
        print()


def import_notes_interactive(engine: NoteVaultEngine):
    """交互式导入笔记"""
    print(f"\n{Colors.CYAN}📥 导入笔记{Colors.RESET}")
    path = input(f"{Colors.YELLOW}目录路径: {Colors.RESET}").strip()
    pattern = input(f"{Colors.YELLOW}文件模式 (默认 *.md): {Colors.RESET}").strip() or "*.md"

    if not os.path.isdir(path):
        print(f"{Colors.RED}⚠️ 目录不存在{Colors.RESET}")
        return

    count = engine.import_from_directory(path, pattern)
    print(f"{Colors.GREEN}✅ 成功导入 {count} 条笔记{Colors.RESET}")


def export_note_interactive(engine: NoteVaultEngine):
    """交互式导出笔记"""
    print(f"\n{Colors.CYAN}📤 导出笔记{Colors.RESET}")
    note_id = input(f"{Colors.YELLOW}笔记 ID: {Colors.RESET}").strip()
    if not note_id.isdigit():
        print(f"{Colors.RED}⚠️ 无效 ID{Colors.RESET}")
        return

    print(f"{Colors.GRAY}格式: html, json, txt, md{Colors.RESET}")
    fmt = input(f"{Colors.YELLOW}导出格式 (默认 html): {Colors.RESET}").strip() or "html"

    output = engine.export_note(int(note_id), fmt)
    if not output:
        print(f"{Colors.RED}⚠️ 笔记不存在{Colors.RESET}")
        return

    note = engine.get_note(int(note_id))
    filename = f"{note['title']}.{fmt}"
    safe_name = "".join(c if c.isalnum() or c in '-_.' else '_' for c in filename)

    output_path = Path.home() / safe_name
    output_path.write_text(output, encoding='utf-8')
    print(f"{Colors.GREEN}✅ 已导出到: {output_path}{Colors.RESET}")


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(
        description='NoteVault-CLI - 轻量级终端 Markdown 笔记与知识库管理引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  notevault                    启动交互式菜单
  notevault --new "标题"       快速创建笔记
  notevault --list             列出所有笔记
  notevault --search "关键词"   搜索笔记
  notevault --stats            显示统计信息
        """
    )
    parser.add_argument('--vault', '-v', help='笔记库路径')
    parser.add_argument('--new', '-n', metavar='TITLE', help='快速创建笔记')
    parser.add_argument('--content', '-c', help='笔记内容 (配合 --new 使用)')
    parser.add_argument('--list', '-l', action='store_true', help='列出笔记')
    parser.add_argument('--search', '-s', metavar='QUERY', help='搜索笔记')
    parser.add_argument('--tag', '-t', metavar='TAG', help='按标签筛选')
    parser.add_argument('--stats', action='store_true', help='统计信息')
    parser.add_argument('--view', metavar='ID', type=int, help='查看笔记详情')
    parser.add_argument('--delete', '-d', metavar='ID', type=int, help='删除笔记')
    parser.add_argument('--export', '-e', metavar='ID', type=int, help='导出笔记')
    parser.add_argument('--format', '-f', default='html', choices=['html', 'json', 'txt', 'md'],
                        help='导出格式 (默认: html)')
    parser.add_argument('--import-dir', metavar='PATH', help='从目录导入 Markdown')
    parser.add_argument('--pattern', default='*.md', help='导入文件模式')
    parser.add_argument('--interactive', '-i', action='store_true', help='强制交互模式')
    parser.add_argument('--version', action='store_true', help='显示版本')

    args = parser.parse_args()

    if args.version:
        print("NoteVault-CLI v1.0.0")
        sys.exit(0)

    engine = NoteVaultEngine(args.vault)

    # 无参数或强制交互模式
    if args.interactive or (not any([
        args.new, args.list, args.search, args.stats, args.view,
        args.delete, args.export, args.import_dir
    ])):
        interactive_menu(engine)
        return

    # 快速创建
    if args.new:
        content = args.content or ""
        if not content:
            print("请输入笔记内容 (Ctrl+D 结束):")
            content = sys.stdin.read()
        note_id = engine.create_note(args.new, content)
        print(f"✅ 笔记创建成功！ID: {note_id}")
        return

    # 列出笔记
    if args.list:
        notes = engine.list_notes(tag=args.tag, limit=50)
        if not notes:
            print("📭 暂无笔记")
            return
        for note in notes:
            print(f"[{note['id']}] {note['title']} ({note['word_count']}字)")
        return

    # 搜索
    if args.search:
        results = engine.search_notes(args.search, limit=20)
        if not results:
            print("📭 未找到匹配笔记")
            return
        for note in results:
            score = f" [匹配度: {note['score']}]" if 'score' in note else ""
            print(f"[{note['id']}] {note['title']}{score}")
        return

    # 统计
    if args.stats:
        stats = engine.get_stats()
        print(f"📓 笔记: {stats['total_notes']} | 📝 字数: {stats['total_words']} | 🔗 链接: {stats['total_links']} | 🏷️ 标签: {stats['total_tags']}")
        return

    # 查看详情
    if args.view:
        note = engine.get_note(args.view)
        if note:
            print(f"\n{'='*50}")
            print(f"标题: {note['title']}")
            print(f"{'='*50}")
            print(note['content'])
            print(f"{'='*50}")
        else:
            print("⚠️ 笔记不存在")
        return

    # 删除
    if args.delete:
        if engine.delete_note(args.delete):
            print("✅ 已删除")
        else:
            print("⚠️ 笔记不存在")
        return

    # 导出
    if args.export:
        output = engine.export_note(args.export, args.format)
        if output:
            print(output)
        else:
            print("⚠️ 笔记不存在")
        return

    # 导入
    if args.import_dir:
        count = engine.import_from_directory(args.import_dir, args.pattern)
        print(f"✅ 成功导入 {count} 条笔记")
        return


if __name__ == '__main__':
    main()
