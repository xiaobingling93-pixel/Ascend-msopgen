#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
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

import sys
import os
import opdesc_parser

PYF_PATH = os.path.dirname(os.path.realpath(__file__))


class OpInfo:
    def __init__(self: any, op_type: str, cfg_file: str):
        op_descs = opdesc_parser.get_op_desc(
            cfg_file, [], [], opdesc_parser.OpDesc, [op_type]
        )
        if op_descs is None or len(op_descs) != 1:
            raise RuntimeError("cannot get op info of {}".format(op_type))
        self.op_desc = op_descs[0]

    def get_op_file(self: any):
        return self.op_desc.op_file

    def get_op_intf(self: any):
        return self.op_desc.op_intf

    def get_inputs_name(self: any):
        return self.op_desc.input_ori_name

    def get_outputs_name(self: any):
        return self.op_desc.output_ori_name


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        raise RuntimeError("arguments must greater than 2")
    op_info = OpInfo(sys.argv[1], sys.argv[2])
    print(op_info.get_op_file())
    print(op_info.get_op_intf())
    print(op_info.get_inputs_name())
    print(op_info.get_outputs_name())