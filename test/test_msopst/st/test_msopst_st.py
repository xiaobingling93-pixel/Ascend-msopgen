import json
import sys
import unittest
import filecmp

import numpy as np
import pytest
from unittest import mock
import os
import stat
import importlib.util
import importlib.machinery
from msopst.st.interface import utils
from msopst.st.interface.arg_parser import MsopstArgParser
from msopst.st.interface.const_manager import ConstManager
from msopst.st.interface import model_parser
from msopst.st.interface.framework import tf_model_parser
from msopst.st.interface.framework.tf_model_parser import TFModelParse
from msopst.st.interface.result_comparer import ResultCompare
from msopst.st.interface.compare_data import CompareData
from msopst.st.interface.case_generator import CaseGenerator
from msopst.st.interface.data_generator import DataGenerator
from msopst.st.interface.st_report import OpSTReport
from msopst.st.interface.st_report import OpSTCaseReport
from msopst.st.interface.st_report import ReportJsonEncoder
from msopst.st.interface.op_st_case_info import OpSTCase
from msopst.st.interface.op_st_case_info import OpSTCaseTrace
from msopst.st.interface.acl_op_runner import AclOpRunner
from msopst.st.interface.atc_transform_om import AtcTransformOm
from msopst.st.interface.advance_ini_parser import AdvanceIniParser
from msopst.st.interface.ms_op_runner import MsOpRunner
from msopst.st.interface import acl_op_runner
from msopst.st.interface import ms_op_generator
from msopst.st.interface import case_design
from util import test_utils
from pathlib import Path
import test_pytorch_model_parser

# 动态计算正确的 op_test_frame 路径
current_file_path = Path(__file__).absolute()
project_root = current_file_path.parent.parent.parent.parent  # 从测试文件上溯4级到msOpGen目录
correct_msopst_path = project_root / "tools" / "msopst" / "scripts" / "msopst.py"

# 验证路径是否存在
if not correct_msopst_path.exists():
    # 添加调试信息
    print(f"Debug: Current file path - {current_file_path}")
    print(f"Debug: Calculated path - {correct_msopst_path}")
    print(f"Debug: Project root exists? - {project_root.exists()}")
    raise FileNotFoundError(f"测试框架路径不存在: {correct_msopst_path}")

# 使用时
op_test_frame_path = correct_msopst_path

# 动态加载模块
loader = importlib.machinery.SourceFileLoader(
    "msopst",
    str(op_test_frame_path)
)
spec = importlib.util.spec_from_loader(loader.name, loader)
msopst = importlib.util.module_from_spec(spec)
loader.exec_module(msopst)

# TBE OPERATOR INPUT/OUTPOUT
ST_GOLDEN_OUTPUT = './test_msopst/st/golden/base_case/golden_output/tbe'
ST_OUTPUT = './test_msopst/st/golden/base_case/output/'
INI_INPUT = './test_msopst/st/golden/base_case/input/conv2_d.ini'
MODEL_ARGS = str(project_root /'test/test_msopst/st/golden/base_case/input/add.pb')
ST_GOLDEN_OP_RESULT_TXT = './test_msopst/st/golden/base_case/input' \
                          '/result.txt'
ST_GOLDEN_ABNORMAL_CASE_JSON_INPUT = './test_msopst/st/golden/base_case/input'\
                                     '/test_add_abnormal_case.json'
ST_GOLDEN_ATC_FAILED_JSON_INPUT = './test_msopst/st/golden/base_case/input/' \
                                  'test_add_when_atc_failed.json'

# AICPU_PARSE_HEAD_FILE OUTPUT
BUCKETIZE_INI_INPUT = './test_msopst/st/golden/base_case/golden_output/aicpu' \
                          '/cpukernel/op_info_cfg/aicpu_kernel/bucketize.ini'
TOPK_INI_INPUT = './test_msopst/st/golden/base_case/golden_output/aicpu' \
                          '/cpukernel/op_info_cfg/aicpu_kernel/top_k.ini'
LESS_INI_INPUT = './test_msopst/st/golden/base_case/golden_output/aicpu' \
                          '/cpukernel/op_info_cfg/aicpu_kernel/less.ini'
CAST_INI_INPUT = './test_msopst/st/golden/base_case/golden_output/aicpu' \
                          '/cpukernel/op_info_cfg/aicpu_kernel/cast.ini'
AICPU_CASE_JSON_GOLDEN_OUTPUT = './test_msopst/st/golden/base_case/golden_output' \
                                '/aicpu/json'

# paramType: optional OUTPUT
OPTIONAL_INI_INPUT = './test_msopst/st/golden/base_case/input/Pooling.ini'
OPTIONAL_ST_GOLDEN_OUTPUT = './test_msopst/st/golden/base_case/' \
                            'golden_output/optional_input'
ST_GOLDEN_OP_CASE_JSON_INPUT = './test_msopst/st/golden/base_case/input' \
                               '/Pooling_case_20210225145706.json'
ST_GOLDEN_ACL_PROJECT_OUTPUT_TESTCASE = './test_msopst/st/golden/base_case/golden_output' \
                                   '/gen_optional_acl_prj/Pooling/src/testcase.cpp'
ST_GOLDEN_ACL_PROJECT_ORIGIN_OUTPUT_TESTCASE = './test_msopst/st/golden/base_case/golden_output' \
                                   '/gen_optional_acl_prj/Pooling/src/testcase_ori.cpp'
ST_GOLDEN_ACL_PROJECT_OUTPUT_RUN = './test_msopst/st/golden/base_case/golden_output' \
                                   '/gen_optional_acl_prj/Pooling/run/out'\
                                   '/test_data/config/'
