import os
import sys
import json
from shutil import copytree, copy
import unittest
import pytest
import subprocess
from unittest import mock
from msopgen.interface.const_manager import ConstManager
from msopgen.interface.arg_parser import ArgParser
from msopgen.interface.op_file_compile import OpFileCompile
from msopgen.interface import utils
from msopgen.simulator import utils as sim_utils
from msopgen import msopgen
from test_msopgen.util import test_utils
from msopgen.simulator.table_gen import TableGen
from msopgen.interface.op_file_aicore import OpFileAiCore
from msopgen.interface.op_info_ir import IROpInfo
from msopgen.interface.op_info_ir_json import JsonIROpInfo
from msopgen.interface.utils import CheckFromConfig
from msopgen.interface.utils import fix_name_is_upper
sys.path.append(os.path.dirname(__file__)+"/../../")
 
base_dir = os.path.dirname(os.path.abspath(__file__))
OUT_PATH_VALID = os.path.join(base_dir, 'msopgen/res')
if not os.path.exists(OUT_PATH_VALID):
    os.makedirs(OUT_PATH_VALID)

IR_JSON_PATH = os.path.join(base_dir, 'res/IR_json.json')
MS_JSON_PATH = os.path.join(base_dir, 'res/MS_json.json')
IR_EXCEL_PATH = os.path.join(base_dir, 'res/IR_excel.xlsx')

IR_JSON_GOLDEN_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_json/golden_output')
IR_JSON_GOLDEN_OUTPUT_CPP = os.path.join(base_dir, 'msopgen/golden/golden_from_json/golden_output_cpp')
IR_JSON_GOLDEN_OUTPUT_ACLNN_CPP = os.path.join(base_dir, 'msopgen/golden/golden_from_json/golden_output_aclnn_cpp')
IR_JSON_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_json/output')

MS_JSON_GOLDEN_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_json/golden_output')
MS_JSON_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_json/output')

MS_SQUARE_INPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_txt/input/square.txt')
MS_SUM_INPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_txt/input/sum.txt')

MS_TXT_GOLDEN_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_txt/golden_output')
MS_TXT_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_ms_txt/output')

IR_EXCEL_GOLDEN_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_excel/golden_output')
IR_EXCEL_OUTPUT = os.path.join(base_dir, 'msopgen/golden/golden_from_excel/output')

SIMULATOR_DUMP = os.path.join(base_dir, 'msopgen/simulator')
parent_dir = os.path.dirname(base_dir)
parent_parent_dir = os.path.dirname(os.path.dirname(base_dir))
# 遍历该目录及其所有子目录和文件
os.chmod(parent_parent_dir, 0o755)
for root, dirs, files in os.walk(parent_dir):
    # 设置所有子目录为 755 (drwxr-xr-x)
    for d in dirs:
        dir_path = os.path.join(root, d)
        try:
            os.chmod(dir_path, 0o755)
            print(f"Set directory permission 755 for: {dir_path}")
        except Exception as e:
            print(f"Failed to set permission for {dir_path}: {str(e)}")
    # 设置所有文件为 644 
    for f in files:
        file_path = os.path.join(root, f)
        try:
            os.chmod(file_path, 0o644)
            print(f"Set file permission 644 for: {file_path}")
        except Exception as e:
            print(f"Failed to set permission for {file_path}: {str(e)}")

print("Permission setting completed.")
class Process():
    def __init__(self, return_code=1):
        self.returncode = return_code

    def communicate(self):
        obj_file = os.path.join(OUT_PATH_VALID, "aicore.bin.0")
        os.fdopen(os.open(obj_file, ConstManager.WRITE_FLAGS, ConstManager.EXECUTABLE_MODE), 'w')
        return "None", ""


