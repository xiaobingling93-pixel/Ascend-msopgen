import os
import stat
import shutil
from setuptools import setup

os.environ['SOURCE_DATE_EPOCH'] = str(int(os.path.getctime(os.path.realpath(__file__))))
topDir = os.getcwd()
currentDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# 把 msopst.py “重命名”为 msopst （复制 + 去后缀 + 加可执行权限）
os.makedirs(os.path.join(topDir, 'build'), exist_ok=True)
dst = os.path.join(topDir, 'build', 'msopst')
shutil.copy(os.path.join(currentDir, 'msopst', 'scripts', 'msopst.py'), dst)
st = os.stat(dst)
os.chmod(dst, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

setup(
    name="msopst",
    version="1.0.0",
    options={
        'bdist_wheel': {
            'python_tag': 'py3'}},
    scripts=['build/msopst', 'msopst/scripts/msopst.ini'],
    packages=['msopst'],
    package_data={
        'msopst': [
            'msopst/scripts/msopst.ini',
            'msopst/st/interface/framework/framework.json',
            'msopst/st/config/white_list_config.json',
            'msopst/template/*',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires = '>=3.7'
)
