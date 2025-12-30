#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

def find_msopst_root(start_path):
    """
    从当前路径向上递归查找 tools/msopst 目录位置
    :param start_path: 起始搜索路径
    :return: tools/msopst 的绝对路径（作为root）
    :raises: FileNotFoundError 如果找不到目录
    """
    current = Path(start_path).absolute()
    
    # 定义所有可能的msopst目录位置（包括嵌套情况）
    possible_names = [
        "msopst",                # 直接位于工具目录下
        "msopst/msopst",         # 处理嵌套结构
        "tools/msopst",          # 标准工具目录
        "tools/msopst/msopst"    # 标准工具目录下的嵌套
    ]
    
    while current != current.parent:  # 直到根目录
        for name in possible_names:
            target = current / name
            if target.exists():
                # 统一返回 tools/msopst 结构
                if "tools/msopst" in str(target):
                    return target if name.count("msopst") == 1 else target.parent
                else:
                    # 如果找到的是非tools路径，尝试推测tools位置
                    tools_candidate = current / "tools" / "msopst"
                    if tools_candidate.exists():
                        return tools_candidate
        current = current.parent
    
    raise FileNotFoundError(
        "未找到 tools/msopst 目录，请检查项目结构\n"
        f"当前搜索路径: {start_path}\n"
        "期望位置: .../tools/msopst 或 .../msopst"
    )

def run_single_test(script_dir, testcase_root, msopst_source_code, test_type, run_env):
    """
    运行指定类型的测试（UT或ST）
    :param script_dir: 测试脚本所在目录（msOpGen根目录）
    :param msopst_source_code: msopst源码目录
    :param test_type: 测试类型 ('ut' 或 'st')
    :return: pytest 返回码
    """
    # 1. 设置输出目录路径（script_dir.parent/output/msopst）
    output_dir = script_dir.parent / "output" / os.path.basename(testcase_root)
    
    # 2. 确保目录存在（创建 output 和 output/msopst）
    output_dir.mkdir(parents=True, exist_ok=True)  

    # 3. 构建测试目录路径（如 test_msopst/ut 或 test_msopst/st）
    # test_path = script_dir / "test_msopst" / test_type

    # 4. 检查关键目录是否存在
    required_dirs = {
        "测试目录": testcase_root,
        "源码目录": msopst_source_code
    }
    for name, path in required_dirs.items():
        if not path.exists():
            raise FileNotFoundError(f"{name}不存在: {path}")
        print(f"{name}: {path}")

    # 5. 构建 pytest 命令
    gen_cmd = [
        sys.executable, '-m', 'pytest',
        str(testcase_root / test_type),
        f'--cov={msopst_source_code}',
        # HTML 报告输出到 output/msopst/coverage_{test_type}
        f'--cov-report=html:{output_dir / f"coverage_{test_type}"}',
        # 同时生成 XML 报告（可选）
        f'--cov-report=xml:{output_dir / "coverage.xml"}',
    ]

    # 6. ST测试需要详细输出
    if test_type == 'st':
        gen_cmd.append('-v')
    
    print(f"\n执行命令: {' '.join(gen_cmd)}")

    # 8. 执行命令并返回状态码
    return subprocess.run(gen_cmd, env=run_env, text=True).returncode
# ==================== 主逻辑 ====================
if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='运行UT或ST测试')
    parser.add_argument('-ut', '--ut', action='store_true', help='运行单元测试(UT)')
    parser.add_argument('-st', '--st', action='store_true', help='运行系统测试(ST)')
    args = parser.parse_args()

    try:
        # 1. 获取脚本所在目录（msOpGen根目录）
        script_dir = Path(__file__).parent.absolute()
        print(f"脚本目录: {script_dir}")

        # 默认同时运行UT和ST
        run_ut = args.ut
        run_st = args.st
        
        if not run_ut and not run_st:
            print("未指定测试类型，默认运行UT和ST测试...")
            run_ut = run_st = True

        # 2. 动态查找 msOpST 所在目录
        msopst_root = find_msopst_root(script_dir)
        print(f"找到 msopst 所在目录: {msopst_root}")

        # 3. 定义源码目录
        msopst_source_code = msopst_root / "st"
        msopst_testcase = script_dir / "test_msopst"


        msopgen_source_code = Path(os.path.realpath(os.path.join(script_dir,"../msopgen")))
        msopgen_testcase = Path(os.path.realpath(os.path.join(script_dir,"test_msopgen")))
        # 7. 设置 PYTHONPATH
        run_env = os.environ.copy()
        python_paths = [
            str(msopst_root.parent),             # msOpGen/tools
            str(script_dir / "test_msopst"),     # test_msopst 目录
            str(msopgen_source_code.parent),
            str(msopgen_testcase.parent)
        ]
        if 'PYTHONPATH' in run_env:
            python_paths.append(run_env['PYTHONPATH'])
        run_env['PYTHONPATH'] = ':'.join(python_paths)
        print(f"设置 PYTHONPATH: {run_env['PYTHONPATH']}")

        # 执行测试
        return_codes = []
        all_passed = True
        
        # 按顺序执行测试
        if run_ut:
            print("\n========== 正在运行单元测试(UT) ==========")
            return_code = run_single_test(script_dir, msopst_testcase, msopst_source_code, 'ut', run_env)
            return_codes.append(('msopst UT', return_code))
            if return_code != 0:
                all_passed = False
            return_code = run_single_test(script_dir, msopgen_testcase, msopgen_source_code, 'ut', run_env)
            return_codes.append(('msopgen UT', return_code))
            if return_code != 0:
                all_passed = False
            
        if run_st:
            print("\n========== 正在运行系统测试(ST) ==========")
            return_code = run_single_test(script_dir, msopst_testcase, msopst_source_code, 'st', run_env)
            return_codes.append(('msopst ST', return_code))
            if return_code != 0:
                all_passed = False
            return_code = run_single_test(script_dir, msopgen_testcase, msopgen_source_code, 'st', run_env)
            return_codes.append(('msopgen ST', return_code))
            if return_code != 0:
                all_passed = False

        # 汇总结果
        print("\n========== 测试结果汇总 ==========")
        for test_type, code in return_codes:
            status = "通过" if code == 0 else "失败"
            print(f"{test_type}测试: {status}")
        
        if all_passed:
            print("\n所有测试通过！")
            sys.exit(0)
        else:
            print("\n部分测试失败！")
            sys.exit(1)

    except Exception as e:
        print(f"\n错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
