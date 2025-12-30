import subprocess
import os
import pytest
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # 根据实际目录结构调整

# 使用相对路径
MSOPST_BIN = PROJECT_ROOT / "tools" / "msopst" / "scripts" / "msopst"
INI_INPUT = PROJECT_ROOT / "test" / "test_msopst"/ "st"  / "golden" / "base_case" / "input" / "conv2_d.ini"
ST_OUTPUT = PROJECT_ROOT / "test" / "test_msopst"/ "st"  / "golden" / "base_case" / "output"
def test_msopst_execution():
    # 验证二进制文件存在
    if not os.path.exists(MSOPST_BIN):
        pytest.skip(f"msopst binary not found at: {MSOPST_BIN}")
    
    # 执行命令
    cmd = [
        "python3",
        MSOPST_BIN,
        "create",
        "-i", INI_INPUT,
        "-out", ST_OUTPUT
    ]
    
    # 运行并检查返回值
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 断言执行成功
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    print(f"Execution output: {result.stdout}")
