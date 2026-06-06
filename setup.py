#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NoteVault-CLI Setup
安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="notevault-cli",
    version="1.0.0",
    author="NoteVault Team",
    author_email="notevault@example.com",
    description="轻量级终端 Markdown 笔记与知识库管理引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/NoteVault-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "notevault=notevault.cli:main",
            "nv=notevault.cli:main",
        ],
    },
    keywords="markdown notes knowledge-base cli terminal note-taking zettelkasten",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/NoteVault-CLI/issues",
        "Source": "https://github.com/gitstq/NoteVault-CLI",
    },
)
