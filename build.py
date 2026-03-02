#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
import argparse
import glob
import logging
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BuildManager:
    """
    统一构建管理：依赖拉取 → 符号链接 → 打包 / 测试。

    用法:
        python build.py                  完整构建（拉取依赖 + 打 whl 包）
        python build.py local            本地构建（跳过依赖拉取, 打 whl 包）
        python build.py test             单元测试（拉取依赖 + 执行测试）
        python build.py test local       单元测试（跳过依赖拉取, 执行测试）
        python build.py -r <revision>    指定依赖的内部源码仓(例如msopcom)的 Git 分支/标签/commit

    参数说明:
        - 参数: command : 构建动作: 为空时为全构建, local 为跳过依赖下载, test 为运行单元测试。
        - 参数: -r, --revision : 指定 Git 修订版本或标签用于依赖检出。
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        argument_parser = argparse.ArgumentParser(description='Build the project and optionally run tests.')
        argument_parser.add_argument('command', nargs='*', default=[],
                                     choices=[[], 'local', 'test'],
                                     help='Build action: omit for full build, "local" to skip dependency download, "test" to run unit tests')
        argument_parser.add_argument('-r', '--revision',
                                     help='Specify Git revision for internal dependent repo (e.g., msopcom).')
        self.parsed_arguments = argument_parser.parse_args()

    def _execute_command(self, command_sequence, timeout_seconds=36000, cwd=None, env=None):
        logging.info("Running: %s", " ".join(command_sequence))
        subprocess.run(command_sequence, timeout=timeout_seconds, check=True, cwd=cwd, env=env)

    def _update_symlink(self, dst_path, src_path):
        src_path = Path(src_path)
        dst_path = Path(dst_path)

        if dst_path.is_symlink():
            dst_path.unlink()
        elif dst_path.exists():
            shutil.rmtree(dst_path)

        dst_path.absolute().parent.mkdir(parents=True, exist_ok=True)
        dst_path.symlink_to(src_path.absolute(), target_is_directory=True)

    def _link_asc_tools_template(self):
        asc_tools_dir = self.project_root / "thirdparty" / "asc-tools" / "utils" / "templates" / \
                        "new_op_project_template"
        install_dir = self.project_root / "msopgen" / "new_op_project_template"
        self._update_symlink(install_dir, asc_tools_dir)

    def run(self):
        os.chdir(self.project_root)

        # 在非 local 场景下按需更新依赖；在 local 场景下仅使用本地已有代码，不更新依赖。
        if 'local' not in self.parsed_arguments.command:
            from download_dependencies import DependencyManager
            DependencyManager(self.parsed_arguments).run()

        self._link_asc_tools_template()

        if 'test' in self.parsed_arguments.command:
            # -------------------- 单元测试 --------------------
            test_dir = self.project_root / "test"
            self._execute_command([sys.executable, "run_test.py"], cwd=str(test_dir))
        else:
            # -------------------- 产品构建（打 whl 包） --------------------
            output_dir = str(self.project_root / "output")

            self._execute_command([sys.executable, "setup.py",
                                   "egg_info", "--egg-base", "build",
                                   "bdist_wheel", "--dist-dir", output_dir])

            self._execute_command([sys.executable, "setup.py",
                                   "egg_info", "--egg-base", "../build",
                                   "bdist_wheel", "--dist-dir", output_dir],
                                  cwd=str(self.project_root / "tools"))

            for whl_file in glob.glob(str(self.project_root / "output" / "*.whl")):
                os.chmod(whl_file, 0o550)


if __name__ == "__main__":
    try:
        BuildManager().run()
    except Exception:
        logging.error(f"Unexpected error: {traceback.format_exc()}")
        sys.exit(1)