class TestUtilsMethods(unittest.TestCase):

    @staticmethod
    def _copy_src_to_dst():
        """
        copy_src_to_dst
        """
        src_tbe = os.path.join(IR_JSON_GOLDEN_OUTPUT, 'tbe')
        src_proto = os.path.join(IR_JSON_GOLDEN_OUTPUT, 'op_proto')
        src_cpukernel = os.path.join(IR_JSON_GOLDEN_OUTPUT, 'cpukernel')
        src_framework = os.path.join(IR_JSON_GOLDEN_OUTPUT, 'framework')
        dst_name = os.path.join(IR_JSON_OUTPUT, 'sample')
        dst_tbe = os.path.join(dst_name, 'tbe')
        dst_proto = os.path.join(dst_name, 'op_proto')
        dst_cpukernel = os.path.join(dst_name, 'cpukernel')
        dst_framework = os.path.join(dst_name, 'framework')
        if not os.path.exists(dst_name):
            os.makedirs(dst_name, mode=0o700)
        copytree(src_tbe, dst_tbe)
        copytree(src_proto, dst_proto)
        copytree(src_cpukernel, dst_cpukernel)
        copytree(src_framework, dst_framework)
        return dst_name

    @pytest.mark.skip 
    def test_gen_tf_caffe_onnx_from_ir_json_compare_success(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        args = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        args1 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'caffe', '-c',
                 'ai_core-ascend310', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT,
                 '-m', '1']
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args1):
                msopgen.main()
        args2 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'caffe', '-c',
                 'aicpu', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT,
                 '-m', '1']
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args2):
                msopgen.main()
        args3 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'onnx', '-c',
                 'aicpu', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT,
                 '-m', '1']
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args3):
                msopgen.main()
        args4 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'onnx', '-c',
                 'ai_core-ascend310', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT,
                 '-m', '1']
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args4):
                msopgen.main()
        self.assertTrue(test_utils.check_result(IR_JSON_OUTPUT,
                                                IR_JSON_GOLDEN_OUTPUT))
        args5 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-out', IR_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args5):
                with mock.patch('msopgen.interface.const_manager.ConstManager.CANN_HOME_PATH', "/usr/local/Ascend/"):
                    msopgen.main()
        args6 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                 'ai_core-ascend310', '-op', 'conv2D', '-out', IR_JSON_OUTPUT,
                 '-m', '1']
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args6):
                msopgen.main()
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        args7 = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-lan', 'cpp', '-out', IR_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args7):
                msopgen.main()

    def test_gen_ms_aicore_tf_from_ms_json_compare_success(self):
        test_utils.clear_out_path(MS_JSON_OUTPUT)
        args = ['msopgen', 'gen', '-i', MS_JSON_PATH, '-f', 'MS', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-out', MS_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        self.assertTrue(test_utils.check_result(MS_JSON_OUTPUT,
                                                MS_JSON_GOLDEN_OUTPUT))

    def test_gen_ms_aicore_from_tf_txt_compare_success(self):
        test_utils.clear_out_path(MS_TXT_OUTPUT)
        args = ['msopgen', 'gen', '-i', MS_SQUARE_INPUT, '-f', 'ms', '-c',
                'ai_core-ascend310', '-out', MS_TXT_OUTPUT]       
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        args1 = ['msopgen', 'gen', '-i', MS_SUM_INPUT, '-f', 'mindspore',
                 '-c', 'ai_core-ascend310', '-out', MS_TXT_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args1):
                msopgen.main()
        self.assertTrue(test_utils.check_result(MS_TXT_OUTPUT,
                                                MS_TXT_GOLDEN_OUTPUT))

    def test_gen_ms_aicpu_from_tf_txt_compare_success(self):
        test_utils.clear_out_path(MS_TXT_OUTPUT)
        args = ['msopgen', 'gen', '-i', MS_SQUARE_INPUT, '-f', 'ms', '-c',
                'aicpu', '-out', MS_TXT_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        args1 = ['msopgen', 'gen', '-i', MS_SUM_INPUT, '-f', 'mindspore',
                 '-c', 'aicpu', '-out', MS_TXT_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args1):
                msopgen.main()
        args2 = ['msopgen', 'gen', '-i', MS_SUM_INPUT, '-f', 'mindspore',
                 '-c', 'aicpu', '-out', MS_TXT_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args2):
                with mock.patch('msopgen.interface.const_manager.ConstManager.CANN_HOME_PATH', "/usr/local/Ascend/"):
                    msopgen.main()

    def test_gen_compile_expect_error(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        dst_name = self._copy_src_to_dst()
        args = ['msopgen', 'compile', '-i', dst_name, '-c', '/usr/local/Ascend/latest']
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.interface.arg_parser.ArgParser._check_compile_path', return_value=True):
                    with mock.patch('msopgen.interface.utils.check_path_valid'):
                        with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_template_compile_file'):
                            with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_framework_cmake'):
                                with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_src_to_dst'):
                                    with mock.patch('msopgen.interface.const_manager.ConstManager.CANN_HOME_PATH',
                                                    "/test/ascend/"):
                                        with mock.patch('os.path.isdir', return_value=False):
                                            argument = ArgParser()
                                            op_project_compile = OpFileCompile(argument)
                                            op_project_compile.copy_template_files(dst_name)
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

        os.chdir(os.path.dirname(__file__) + "/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.interface.arg_parser.ArgParser._check_compile_path', return_value=True):
                    with mock.patch('msopgen.interface.utils.check_path_valid'):
                        with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_framework_cmake'):
                            with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_src_to_dst'):
                                with mock.patch('msopgen.interface.const_manager.ConstManager.CANN_HOME_PATH',
                                                "/test/ascend/"):
                                    with mock.patch('os.path.isdir', return_value=False):
                                        argument = ArgParser()
                                        op_project_compile = OpFileCompile(argument)
                                        op_project_compile._copy_deliverable_cmake_file(dst_name)
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)
        os.chdir(os.path.dirname(__file__) + "/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)

    @pytest.mark.skipif(sys.version_info > (3, 9), reason="Can not read xlsx on py>3.9")
    def test_gen_tf_from_ir_excel_compare_success(self):
        test_utils.clear_out_path(IR_EXCEL_OUTPUT)
        args = ['msopgen', 'gen', '-i', IR_EXCEL_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2DTik', '-out', IR_EXCEL_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        self.assertTrue(test_utils.check_result(IR_EXCEL_OUTPUT,
                                                IR_EXCEL_GOLDEN_OUTPUT))

    def test_gen_tf_cpp_from_ir_json_compare_success(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        args = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-lan', 'cpp', '-out', IR_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()

        self.assertTrue(test_utils.check_result(IR_JSON_OUTPUT,
                                                IR_JSON_GOLDEN_OUTPUT_CPP))

    def test_gen_aclnn_cpp_from_ir_json_compare_success(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        args = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'aclnn', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-lan', 'cpp', '-out', IR_JSON_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopgen.main()
        self.assertTrue(test_utils.check_result(IR_JSON_OUTPUT,
                                                IR_JSON_GOLDEN_OUTPUT_ACLNN_CPP))

    def test_arg_parser_expection_1(self):
        argument1 = ['msopgen']
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', argument1):
                args = ArgParser()
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)            
        argument3 = ['msopgen', 'gen', '-i', IR_EXCEL_PATH, '-f', 'test', '-c',
                     'ai_core-ascend310', '-op', 'Conv2DTik', '-out', IR_EXCEL_OUTPUT]
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', argument3):
                args = ArgParser()          
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_CONFIG_UNSUPPORTED_FMK_TYPE_ERROR)
        argument5 = ['msopgen', 'gen', '-i', '/root/test.txt', '-f', 'tf', '-c',
                     'ai_core-ascend310', '-op', 'Conv2DTik', '-out', IR_EXCEL_OUTPUT]
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', argument5):
                args = ArgParser()
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_read_json_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.read_json_file('home/json_read')
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_OPEN_FILE_ERROR)

    def test_load_json_expection(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.json_load('home/json_read', '')
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_READ_FILE_ERROR)

    def test_check_path_valid1(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.check_path_valid('', True)
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_make_dirs(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.isdir', return_value=False):
                with mock.patch('os.makedirs', side_effect=OSError):
                    utils.make_dirs('/home/test1')
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_MAKE_DIRS_ERROR)

    def test_read_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.read_file("/home/test_read_file")
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_READ_FILE_ERROR)

    def test_write_json_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.fdopen', side_effect=IOError):
                utils.write_json_file('/home/test1', "ok")
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_WRITE_FILE_ERROR)

    def test_check_ir_format(self):
        # with pytest.raises(utils.MsOpGenException) as error:
        #     with mock.patch('os.fdopen', side_effect=IOError):
        config = utils.CheckFromConfig()
        res = config.check_ir_format("ND")
        self.assertEqual(res, ["ND"])

    def test_compile_project(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        dst_name = self._copy_src_to_dst()
        args = ['msopgen', 'compile', '-i', dst_name, '-c', '/usr/local/Ascend/latest']
        with pytest.raises(SystemExit):
            with mock.patch(
                    'msopgen.interface.utils.check_path_valid'):
                with mock.patch('builtins.open') as open_file, \
                        mock.patch('os.fdopen'):
                    open_file.write = None
                    with mock.patch(
                            'msopgen.interface.op_file_compile.OpFileCompile._execute_command'):
                        with mock.patch('sys.argv', args):
                            msopgen.main()
        os.chdir(os.path.dirname(__file__)+"/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)

    def test_copy_template_files(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        dst_name = self._copy_src_to_dst()
        args = ['msopgen', 'compile', '-i', dst_name, '-c', '/usr/local/Ascend/latest']
        with mock.patch('sys.argv', args):
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch('msopgen.interface.utils.check_path_valid'):
                    with mock.patch('msopgen.interface.op_file_compile.OpFileCompile._copy_src_to_dst'):
                        argument = ArgParser()
                        op_project_compile = OpFileCompile(argument)
                        op_project_compile.copy_template_files(dst_name)
        os.chdir(os.path.dirname(__file__) + "/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)

    def test_replace_build_content(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        with mock.patch(
                'msopgen.interface.utils.check_path_valid'):
            with mock.patch('builtins.open') as open_file, \
                    mock.patch('os.fdopen'):
                open_file.write = None
                OpFileCompile._replace_build_content('./build.sh', 'aa', 'nn')
        os.chdir(os.path.dirname(__file__) + "/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)

    def test_copy_src_to_dst(self):
        test_utils.clear_out_path(IR_JSON_OUTPUT)
        dst_name = self._copy_src_to_dst()
        template_proj_path = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], '..', '..',
            'msopgen', 'interface',
            ConstManager.OP_TEMPLATE_PATH)
        args = ['msopgen', 'compile', '-i', dst_name, '-c',
                '/usr/local/Ascend/latest']
        with mock.patch('sys.argv', args):
            with mock.patch('msopgen.interface.utils.check_path_valid'), \
                    mock.patch('os.path.exists', return_value=True):
                with mock.patch('os.listdir',
                                return_value=['tbe', 'cmake', 'build.sh']):
                    with mock.patch('shutil.copytree'), mock.patch(
                            'shutil.copy2'):
                        with mock.patch(
                                'msopgen.interface.op_file_compile.OpFileCompile._copy_cmake_file'):
                            argument = ArgParser()
                            op_project_compile = OpFileCompile(argument)
                            op_project_compile._copy_template_compile_file(
                                template_proj_path, dst_name)
        os.chdir(os.path.dirname(__file__) + "/../../")
        test_utils.clear_out_path(IR_JSON_OUTPUT)

    def test_invalid_op_language(self):
        args = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
            'ai_core-ascend310', '-op', 'Conv2D', '-lan', 'XXX', '-out', IR_JSON_OUTPUT]
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', args):
                arg_parser = ArgParser()
        self.assertTrue(error.value.args[0], 1005)
    
    def test_windows2(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'gen', '-i', IR_JSON_PATH, '-f', 'tf', '-c',
                'ai_core-ascend310', '-op', 'Conv2D', '-lan', 'cpp', '-out', IR_JSON_OUTPUT]
        def get_system():
            return'Windows'
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                with mock.patch('platform.system', get_system):
                    msopgen.main()

    def test_check_type_format_length_equal_lengths(self):
        mock_argument = mock.MagicMock()
        mock_argument.input_path = 'input_path0'
        mock_argument.gen_flag = False
        mock_argument.output_path = 'output_path0'
        mock_argument.op_type = 'op_type0'
        mock_argument.framework = 'framework'
        mock_argument.mi_cmd = 'mi_cmd0'
        json_ir_op_info = JsonIROpInfo(mock_argument)
        check_map = {
            'name': 'test_op',
            'format': ['ND', 'NCHW'],
            'type': ['int8', 'float32']
        }
        result = json_ir_op_info.check_type_format_length(check_map)
        self.assertEqual(result, check_map)

    def test_check_type_format_length_format_length_one(self):
        mock_argument = mock.MagicMock()
        mock_argument.input_path = 'input_path1'
        mock_argument.gen_flag = False
        mock_argument.output_path = 'output_path1'
        mock_argument.op_type = 'op_type'
        mock_argument.framework = 'framework'
        mock_argument.mi_cmd = 'mi_cmd1'

        json_ir_op_info = JsonIROpInfo(mock_argument)
        check_map = {
            'name': 'test_op',
            'format': 'ND',
            'type': ['int8', 'float32']
        }
        expected_result = {
            'name': 'test_op',
            'format': ['ND', 'ND'],
            'type': ['int8', 'float32']
        }
        result = json_ir_op_info.check_type_format_length(check_map)
        self.assertEqual(result, expected_result)

    def test_check_type_format_length_type_length_one(self):
        mock_argument = mock.MagicMock()
        mock_argument.input_path = 'input_path2'
        mock_argument.gen_flag = False
        mock_argument.output_path = 'output_path2'
        mock_argument.op_type = 'op_type'
        mock_argument.framework = 'framework'
        mock_argument.mi_cmd = 'mi_cmd2'

        json_ir_op_info = JsonIROpInfo(mock_argument)
        check_map = {
            'name': 'test_op',
            'format': ['ND', 'NCHW'],
            'type': 'int8'
        }
        expected_result = {
            'name': 'test_op',
            'format': ['ND', 'NCHW'],
            'type': ['int8', 'int8']
        }
        result = json_ir_op_info.check_type_format_length(check_map)
        self.assertEqual(result, expected_result)

    def test_check_type_format_length_invalid_lengths(self):
        mock_argument = mock.MagicMock()
        mock_argument.input_path = 'input_path3'
        mock_argument.gen_flag = False
        mock_argument.output_path = 'output_path3'
        mock_argument.op_type = 'op_type'
        mock_argument.framework = 'framework'
        mock_argument.mi_cmd = 'mi_cmd3'

        json_ir_op_info = JsonIROpInfo(mock_argument)
        check_map = {
            'name': 'test_op',
            'format': ['ND', 'NCHW'],
            'type': ['int8', 'float16', 'float32']
        }
        with self.assertRaises(utils.MsOpGenException):
            json_ir_op_info.check_type_format_length(check_map)


class TestSimulatorMethods(unittest.TestCase):

    @staticmethod
    def get_parse_dump(*args):
        with open(os.path.join(SIMULATOR_DUMP, 'dump_file.json')) as fp:
            return json.load(fp)
        
    @staticmethod
    def objdump_output(*args):
        return ["0000000000000000 <add_custom>:", "/home/xx/add.cpp:114", "       0: <not available>",
                "       4: <xxx>", "/home/xx/kernel_tpipe.h:503", "      84: <not available>"]
    
    @staticmethod
    def objdump_output_with_no_bug_info(*args):
        return ["add()", "       0: <not available>", "       4: <xxx>", "      84: <not available>"]
    
    @staticmethod
    def objdump_output_file(*args):
        with open(os.path.join(SIMULATOR_DUMP, 'objdump_output.txt')) as fp:
            return fp.readlines()
        
    @staticmethod
    def objdump_checkout(*args, **kwargs):
        output = TestSimulatorMethods.objdump_output()
        return "\n".join(output).encode(encoding="utf-8")
    
    @staticmethod
    def compare_json_file(file1, file2, head=0):
        with open(file1) as f1:
            with open(file2) as f2:
                if head:
                    event1 = json.load(f1).get("traceEvents")
                    event2 = json.load(f2).get("traceEvents")
                    return event1[:head] == event2[:head]
                return json.load(f1) == json.load(f2)

    @staticmethod
    def compare_file(file1, file2):
        with open(file1) as f1:
            with open(file2) as f2:
                return f1.readlines() == f2.readlines()

    def test_simulator_output_json_success(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.simulator.parse_dump.ParseDump.parse_dump_files',
                                TestSimulatorMethods.get_parse_dump):
                    msopgen.main()
        self.assertEqual(error.value.code, 0)

    def test_simulator_output_json_success_with_ascend910b(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-subc', 'veccore0', '-out', OUT_PATH_VALID]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.simulator.parse_dump.ParseDump.parse_dump_files',
                                TestSimulatorMethods.get_parse_dump):
                    msopgen.main()
        self.assertEqual(error.value.code, 0)

    def test_simulator_output_json_success_with_code_line(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-subc', 'veccore0', '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'test.o')]
        
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.simulator.parse_objdump.RelocParser._execute_objdump',
                                TestSimulatorMethods.objdump_output):
                    msopgen.main()
        self.assertEqual(error.value.code, 0)

    def test_arg_parser_expection_2(self):
        argument1 = ['msopgen']
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', argument1):
                args = ArgParser()
        self.assertEqual(error.value.args[0],
                         ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)
        # 缺少参数
        argument2 = ['msopgen', 'sim']
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', argument2):
                args = ArgParser()
        self.assertEqual(error.value.code, 2)
        
        # 缺少参数
        argument3 = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', argument3):
                args = ArgParser()
        self.assertEqual(error.value.code, 2)
        
        # core_id 错误
        argument4 = ['msopgen', 'sim', '-c', 'wrongcore0', '-d', SIMULATOR_DUMP,
                     '-out', OUT_PATH_VALID]
        with pytest.raises(sim_utils.Dump2TraceException) as error:
            with mock.patch('sys.argv', argument4):
                args = ArgParser()
        self.assertIsInstance(error.value, sim_utils.Dump2TraceException)

        # dump path 错误
        argument4 = ['msopgen', 'sim', '-c', 'core0', '-d', "wrong_dump_path",
                     '-out', OUT_PATH_VALID]
        with pytest.raises(sim_utils.Dump2TraceException) as error:
            with mock.patch('sys.argv', argument4):
                args = ArgParser()
        self.assertIsInstance(error.value, sim_utils.Dump2TraceException)

        # output path 不存在
        argument5 = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                     '-out', "wrong_output_path"]
        with mock.patch('sys.argv', argument5):
            args = ArgParser()
        self.assertEqual(args.output, "wrong_output_path")

        # .o 路径文件错误
        argument6 = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                     '-out', OUT_PATH_VALID, '-reloc', os.path.join(SIMULATOR_DUMP, 'wrong.o')]
        with pytest.raises(sim_utils.Dump2TraceException) as error:
            with mock.patch('sys.argv', argument6):
                args = ArgParser()
        self.assertIsInstance(error.value, sim_utils.Dump2TraceException)

        # subcore_id 错误
        argument4 = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                     '-subc', 'wrong_subcore_id', '-out', OUT_PATH_VALID]
        with pytest.raises(sim_utils.Dump2TraceException) as error:
            with mock.patch('sys.argv', argument4):
                args = ArgParser()
        self.assertIsInstance(error.value, sim_utils.Dump2TraceException)

    def test_simulator_output_json_with_no_debug_info_reloc(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'test.o')]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.simulator.parse_objdump.RelocParser._execute_objdump',
                                TestSimulatorMethods.objdump_output_with_no_bug_info):
                    msopgen.main()
        self.assertEqual(error.value.code, ConstManager.MS_OP_GEN_SIMULATOR_ERROR)

    def test_simulator_output_json_right(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-subc', 'veccore0', '-out', OUT_PATH_VALID]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('msopgen.simulator.trace.TraceContent.get_render_list',
                                TestSimulatorMethods.get_parse_dump):
                    msopgen.main()
        self.assertEqual(error.value.code, 0)
        file1 = os.path.realpath(os.path.join(SIMULATOR_DUMP, "dump2json_core0.json"))
        file2 = os.path.realpath(os.path.join(OUT_PATH_VALID, "dump2trace_core0.json"))
        self.assertTrue(TestSimulatorMethods.compare_json_file(file1, file2))

    def test_simulator_output_json_right_with_code_line(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'test.o')]
        import platform
        system = platform.system()

        def get_system():
            return system
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('os.getenv', return_value="ccec_compiler/bin"):
                    with mock.patch('msopgen.simulator.parse_objdump.check_execute_file', return_value=True):
                        with mock.patch('platform.system', get_system):
                            with mock.patch('subprocess.check_output',
                                            TestSimulatorMethods.objdump_checkout):
                                msopgen.main()
        self.assertEqual(error.value.code, 0)
        file1 = os.path.realpath(os.path.join(SIMULATOR_DUMP, "dump2json_core0_with_code.json"))
        file2 = os.path.realpath(os.path.join(OUT_PATH_VALID, "dump2trace_core0.json"))
        self.assertTrue(TestSimulatorMethods.compare_json_file(file1, file2, 2))

    def test_simulator_output_json_without_cce_objdump(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'test.o')]
        
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('os.getenv', lambda x: "ccec_compiler/bin"):
                    msopgen.main()
        self.assertEqual(error.value.code, ConstManager.MS_OP_GEN_SIMULATOR_ERROR)

    def test_table_generate(self):
        table_gen = TableGen(("A", "BCD", "EFGH"), [["content", "asd", "rtyxxxxxx"], ["aaaaaaaaaaaaa", "sxza", "a"]])
        actual = table_gen.get_table_str()
        expect = "+------------------+--------+--------------+\n" + \
                 "|        A         |  BCD   |     EFGH     |\n" + \
                 "+------------------+--------+--------------+\n" + \
                 "|     content      |  asd   |  rtyxxxxxx   |\n" + \
                 "|  aaaaaaaaaaaaa   |  sxza  |      a       |\n" + \
                 "+------------------+--------+--------------+\n"
        self.assertEqual(actual, expect)

    def test_code_hot_line_file(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'test.o')]
        import platform
        system = platform.system()

        def get_system():
            return system
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('os.getenv', return_value="ccec_compiler/bin"):
                    with mock.patch('msopgen.simulator.parse_objdump.check_execute_file', return_value=True):
                        with mock.patch('platform.system', get_system):
                            with mock.patch('subprocess.check_output',
                                            TestSimulatorMethods.objdump_checkout):
                                msopgen.main()
        self.assertEqual(error.value.code, 0)
        file1 = os.path.realpath(os.path.join(SIMULATOR_DUMP, "code_exe_prof.csv"))
        file2 = os.path.realpath(os.path.join(OUT_PATH_VALID, "core0_code_exe_prof.csv"))
        self.assertTrue(TestSimulatorMethods.compare_file(file1, file2))

    def test_reloc_is_executable_file(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', SIMULATOR_DUMP,
                '-out', OUT_PATH_VALID,
                '-reloc', os.path.join(SIMULATOR_DUMP, 'aicore.bin.0')]
        import platform
        system = platform.system()

        process = Process(0)
        def get_system():
            return system
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('os.getenv', return_value="ccec_compiler/bin"):
                    with mock.patch('msopgen.simulator.parse_objdump.check_execute_file', return_value=True):
                        with mock.patch('platform.system', get_system):
                            with mock.patch('subprocess.check_output',
                                            TestSimulatorMethods.objdump_checkout):
                                with mock.patch('subprocess.Popen', return_value=process):
                                    with mock.patch('msopgen.simulator.utils.CheckPath.check_file', return_value="not empty"):
                                        msopgen.main()
        self.assertEqual(error.value.code, 0)

    def test_reg_dump_parser(self):
        from msopgen.simulator.reg_dump_parser import RegDumpParser
        for path in [os.path.join(os.path.realpath(SIMULATOR_DUMP), f"core{c}_reg_log.dump") for c in range(1, 3)]:
            rdp = RegDumpParser(path)
            first_pc = rdp.get_start_pc()
            self.assertTrue(first_pc)

    def test_mixcore_normal(self):
        test_utils.clear_out_path(OUT_PATH_VALID)
        for dump_name in ["instr", "dcache", "instr_popped"]:
            src = os.path.join(SIMULATOR_DUMP, f"core0.veccore0.{dump_name}_log.dump")
            os.makedirs(os.path.join(OUT_PATH_VALID, 'dump'), ConstManager.DIR_MODE, exist_ok=True)
            dst1 = os.path.join(OUT_PATH_VALID, 'dump', f"core0.veccore0.{dump_name}_log.dump")
            dst2 = os.path.join(OUT_PATH_VALID, 'dump', f"core0.cubecore0.{dump_name}_log.dump")
            copy(src, dst1)
            copy(src, dst2)
        args = ['msopgen', 'sim', '-c', 'core0', '-d', os.path.join(OUT_PATH_VALID, 'dump'),
                '-mix', '-out', OUT_PATH_VALID]
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                msopgen.main()
        self.assertEqual(error.value.code, 0)
        file1 = os.path.realpath(os.path.join(SIMULATOR_DUMP, "dump2json_mixcore.json"))
        file2 = os.path.realpath(os.path.join(OUT_PATH_VALID, "dump2trace_core0.json"))
        self.assertTrue(TestSimulatorMethods.compare_json_file(file1, file2, 3))

    def test_out_of_range_abnormal(self):
        argument = ['msopgen', 'gen', '-i', '/root/test.txt', '-f', 'tf', '-c',
                    'ai_core-ascend310', '-op', 'Conv2DTik', '-out', IR_EXCEL_OUTPUT]
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('sys.argv', argument):
                args = ArgParser()
                opfile = OpFileAiCore(args)
                self.assertEqual(opfile.super()._generate_attr([], []), [])
                iropinfo = IROpInfo(args)
                self.assertEqual(iropinfo._del_with_row_col([], []), None)
                self.assertEqual(IROpInfo._deal_with_ir_map([], {}), {})
                jsoniropinfo = JsonIROpInfo(args)
                self.assertEqual(jsoniropinfo._update_parsed_info("", "", [], []), None)
                self.assertEqual(utils.fix_name_is_upper("name", "fix_name", 10, ""), "fix_name")
                config = utils.CheckFromConfig()
                self.assertEqual(config.get_type_number("ir_type"), 1)
                self.assertEqual(utils.check_name_valid(None), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)
                opfile.compute_unit = ["", "", ""]
                self.assertEqual(opfile.super()._make_info_cfg_file(""), None)
                self.assertEqual(opfile.super()._generate_cpp_aicore(), "")
                self.assertEqual(opfile.super()._generate_cmake_config_cpp(), None)

    def test_get_type_number_ir_type_not_in_io_dtype_map(self):
        # 创建类的实例
        check = CheckFromConfig()
        # 模拟 io_dtype_map 没有包含的 ir_type
        check.io_dtype_map = {'some_other_type': 'value'}
        # 定义一个不在 io_dtype_map 中的 ir_type
        ir_type = 'non_existent_type'
        # 调用 get_type_number 并检查返回值是否为默认值 1
        type_num = check.get_type_number(ir_type)
        self.assertEqual(type_num, 1, "Expected type_num to be 1 when ir_type is not in io_dtype_map")

    def test_len_name_less(self):
        name = "test"
        fix_name = "fixed"
        index = 10  # 设置一个比 name 长度大的索引
        name_str = "example"
        result = fix_name_is_upper(name, fix_name, index, name_str)
        # 当 len(name) < index 时，应返回 fix_name
        self.assertEqual(result, fix_name)

if __name__ == '__main__':
    unittest.main()
