import unittest
import pytest
import numpy as np
from unittest import mock
from msopst.st.interface import utils
from msopst.st.interface.const_manager import ConstManager
from msopst.st.interface.data_generator import DataGenerator
from msopst.st.interface.st_report import OpSTReport


class TestUtilsMethods(unittest.TestCase):

    def test_msopst_generate1(self):
        report = OpSTReport()
        data_generator = DataGenerator([], '/home', True, report)
        distribution_list = ['normal', 'beta', 'laplace', 'triangular', 'relu',
                             'sigmoid', 'softmax', 'tanh']
        for i in distribution_list:
            data_generator.gen_data((64, 6), 1, 10, 'bool_', i)

    def test_msopst_generate_error(self):
        report = OpSTReport()
        with pytest.raises(utils.OpTestGenException) as error:
            data_generator = DataGenerator([], '/home', True, report)
            data_generator.gen_data((64, 6), 1, 10, 'bool_', 'error')
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)

    def test_gen_data_with_value_error1(self):
        report = OpSTReport()
        with pytest.raises(utils.OpTestGenException) as error:
            data_generator = DataGenerator([], '/home', True, report)
            data_generator.gen_data_with_value((64, 6), 
                                               './test_msopst/st/golden/base_case/input/test_value_add_input_1.bin',
                                               "float32")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)

    def test_gen_data_with_value_error2(self):
        report = OpSTReport()
        with pytest.raises(utils.OpTestGenException) as error:
            data_generator = DataGenerator([], '/home', True, report)
            data_generator.gen_data_with_value((64, 6), [1, 2, 3, 4], "float32")
        self.assertEqual(error.value.args[0],
                         ConstManager.OP_TEST_GEN_WRITE_FILE_ERROR)


if __name__ == '__main__':
    unittest.main()