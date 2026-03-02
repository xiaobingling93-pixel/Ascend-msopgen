#!/usr/bin/env python
# coding=utf-8
# -------------------------------------------------------------------------
# This file is part of the MindStudio project.
# Copyright (c) 2025 Huawei Technologies Co.,Ltd.
#
# MindStudio is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# -------------------------------------------------------------------------
"""
Function:
This file mainly set up for op_gen whl package.
"""

import os
import stat
import shutil
from setuptools import setup
from pathlib import Path

os.environ['SOURCE_DATE_EPOCH'] = str(int(os.path.getctime(os.path.realpath(__file__))))
currentDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
os.chdir(currentDir)
os.makedirs('build', exist_ok=True)
# 把 msopgen.py “重命名”为 msopgen （复制 + 去后缀 + 加可执行权限）
src = 'msopgen/msopgen.py'
dst = 'build/msopgen'
shutil.copy(src, dst)
st = os.stat(dst)
os.chmod(dst, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def update_symlink(dst_path, src_path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)

    if dst_path.is_symlink():
        dst_path.unlink()
    elif dst_path.exists():
        shutil.rmtree(dst_path)

    dst_path.absolute().parent.mkdir(parents=True, exist_ok=True)
    dst_path.symlink_to(src_path.absolute(), target_is_directory=True)


def link_asc_tools_template():
    project_root = Path(__file__).resolve().parent
    asc_tools_dir = project_root / "thirdparty" / "asc-tools" / "utils" / "templates" / \
                    "new_op_project_template"
    install_dir = project_root / "msopgen" / "new_op_project_template"
    update_symlink(install_dir, asc_tools_dir)

link_asc_tools_template()

setup_kwargs = {
    "include_package_data": True
}


def read_txt(file_name):
    """
    read from file
    """
    with open(file_name) as file_object:
        return file_object.read()

setup(
    name="msopgen",
    version="1.0.0",
    scripts=[dst],
    zip_safe=False,
    package_dir={'': '.'},
    packages=['msopgen', 'msopgen/interface', 'msopgen/simulator'],
    package_data={
        "msopgen": [
            "json_template/*",
            "config/*",
            "new_op_project_template/**/*"
        ],
    },
    install_requires=[],
    license=read_txt("LICENSE"),
    include_package_data=True,
    python_requires = '>=3.7'
)
