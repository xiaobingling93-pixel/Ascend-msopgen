import unittest
from collections import OrderedDict
from collections import namedtuple
import pytest
from unittest import mock
from msopgen.interface.op_file_aicore import OpFileAiCore


class OpInfo:
    def __init__(self, parsed_info_input, parsed_info_output, fix_op_type_in):
        self.parsed_input_info = parsed_info_input
        self.parsed_output_info = parsed_info_output
        self.fix_op_type = fix_op_type_in


class TestOpFileAiCoreMethods(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super(TestOpFileAiCoreMethods, self).__init__(method_name)
        self.op_info = OpInfo('', '', '')
        self.output_path = ''

    def test_generate_input_output_info_cfg(self):
        op_file = OpFileAiCore

        parsed_info = OrderedDict([('x', {
            'ir_type_list': ['DT_FLOAT', ' DT_INT32'],
            'param_type': 'required', 'format_list': ['NCHW']})])
        str_template = "input{index}.name={name}\ninput{index}.dtype={dtype}\ninput{index}.paramType={paramType}\ninput{index}.format={format}"
        self._mapping_info_cfg_type = mock.Mock(return_value="int8")
        ret = op_file._generate_input_output_info_cfg(self, parsed_info, str_template)
        print(ret)
        op_file._generate_cpp_impl(self)
        golden_ret = "input0.name=x\ninput0.dtype=int8,int8\ninput0.paramType=required\ninput0.format=NCHW,NCHW"
        self.assertEqual(golden_ret, ret)
        OpInfo = namedtuple('OpInfo', ['parsed_input_info'])
        value = {
            "param_type" : "optional",
            "ir_type_list" : ["DT_FLOAT"],
            "format_list" : ["ND"]
        }
        dict_value = {"a" : value}
        op_info_tmp = OpInfo(parsed_input_info = dict_value)
        self.op_info = op_info_tmp
        ret = op_file._generate_cpp_params(self, False)

if __name__ == '__main__':
    unittest.main()
