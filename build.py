#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import logging
import argparse
import sys
import glob
from pathlib import Path
from download_dependencies import update_submodule


def exec_cmd(cmd):
    result = subprocess.run(cmd, capture_output=False, text=True, timeout=3600)
    if result.returncode != 0:
        logging.error("execute command %s failed, please check the log", " ".join(cmd))
        sys.exit(result.returncode)


def run_tests():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(script_dir, 'test')
    os.chdir(test_dir)
    subprocess.run([sys.executable, 'run_test.py'], check=True)

def create_arg_parser():
    parser = argparse.ArgumentParser(description='Build script with optional testing')
    parser.add_argument('command', nargs='?', default='build', 
                    choices=['build', 'test'],
                    help='Command to execute (build or test)')
    parser.add_argument('-r', '--revision',
                        help="Build with specific revision or tag")
    return parser

def update_symlink(dst_path, src_path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)

    if dst_path.is_symlink():
        dst_path.unlink()
    elif dst_path.exists():
        shutil.rmtree(dst_path)

    dst_path.absolute().parent.mkdir(parents=True, exist_ok=True)
    dst_path.symlink_to(src_path.absolute(), target_is_directory=True)

def add_link_to_asc_tools_template():
    asc_tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "thirdparty", "asc-tools",
                                                 "utils", "templates", "new_op_project_template"))
    asc_tools_install_dir = os.path.join(os.path.dirname(__file__), "msopgen", "new_op_project_template")
    update_symlink(asc_tools_install_dir, asc_tools_dir)


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    current_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    os.chdir(current_dir)
    # 解析入参是否为local，非local场景时按需更新代码；local场景不更新代码只使用本地代码
    if 'local' not in args.command:
        # update submodule
        update_submodule(args)
    # 获取编译文件
    add_link_to_asc_tools_template()
    if args.command == 'test':
        run_tests()
    else:
        # msopgen打whl包
        exec_cmd([sys.executable, 'setup.py', 'egg_info', '--egg-base', 'build', 'bdist_wheel', '--dist-dir',  os.path.join(current_dir, 'output')])
        # msopst打whl包
        os.chdir("tools")
        exec_cmd([sys.executable, "setup.py", 'egg_info', '--egg-base', '../build', 'bdist_wheel', '--dist-dir',  os.path.join(current_dir, 'output')])
        whl_package = glob.glob(os.path.join(current_dir, "dist", "*.whl"))
        for file in whl_package:
            os.chmod(file, 0o550)