MSOPST_CONF_INI = './test_msopst/st/golden/base_case/input/msopst.ini'

# dynamic shape
ST_GOLDEN_OP_DYNAMIC_SHAPE_INI_INPUT = './test_msopst/st/golden/base_case/input' \
                                       '/add.ini'

ST_GOLDEN_OP_DYNAMIC_SHAPE_JSON_INPUT = './test_msopst/st/golden/base_case/input' \
                                        '/add_case.json'
ST_GOLDEN_DYNAMIC_SHAPE_TESTCASE = './test_msopst/st/golden/base_case/golden_output/' \
                                   'gen_optional_acl_prj/Add/src/testcase.cpp'

# MINDSPORE OPERATOR INPUT/OUTPOUT
ST_MS_GOLDEN_JSON_OUTPUT = './test_msopst/st/golden/base_case/golden_output' \
                           '/mindspore/json'
ST_MS_GOLDEN_INPUT_JSON = './test_msopst/st/golden/base_case/input/ms_st_report.json'

ST_GOLDEN_OP_GEN_WITH_VALUE_JSON_INPUT = './test_msopst/st/golden/base_case/input' \
                                             '/test_value_add.json'
ST_GOLDEN_OP_GEN_WITH_VALUE_ACL_PROJECT_OUTPUT = './test_msopst/st/golden/base_case' \
                                                 '/golden_output/' \
                                                 'gen_optional_acl_prj/Adds/src/testcase.cpp'
ST_MS_GOLDEN_INPUT_JSON_WITH_VALUE = './test_msopst/st/golden/base_case/input/ms_case_with_value.json'
ST_PT_GOLDEN_INPUT_JSON = './test_msopst/st/golden/base_case/input/pt_torch_api_caste.json'
ST_GOLDEN_OP_FUZZ_CASE_JSON_INPUT = './test_msopst/st/golden/base_case/input' \
                                    '/test_add_fuzz.json'
ST_GOLDEN_OP_FUZZ_CASE_OUTPUT_SRC = './test_msopst/st/golden/base_case/golden_output' \
                                   '/fuzz/Add/src/testcase.cpp'
ST_GOLDEN_OP_FUZZ_CASE_OUTPUT_RUN = './test_msopst/st/golden/base_case/golden_output' \
                                   '/fuzz/Add/run/out'\
                                   '/test_data/config/'
ST_GOLDEN_MS_FUZZ_CASE_JSON_INPUT = './test_msopst/st/golden/base_case/input' \
                                    '/ms_case_fuzz.json'
ST_GOLDEN_MS_FUZZ_CASE_OUTPUT_SRC = './test_msopst/st/golden/base_case/golden_output' \
                                   '/fuzz/Square/src'
# const input
ST_GOLDEN_CONST_INPUT_VALUE_JSON = './test_msopst/st/golden/base_case/input' \
                                    '/const_input_with_value.json'
ST_GOLDEN_CONST_INPUT_DATA_DISTRIBUTE_JSON = './test_msopst/st/golden/base_case/input' \
                                    '/const_input_with_data_distribute.json'
ST_GOLDEN_CONST_INPUT_NO_VALUE_JSON = './test_msopst/st/golden/base_case/input' \
                                    '/const_input_with_no_value.json'
ST_GOLDEN_SCALAR_INPUT_WITH_VALUE_JSON = './test_msopst/st/golden/base_case/input' \
                                    '/scalar_input_with_value.json'
# attr support data type
ST_GOLDEN_ATTR_SUPPORT_DATA_TYPE_JSON = './test_msopst/st/golden/base_case/input' \
                                    '/test_attr_support_data_type.json'
ST_GOLDEN_ATTR_SUPPORT_DATA_TYPE_TESTCASE = './test_msopst/st/golden/base_case/golden_output' \
                                        '/gen_optional_acl_prj/TestOp/testcase.cpp'
ST_GOLDEN_ATTR_SUPPORT_DATA_TYPE_ACL_JSON = './test_msopst/st/golden/base_case/golden_output' \
                                            '/gen_optional_acl_prj/TestOp/acl_op.json'
# const input golden files.
ST_GOLDEN_CONST_INPUT_SRC_TESTCASE = './test_msopst/st/golden/base_case/golden_output' \
                                        '/gen_optional_acl_prj/ResizeBilinearV2/src/testcase.cpp'
ST_GOLDEN_CONST_INPUT_SRC_OP_EXECUTE = './test_msopst/st/golden/base_case/golden_output' \
                                       '/gen_optional_acl_prj/ResizeBilinearV2/src/op_execute.cpp'
ST_GOLDEN_CONST_INPUT_CONFIG_ACL_OP = './test_msopst/st/golden/base_case/golden_output' \
                                        '/gen_optional_acl_prj/ResizeBilinearV2/config/acl_op.json'
ST_GOLDEN_SCALAR_INPUT_SRC_TESTCASE = './test_msopst/st/golden/base_case/golden_output' \
                                        '/gen_optional_acl_prj/const_input/TestScalar/testcase.cpp'
ST_GOLDEN_SCALAR_INPUT_CONFIG_ACL_OP = './test_msopst/st/golden/base_case/golden_output' \
                                        '/gen_optional_acl_prj/const_input/TestScalar/acl_op.json'

ST_GOLDEN_OP_ADD_REPORT_JSON_INPUT = './test_msopst/st/golden/base_case/input/add_st_report.json'
ST_GOLDEN_OP_POOLING_REPORT_JSON_INPUT = './test_msopst/st/golden/base_case/input/pooling_st_report.json'
ST_REPORT = './test_msopst/st/golden/base_case/input/golden_st_report.json'

