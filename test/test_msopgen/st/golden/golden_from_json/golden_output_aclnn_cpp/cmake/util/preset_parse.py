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

import json
import sys
import os


def read_json(file):
    with open(file, 'r') as fd:
        config = json.load(fd)
    return config


def get_config_opts(file):
    config = read_json(file) 

    src_dir = os.path.abspath(os.path.dirname(file))
    opts = ''

    for conf in config:
        if conf == 'configurePresets':
            for node in config[conf]:
                macros = node.get('cacheVariables')
                if macros is not None:
                    for key in macros:
                        opts += '-D{}={} '.format(key, macros[key]['value'])

    opts = opts.replace('${sourceDir}', src_dir)
    print(opts)


if __name__ == "__main__":
    get_config_opts(sys.argv[1])
