#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NoteVault Core Engine Tests
核心引擎单元测试
"""

import os
import sys
import tempfile
import shutil

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notevault.core import NoteVaultEngine


def test_create_note():
    """测试创建笔记"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        note_id = engine.create_note("测试笔记", "这是测试内容 #tag1 #tag2")
        assert note_id > 0

        note = engine.get_note(note_id)
        assert note is not None
        assert note['title'] == "测试笔记"
        assert "tag1" in note['tags']
        assert "tag2" in note['tags']
        print("✅ test_create_note passed")


def test_update_note():
    """测试更新笔记"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        note_id = engine.create_note("旧标题", "旧内容")
        engine.update_note(note_id, title="新标题", content="新内容 #updated")

        note = engine.get_note(note_id)
        assert note['title'] == "新标题"
        assert "updated" in note['tags']
        print("✅ test_update_note passed")


def test_delete_note():
    """测试删除笔记"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        note_id = engine.create_note("待删除", "内容")
        assert engine.delete_note(note_id)
        assert engine.get_note(note_id) is None
        print("✅ test_delete_note passed")


def test_search_notes():
    """测试搜索功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        engine.create_note("Python教程", "Python 是一门优秀的编程语言")
        engine.create_note("JavaScript指南", "JS 用于前端开发")
        engine.create_note("Python进阶", "Python 高级特性详解")

        results = engine.search_notes("Python")
        assert len(results) >= 2
        # 标题匹配的应该排在前面
        assert any("Python" in r['title'] for r in results)
        print("✅ test_search_notes passed")


def test_bidirectional_links():
    """测试双向链接"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        engine.create_note("笔记A", "这是笔记A，链接到 [[笔记B]]")
        engine.create_note("笔记B", "这是笔记B的内容")

        backlinks = engine.get_backlinks("笔记B")
        assert len(backlinks) == 1
        assert backlinks[0]['title'] == "笔记A"
        print("✅ test_bidirectional_links passed")


def test_tags():
    """测试标签功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        engine.create_note("笔记1", "内容 #python #coding")
        engine.create_note("笔记2", "内容 #python #ai")

        tags = engine.get_all_tags()
        assert "python" in tags
        assert "coding" in tags
        assert "ai" in tags

        notes = engine.list_notes(tag="python")
        assert len(notes) == 2
        print("✅ test_tags passed")


def test_stats():
    """测试统计功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        engine.create_note("笔记1", "Hello World")
        engine.create_note("笔记2", "Python 编程指南")

        stats = engine.get_stats()
        assert stats['total_notes'] == 2
        assert stats['total_words'] > 0
        print("✅ test_stats passed")


def test_export():
    """测试导出功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)
        note_id = engine.create_note("导出测试", "# 标题\n\n正文内容")

        html = engine.export_note(note_id, "html")
        assert "<html>" in html
        assert "标题" in html

        json_str = engine.export_note(note_id, "json")
        assert "导出测试" in json_str
        print("✅ test_export passed")


def test_import():
    """测试导入功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = NoteVaultEngine(tmpdir)

        # 创建测试文件
        import_dir = os.path.join(tmpdir, "import_test")
        os.makedirs(import_dir)
        with open(os.path.join(import_dir, "test1.md"), "w") as f:
            f.write("# Test1\nContent")
        with open(os.path.join(import_dir, "test2.md"), "w") as f:
            f.write("# Test2\nContent")

        count = engine.import_from_directory(import_dir)
        assert count == 2

        stats = engine.get_stats()
        assert stats['total_notes'] == 2
        print("✅ test_import passed")


def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行 NoteVault 单元测试...\n")
    tests = [
        test_create_note,
        test_update_note,
        test_delete_note,
        test_search_notes,
        test_bidirectional_links,
        test_tags,
        test_stats,
        test_export,
        test_import,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"测试结果: {Colors.GREEN if failed == 0 else Colors.RED}{passed} 通过, {failed} 失败{Colors.RESET}")
    return failed == 0


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