ST_GOLDEN_TORCH_API_OUTPUT = "./test_msopst/st/golden/base_case/golden_output/torch_npu_api"

ASCENDC_HOST_CPP_FILE = './test_msopst/st/golden/base_case/input/add_ascendc.cpp'
ASCENDC_ST_GOLDEN_OUTPUT = './test_msopst/st/golden/base_case/golden_output/ascendc'

ASCENDC_ST_CASE_JSON = './test_msopst/st/golden/base_case/input/ascendc/AddAscendC_case.json'
ASCENDC_KERNEL_CPP_FILE = './test_msopst/st/golden/base_case/input/ascendc/add_ascendc.cpp'

WRITE_FLAGS = os.O_WRONLY | os.O_CREAT
WRITE_MODES = stat.S_IWUSR | stat.S_IRUSR


class NumpyArrar:
    def tofile(self, file_path):
        pass

class CaseInfo:
    def __init__(self, er_thr):
        self.op_params = {"error_threshold": er_thr}


class Args:
    def __init__(self, input_file, output_path, model_path):
        self.input_file = input_file
        self.output_path = output_path
        self.model_path = model_path
        self.quiet = False


class MyMsOpRunner(MsOpRunner):
    def execute_command(self, cmd):
        self._execute_command(cmd)


class MyCaseGenerator(CaseGenerator):
    def get_default_attr_value(self, attr_type, default_value_str, attr_name):
        return self._get_default_attr_value(attr_type, default_value_str, attr_name)


def compare_context(src_name, dst_name):
    if not filecmp.cmp(src_name, dst_name):
        print(" %s VS %s return false." % (src_name, dst_name))
        return False
    return True

class TestUtilsMethods(unittest.TestCase):

    def test_check_path_valid(self):
        args = ['aaa.py', 'create', '-i', '/home/a.ini']
        with pytest.raises(SystemExit) as error:
            with mock.patch('sys.argv', args):
                with mock.patch('os.path.exists', return_value=True), \
                     mock.patch('os.access', return_value=True), \
                     mock.patch('os.path.isfile', return_value=True), \
                     mock.patch('os.path.isdir', return_value=False):
                    msopst.main()
        self.assertEqual(error.value.code,
                         ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)

    def test_model_parser_1(self):
        """
        verify the abnormal scene of get_tf_model_nodes function
        in tf_model_parser.py
        """
        args = Args('./a.json', '', './a.pb')
        with pytest.raises(utils.OpTestGenException) as error:
            tf_model_parser = TFModelParse(args)
            tf_model_parser.get_tf_model_nodes("Conv2D")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)

    def test_get_info_from_model_fun(self):
        """
        verify the normal scene of _get_info_from_model function
        in case_generator.py
        """
        args = Args('./a.json', '', '')
        case_gen = CaseGenerator(args)
        item = {'name': 'data_format', 'type': 's', 'value': '"NHWC"'}
        attr = {'name': 'data_format', 'type': 'string', 'value': 'NHWC'}
        attr_list = [{'name': 'data_format',
                      'type': 'string', 'value': 'NHWC'}]
        base_case = {'case_name': 'Test_XXX_sub_case_001', 'op': 'Conv2D',
                     'input_desc':
                         [
                             {'format': ['NHWC'],
                              'type': 'float',
                              'shape': [[1, 1, 1, 4096]],
                              'data_distribute': ['uniform'],
                              'value_range': [[0.1, 1.0]],
                              'name': 'x'}
                         ],
                     'output_desc': [
                         {
                             'format': ['NHWC'],
                             'type': 'float',
                             'shape': [[1, 1, 1, 1000]],
                             'name': 'y'}]}
        case_gen._get_info_from_model(item, attr, attr_list, base_case)

    def test_model_parser_2(self):
        """
        verify the scene of get_tf_model_node function in tf_model_parser.py
        """
        args = Args('./a.json', '', MODEL_ARGS)
        with mock.patch(
                'msopst.st.interface.framework.'
                'tf_model_parser.input', return_value='n'):
            tf_model_parser = TFModelParse(args)
            tf_model_parser.get_tf_model_nodes("Conv2D")

    def test_model_parser_3(self):
        """
        verify the abnormal scene of change_shape function
        in tf_model_parser.py
        """
        args = Args('./a.json', '', MODEL_ARGS)
        lines = '{"Placeholder": ' \
                '{"ori_shape": [-1, 224, 224, 3], "new_shape": []}}'
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch(
                    'msopst.st.interface.utils.check_path_valid'):
                with mock.patch('builtins.open',
                                mock.mock_open(read_data=lines)):
                    with mock.patch('os.open') as open_file, \
                            mock.patch('os.fdopen'):
                        open_file.write = None
                        tf_model_parser = TFModelParse(args)
                        tf_model_parser.change_shape()
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_TF_CHANGE_PLACEHOLDER_ERROR)

    def test_model_parser_4(self):
        """
        verify the abnormal scene of get_model_nodes function
        in model_parser.py
        """
        args = Args('./a.json', '', './a.pbv')
        with pytest.raises(utils.OpTestGenException) as error:
            model_parser.get_model_nodes(args, '')
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)

    def test_model_parser_5(self):
        """
        verify the abnormal scene of _attr_value_shape_list function
        in tf_model_parser.py
        """
        attr_value_shape = [np.array([[1, 2], [3, 4]])]
        tf_model_parser._attr_value_shape_list(attr_value_shape)

    def test_model_parser_6(self):
        """
        verify the abnormal scene of _map_tf_input_output_dtype function
        in tf_model_parser.py
        """
        tf_dtype_list = ["float32", "float16", "int8", "int16", "int32",
                         "uint8", "uint16", "uint32", "bool", "int64"]
        for tf_dtype in tf_dtype_list:
            tf_model_parser._map_tf_input_output_dtype(tf_dtype)

    def test_model_parser_7(self):
        """
        verify the abnormal scene of get_shape function
        in tf_model_parser.py
        """
        args = Args('./a.json', '', './a.pb')
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch(
                    'msopst.st.interface.utils.check_path_valid'):
                tf_model_parser = TFModelParse(args)
                tf_model_parser.get_shape()
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_TF_LOAD_ERROR)

    def test_model_parser_new_shape_error(self):
        """
        verify the abnormal scene of change_shape function
        in tf_model_parser.py
        """
        args = Args('./a.json', '', MODEL_ARGS)
        lines = '{"Placeholder": ' \
                '{"ori_shape": [-1, 224, 224, 3], "new_shape": ["a", "b"]}}'

        class NodeMock(object):
            op = "Placeholder"
            name = "Placeholder"

        class GraphMock(object):
            node = [NodeMock]

        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch('msopst.st.interface.framework.tf_model_parser._tf_utils_load_graph_def',
                            return_value=GraphMock):
                with mock.patch('msopst.st.interface.utils.check_path_valid'):
                    with mock.patch('builtins.open', mock.mock_open(read_data=lines)):
                        with mock.patch('os.open') as open_file, mock.patch('os.fdopen'):
                            open_file.write = None
                            tf = TFModelParse(args)
                            tf.change_shape()
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_TF_CHANGE_PLACEHOLDER_ERROR)

    def test_compare_func_1(self):
        """
        verify the abnormal scene of compare function in result_comparer.py
        """
        report = OpSTReport()
        run_dir = "xxx.txt"
        err_thr = [0.01, 0.01]
        error_report = 'false'
        comparer_obj = ResultCompare(report, run_dir, err_thr, error_report)
        comparer_obj.compare()

    def test_compare_func_2(self):
        """
        verify the normal scene of compare function in result_comparer.py
        """
        report = OpSTReport()
        op_st = OpSTCase("AddN", {"calc_expect_func_file_func": 1})
        op_st_case_trace = OpSTCaseTrace(op_st)
        op_st_report = OpSTCaseReport(op_st_case_trace)
        err_thr = [0.01, 0.01]
        error_report = 'false'
        with mock.patch('msopst.st.interface.utils.check_path_valid'):
            with mock.patch(
                    'msopst.st.interface.utils.execute_command'):
                with mock.patch('os.path.exists',
                                return_value=True), mock.patch('os.chdir'):
                    with mock.patch('os.access', return_value=True):
                        with mock.patch('os.path.join',
                                        return_value=ST_GOLDEN_OP_RESULT_TXT):
                            with mock.patch(
                                    'msopst.st.interface.st_report.'
                                    'OpSTReport.get_case_report',
                                    return_value=op_st_report):
                                runner = AclOpRunner('/home', 'ddd', report)
                                runner.run()
                                comparer_obj = ResultCompare(report, ST_GOLDEN_OP_RESULT_TXT, err_thr, error_report)
                                comparer_obj.compare()

    def test_compare_func_3(self):
        """
        verify the normal scene of compare_by_path function in result_comparer.py
        """
        report = OpSTReport()
        op_st = OpSTCase("AddN", {"calc_expect_func_file_func": 1})
        op_st_case_trace = OpSTCaseTrace(op_st)
        op_st_report = OpSTCaseReport(op_st_case_trace)
        error_report = 'false'
        with mock.patch('msopst.st.interface.utils.check_path_valid'):
            with mock.patch('msopst.st.interface.utils.execute_command'):
                with mock.patch('os.path.exists',
                                return_value=True), mock.patch('os.chdir'):
                    with mock.patch('os.access', return_value=True):
                        with mock.patch('os.listdir', return_value='AddN'):
                            with mock.patch(
                                    'os.path.join',
                                    return_value=ST_GOLDEN_OP_RESULT_TXT):
                                with mock.patch(
                                        'msopst.st.interface.st_report.'
                                        'OpSTReport.get_case_report',
                                        return_value=op_st_report):
                                    runner = AclOpRunner(
                                        '/home', 'ddd', report)
                                    runner.run()
                                    ResultCompare.compare_by_path(report, ST_GOLDEN_OP_RESULT_TXT, error_report)

    def test_compare_func_4(self):
        """
        verify the normal scene of data_compare function in result_comparer.py
        """
        err_thr = [0.01, 0.01]
        npu_output = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        cpu_output = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
        npu_output_array = np.array(npu_output)
        cpu_output_array = np.array(cpu_output)
        error_report = 'false'
        compare_data_obj = CompareData('current case', err_thr, error_report, '')
        compare_data_obj.compare(npu_output_array, cpu_output_array)

    def test_compare_func_5(self):
        """
        verify the normal scene of data_compare function in result_comparer.py
        """
        report = OpSTReport()
        op_st = OpSTCase("AddN", {"calc_expect_func_file_func": 1})
        op_st_case_trace = OpSTCaseTrace(op_st)
        op_st_report = OpSTCaseReport(op_st_case_trace)
        report.report_list = [op_st_report]
        report._summary_txt()

    def test_compare_get_err_thr(self):
        """
        verify the abnormal scene of compare function in result_comparer.py
        """
        report = OpSTReport()
        run_dir = "xxx.txt"
        err_thr = [0.01, 0.01]
        error_report = 'false'
        comparer_obj = ResultCompare(report, run_dir, err_thr, error_report)
        case_info = CaseInfo([0.1,0.1])
        res = comparer_obj._get_err_thr(case_info)
        self.assertEqual(err_thr, res)

    def test_compare_get_err_thr_02(self):
        """
        verify the abnormal scene of compare function in result_comparer.py
        """
        report = OpSTReport()
        run_dir = "xxx.txt"
        err_thr = ""
        error_report = 'false'
        comparer_obj = ResultCompare(report, run_dir, err_thr, error_report)
        case_info = CaseInfo([0.1, 0.1])
        res = comparer_obj._get_err_thr(case_info)
        self.assertEqual([0.1, 0.1], res)

    def test_compare_get_err_thr_03(self):
        """
        verify the abnormal scene of compare function in result_comparer.py
        """
        report = OpSTReport()
        run_dir = "xxx.txt"
        err_thr = ""
        error_report = 'false'
        comparer_obj = ResultCompare(report, run_dir, err_thr, error_report)
        case_info = CaseInfo(None)
        res = comparer_obj._get_err_thr(case_info)
        self.assertEqual([0.01, 0.05], res)

    # -----------------------case_generator--------------------------
    def test_case_generator_1(self):
        """
        verify the normal scene of _get_default_attr_value function
        in case_generator.py
        """
        args = Args('./a.json', '', '')
        case_gen = MyCaseGenerator(args)
        case_gen.get_default_attr_value("float", '0.1', 'xxx')
        case_gen.get_default_attr_value("int", '1', 'xxx')
        case_gen.get_default_attr_value("bool", 'true', 'xxx')
        case_gen.get_default_attr_value("str", 'stride', 'xxx')
        case_gen.get_default_attr_value("list", '[1]', 'xxx')
        case_gen.get_default_attr_value("listListInt", '[[1]]', 'xxx')
        case_gen.get_default_attr_value("listInt", '[1]', 'xxx')
        case_gen.get_default_attr_value("listFloat", '[0.1]', 'xxx')
        case_gen.get_default_attr_value("listStr", '[\'x\']', 'xxx')
        case_gen.get_default_attr_value("listBool", '[\'true\']', 'xxx')

    # -----------------------data_generator--------------------------
    def test_gen_data_1(self):
        """
        verify the normal scene of gen_data function
        in data_generator.py
        """
        report = OpSTReport()
        with pytest.raises(utils.OpTestGenException) as error:
            data_generator = DataGenerator([], '/home', True, report)

            data_generator.gen_data([1, 4], -10, 4, 'int32', 'xx')
            self.assertEqual(error.value.args[0],
                             ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)

    def test_gen_data_2(self):
        """
        verify the normal scene of gen_data function
        in data_generator.py
        """
        report = OpSTReport()
        data_generator = DataGenerator([], '/home', True, report)
        data_distribution = ['uniform', 'normal', 'beta', 'laplace',
                             'triangular', 'sigmoid', 'softmax', 'tanh']
        for distribution in data_distribution:
            data = data_generator.gen_data(
                [2, 4], -10, 400, 'float', distribution)
        self.assertEqual(2, len(data.shape))

    # ---------------------profiling_analysis-----------------------
    def test_profiling_analysis_1(self):
        """
        verify the normal scene of _get_op_case_result_and_show_data function
        in acl_op_runner.py
        """
        csv_file = current_file_path.parent / "golden" / "base_case" / "input" / "op_summary_0_1.csv"
        op_name_list = ["Cast", "Cast", "Cast", "Cast"]
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        runner._get_op_case_result_and_show_data(
            csv_file, op_name_list)

    def test_profiling_op_name_list_fail(self):
        """
        verify the normal scene of _get_op_case_result_and_show_data function
        in acl_op_runner.py
        """
        csv_file = current_file_path.parent / "golden" / "base_case" / "input" / "op_summary_0_1.csv"
        op_name_list = []
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        runner._prof_get_op_case_info_from_csv_file(
            csv_file, op_name_list)

    def test_profiling_csv_file_fail(self):
        """
        verify the normal scene of _get_op_case_result_and_show_data function
        in acl_op_runner.py
        """
        csv_file = current_file_path.parent / "golden" / "base_case" / "input" / "op_summary.csv"
        op_name_list = ["Cast", "Cast", "Cast", "Cast"]
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        runner._prof_get_op_case_info_from_csv_file(
            csv_file, op_name_list)

    def test_profiling_analysis_2(self):
        """
        verify the normal scene of _prof_get_op_name_from_report function
        in acl_op_runner.py
        """
        report = OpSTReport()
        op_st = OpSTCase("AddN", {"calc_expect_func_file_func": 1})
        op_st_case_trace = OpSTCaseTrace(op_st)
        op_st_report = OpSTCaseReport(op_st_case_trace)
        with mock.patch(
                'msopst.st.interface.st_report.'
                'OpSTReport.get_case_report', return_value=op_st_report):
            runner = AclOpRunner('/home', 'ddd', report)
            run_result_list = ["1  Test_AddN_001_case_001  [pass]"]
            runner._prof_get_op_name_from_report(run_result_list)

    def test_profiling_show_data(self):
        each_case_info_list = ['Cast', 'AI_CPU', '1338.541672']
        op_case_info_list = []
        for i in range(30):
            op_case_info_list.append(each_case_info_list)
        acl_op_runner.display_op_case_info(op_case_info_list)

    def test_prof_analyze(self):
        out_path = "./test_msopst/st/golden/base_case/input"
        lines = "1  Test_AddN_001_case_001  [pass] \n " \
                "2  Test_AddN_001_case_002  [pass] \n " \
                "3  Test_AddN_001_case_003  [pass] \n"
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        with mock.patch(
                'msopst.st.interface.utils.ScanFile.scan_subdirs',
                return_value=['result.txt']):
            with mock.patch(
                    'msopst.st.interface.utils.read_file',
                    return_value=lines):
                with mock.patch('os.path.join', return_value=out_path), \
                     mock.patch('os.path.exists', return_value=True), \
                     mock.patch('os.access', return_value=True), \
                     mock.patch('os.chdir'):
                    with mock.patch('msopst.st.interface.utils.execute_command'):
                        runner.prof_analyze(os.path.join(out_path, ConstManager.PROF))

    def test_prof_run_no_install_path(self):
        out_path = "./test_msopst/st/golden/base_case/input"
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        runner.prof_run(out_path, '', '')

    def test_prof_run(self):
        out_path = "./test_msopst/st/golden/base_case/input"
        lines = "1  Test_AddN_001_case_001  [pass] \n " \
                "2  Test_AddN_001_case_002  [pass] \n " \
                "3  Test_AddN_001_case_003  [pass] \n"
        report = OpSTReport()
        runner = AclOpRunner('/home', 'ddd', report)
        with mock.patch('os.getenv', return_value="/home/test/Ascend"):
            with mock.patch(
                    'msopst.st.interface.utils.ScanFile.scan_subdirs',
                    return_value=['result.txt']):
                with mock.patch(
                        'msopst.st.interface.utils.read_file',
                        return_value=lines):
                    with mock.patch('os.path.join', return_value=out_path), \
                         mock.patch('os.path.exists', return_value=True), \
                         mock.patch('os.access', return_value=True), \
                         mock.patch('os.chdir'):
                        with mock.patch(
                                'msopst.st.interface.utils.execute_command'):
                            runner.prof_run(out_path, '', '')

    def test_scan_subdirs(self):
        prof_base_path = '/home/test'
        scan = utils.ScanFile(prof_base_path, first_prefix="PROF",
                              second_prefix="device")
        with mock.patch('os.path.exists', return_value=True):
            with mock.patch('os.path.isdir', return_value=True):
                with mock.patch('os.path.split', return_value=["PROF_A", "device_0"]):
                    with mock.patch('os.listdir',
                                    return_value=["PROF_A/device_0"]):
                        scan.scan_subdirs()

    def test_st_report_save(self):
        """
        test_st_report_save
        """
        test_utils.clear_out_path(ST_OUTPUT)
        report = OpSTReport()
        report_data_path = os.path.join(ST_OUTPUT, 'st_report.json')
        with mock.patch(
                'msopst.st.interface.st_report.OpSTReport._to_json_obj',
                return_value=[{}]):
            report.save(report_data_path)
        with mock.patch(
                'msopst.st.interface.st_report.OpSTReport._to_json_obj',
                return_value=[{}]):
            report.save(report_data_path)

    @unittest.mock.patch('msopst.st.interface.case_generator.getattr')
    def test_create_cmd_for_mindspore(self, getattr_mock):
        """
        test create cmd for mindspore operator
        """
        test_utils.clear_out_path(ST_OUTPUT)
        op_info = {'op_name': 'Square',
                   'inputs': [{'index': 0, 'name': 'x', 'need_compile': False,
                               'param_type': 'required', 'shape': 'all'}],
                   'outputs': [{'index': 0, 'name': 'y',
                                'need_compile': False,
                                'param_type': 'required',
                                'shape': 'all'}],
                   'attr': [],
                   'fusion_type': 'OPAQUE',
                   'dtype_format': [(('float32', 'DefaultFormat'),
                                     ('float32', 'DefaultFormat'))],
                   'imply_type': 'TBE', 'async_flag': False,
                   'binfile_name': 'square.so', 'compute_cost': 10,
                   'kernel_name': 'square_impl', 'partial_flag': 'True',
                   'reshape_type': '', 'dynamic_format': False,
                   'dynamic_shape': False, 'op_pattern': ''}
        getattr_mock.return_value = op_info
        lines = ''
        args = ['aaa.py', 'create', '-i', 'op_impl.py', '-out', ST_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                with mock.patch('msopst.st.interface.utils'
                                '.check_path_valid'):
                    with mock.patch('builtins.open', mock.mock_open(
                            read_data=lines)):
                        with mock.patch('msopst.st.interface'
                                        '.case_generator'
                                        '.importlib.import_module'):
                            with mock.patch('msopst.st.interface.arg_parser.'
                                'MsopstArgParser._check_path_permission_valid', 
                                return_value=None):
                                msopst.main()

        self.assertTrue(test_utils.check_file_context(
            ST_OUTPUT, ST_MS_GOLDEN_JSON_OUTPUT))

    def test_ms_op_generator(self):
        """
        test _create_ms_op_json_content function of ms_op_generator.py
        """
        data = [{"case_name": "Test_Add_001",
                 "op": "Add",
                 "st_mode": 'ms_python_train',
                 "calc_expect_func_file": "/home/aa.py"
                                          ":calc_expect_func",
                 "input_desc": [
                     {
                         "format": ["NC1HWC0"],
                         "ori_format": ["NCHW"],
                         "type": "float16",
                         "shape": [8, 1, 16, 4, 16],
                         "ori_shape": [8, 1, 16, 4, 16],
                         "data_distribute": ["uniform"],
                         "value_range": [[0.1, 1.0]]
                     }],
                 "output_desc": [
                     {
                         "format": ["NC1HWC0"],
                         "ori_format": ["NCHW"],
                         "type": "float16",
                         "shape": [8, 1, 16, 4, 16],
                         "ori_shape": [8, 16, 16, 4]
                     }]
                 }]
        ms_op_generator._create_ms_op_json_content(data)

    @staticmethod
    def mock_gen_data(cls, *args, **kwargs):
        """mock tofile"""
        return NumpyArrar()

    def test_abnormal_case(self):
        """
        test abnormal case with input json
        """
        test_utils.clear_out_path(ST_OUTPUT)
        args = ['msopst', 'run', '-i', ST_GOLDEN_ABNORMAL_CASE_JSON_INPUT, '-soc',
                'Ascend310', '-out', ST_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                with mock.patch(
                        'msopst.st.interface.utils.execute_command'):
                    msopst.main()

    def test_interrupt_process_when_atc_failed(self):
        """
        test interrupt process when running atc cmd failed and the st case is expected success in default
        """
        test_utils.clear_out_path(ST_OUTPUT)
        args = ['msopst', 'run', '-i', ST_GOLDEN_ATC_FAILED_JSON_INPUT, '-soc',
                'Ascend310', '-out', ST_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopst.main()
        self.assertRaises(utils.OpTestGenException, utils.check_path_exists, '', ConstManager.ATC_TRANSFORM_ERROR)

    def test_check_list_float(self):
        err_thr = utils.check_list_float([0.1, 0.1], "err_thr")
        self.assertEqual(err_thr,[0.1, 0.1])

    def test_check_list_float_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            utils.check_list_float(["A"], "err_thr")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_ERROR_THRESHOLD_ERROR)

    def test_clas_report_json_encoder(self):
        value1 = np.int8(1)
        value2 = np.float16(1.0)
        value4 = np.zeros(5)
        json_obj ={"value1": [value1],
                   "value2": [value2],
                   "value3": [(1.000000066 + 0j)],
                   "value4": [value4]
                   }
        json.dumps(json_obj, indent=4, cls=ReportJsonEncoder)

    def test_msopst_write_content_to_file_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch('os.fdopen', side_effect=OSError):
                AtcTransformOm._write_content_to_file("content", "/home")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)

    def test_msopst_write_json_file1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch('os.fdopen', side_effect=IOError):
                utils.write_json_file('/home/result', "test")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)

    def test_get_compare_stage_result(self):
        """
        verify the abnormal scene of compare function in result_comparer.py
        """
        report_path = os.path.realpath(ST_REPORT)
        report = OpSTReport()
        report.load(report_path)
        run_dir = ""
        err_thr = [0.01, 0.01]
        error_report = 'false'
        op_st = OpSTCase("AddN", {"calc_expect_func_file_func": 1})
        op_st_case_trace = OpSTCaseTrace(op_st)
        op_st_report = OpSTCaseReport(op_st_case_trace)
        result = "[pass]"
        case_name = 'AddN'
        with mock.patch('os.path.join', return_value=ST_GOLDEN_OP_RESULT_TXT):
            comparer_obj = ResultCompare(report, run_dir, err_thr,
                                         error_report)
            comparer_obj.compare()
            comparer_obj._get_run_stage_result(result, case_name, op_st_report)

    def test_display_output(self):
        diff_thd = [0.01, 0.05]
        value1 = np.int8(1)
        value2 = np.float16(1.0)
        with mock.patch('msopst.st.interface.compare_data.CompareData._display_data_by_index'):
            compare_data_obj = CompareData('current case', diff_thd, 'false', '')
            compare_data_obj.compare(value1, value2)
            compare_data_obj._display_output(0, 30, 0.01)

    def test_write_err_report(self):
        test_utils.clear_out_path(ST_OUTPUT)
        compare_data = CompareData({}, [0.01, 0.05], "true", ST_OUTPUT)
        data = [1, 2, 3, 4, 5]
        compare_data._write_err_report(ST_OUTPUT, data)

    def test_ms_op_runner_execute_command(self):
        """
        test ms op runner api
        """
        run_cmd = ['python3', '-m', 'pytest', '-s', "Add3_test.py"]
        path = "/home/xxx/out"
        op_name = "Add3"
        soc_version = "Ascend910"
        report = OpSTReport("cmd")
        ms_op_runner = MyMsOpRunner(path, op_name, soc_version, report)
        try:
            ms_op_runner.execute_command(run_cmd)
        except Exception as exception:
            self.assertIsInstance(exception, utils.OpTestGenException)

    def test_check_name_valid(self):
        name = "zn&#" * 256
        with pytest.raises(utils.OpTestGenException) as error:
            utils.check_name_valid(name)
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)

    def test_check_file_size(self):
        with mock.patch('os.path.getsize', return_value=100*1024*1024):
            utils.check_file_size("/test")

        with mock.patch('os.path.getsize', return_value=200*1024*1024):
            with pytest.raises(utils.OpTestGenException) as error:
                utils.check_file_size("/test")
            self.assertEqual(error.value.args[0],
                             ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)
                             
        with pytest.raises(utils.OpTestGenException) as error:
            utils.check_file_size("/test")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)

    def test_check_atc_args_valid(self):
        atc_args1 = "--log=log " * 256
        with pytest.raises(utils.OpTestGenException) as error:
            AdvanceIniParser._check_atc_args_valid(atc_args1)
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)
        atc_args2 = "--log=log^&"
        with pytest.raises(utils.OpTestGenException) as error:
            AdvanceIniParser._check_atc_args_valid(atc_args2)
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)

    def test_init_tool_chain(self):
        tool_chain_str = "TOOL_CHAIN = \"/test1/bin/gcc\""
        test_utils.clear_out_path(ST_OUTPUT)
        tool_chain_msopst_ini = os.path.join(ST_OUTPUT, 'msopst.ini')
        with os.fdopen(os.open(tool_chain_msopst_ini, WRITE_FLAGS, WRITE_MODES), 'w') as fout:
            fout.write(tool_chain_str)
        with pytest.raises(utils.OpTestGenException) as error:
            get_advance_args = AdvanceIniParser(tool_chain_msopst_ini)
            get_advance_args.get_advance_args_option()
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)

    def test_st_torch_api(self):
        """
        run st: torch api
        """
        test_utils.clear_out_path(ST_OUTPUT)
        self.gen_data_ = DataGenerator.gen_data
        DataGenerator.gen_data = staticmethod(self.mock_gen_data)
        args = ['msopst', 'run', '-i', ST_PT_GOLDEN_INPUT_JSON, '-soc',
                'Ascend910', '-out', ST_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                with mock.patch(
                        'msopst.st.interface.utils.execute_command'):
                    msopst.main()
        DataGenerator.gen_data = self.gen_data_

    def test_run_torch_st_with_profiling(self):
        """
        run st: torch api
        """
        with mock.patch('os.getenv', return_value="/home"):
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch(
                        'msopst.st.interface.utils.execute_command'):
                    with mock.patch(
                            'msopst.st.interface.utils'
                            '.check_path_valid'):
                        with mock.patch('os.path.exists',
                                        return_value=True), mock.patch('os.chdir'):
                            report = OpSTReport()
                            advance = AdvanceIniParser(MSOPST_CONF_INI)
                            runner = AclOpRunner('/home', 'ddd', report, advance)
                            runner.run_torch_api('Add')

    def test_get_pta_and_pro_path(self):
        """
        run st: get_pta_and_pro_path
        """
        report = OpSTReport()
        advance = AdvanceIniParser(MSOPST_CONF_INI)
        runner = AclOpRunner('/home', 'ddd', report, advance)
        pta_path, prof_path = runner._get_pta_and_prof_path(ST_GOLDEN_TORCH_API_OUTPUT)
        self.assertTrue(prof_path != "")

    def test_run_msprof_py(self):
        """
        run st: torch api
        """
        with mock.patch('os.getenv', return_value="/home"):
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch(
                        'msopst.st.interface.acl_op_runner.AclOpRunner._get_pta_and_prof_path',
                        return_value=('/home', '/ddd')):
                    with mock.patch(
                            'msopst.st.interface.acl_op_runner.AclOpRunner._get_job_path', return_value='/aaa'):
                        with mock.patch(
                                'msopst.st.interface.utils.execute_command'):
                            with mock.patch(
                                    'msopst.st.interface.utils'
                                    '.check_path_valid'):
                                with mock.patch('os.path.exists',
                                                return_value=True), mock.patch('os.chdir'):
                                    report = OpSTReport()
                                    advance = AdvanceIniParser(MSOPST_CONF_INI)
                                    runner = AclOpRunner('/home', 'ddd', report, advance)
                                    runner.run_msprof_py('/home', 'ddd', '/aaa')

    def test_check_required_key_valid(self):
        """
        run st: torch api
        """
        test_utils.clear_out_path(ST_OUTPUT)
        json_obj1 = {"st_mode": 'aaa'}
        with pytest.raises(utils.OpTestGenException) as error:
            utils.check_required_key_valid(json_obj1,
                                                 ConstManager.REQUIRED_KEYS,
                                                 'case', '/home')
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_PARSE_JSON_FILE_ERROR)
        json_obj2 = {"run_torch_api": 'torch.aaa'}
        with pytest.raises(utils.OpTestGenException) as error:
            utils.check_required_key_valid(json_obj2,
                                                 ConstManager.REQUIRED_KEYS,
                                                 'case', '/home')
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_PARSE_JSON_FILE_ERROR)

    def test_execute_atc_cmd1(self):
        os.environ[ConstManager.ASCEND_CUSTOM_OPP_PATH] = '/home/test/sp!'
        report = OpSTReport()
        CASE_LIST = [{'op': 'Op'}]
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch(
                    'msopst.st.interface.utils.execute_command'):
                with mock.patch(
                        'msopst.st.interface.utils.check_path_valid'):
                    with mock.patch('os.makedirs', return_value=True):
                        atc_transform = AtcTransformOm(CASE_LIST, '/home',
                                                       None, False, report)
                        atc_transform._execute_atc_cmd("atc", "cd aaa")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_INVALID_PARAM_ERROR)
        os.environ[ConstManager.ASCEND_CUSTOM_OPP_PATH] = ''

    def test_execute_atc_cmd2(self):
        os.environ[ConstManager.ASCEND_CUSTOM_OPP_PATH] = '/home/test/sp'
        report = OpSTReport()
        CASE_LIST = [{'op': 'Op'}]
        with mock.patch('msopst.st.interface.utils.execute_command'):
            with mock.patch(
                    'msopst.st.interface.utils.check_path_valid'):
                with mock.patch('os.makedirs', return_value=True):
                    atc_transform = AtcTransformOm(CASE_LIST, '/home', None,
                                                   False, report)
                    atc_transform._execute_atc_cmd("atc", "cd aaa")
        os.environ[ConstManager.ASCEND_CUSTOM_OPP_PATH] = ''

    def test_gen_ascendc_test_code(self):
        test_utils.clear_out_path(ST_OUTPUT)
        args = ['msopst', 'ascendc_test', '-i', ASCENDC_ST_CASE_JSON,
                '-kernel', ASCENDC_KERNEL_CPP_FILE, '-out', ST_OUTPUT]
        with pytest.raises(SystemExit):
            with mock.patch('sys.argv', args):
                msopst.main()


    def test_get_np_type(self):
        result = utils.get_np_type("bfloat16")
        import tensorflow
        self.assertEqual(result, tensorflow.bfloat16.as_numpy_dtype)

if __name__ == '__main__':
    unittest.main()
