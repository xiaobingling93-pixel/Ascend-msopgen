#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created on Feb  28 20:56:45 2020
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

import os
import glob
import json
import argparse
import const_var


BINARY_INFO_CONFIG_JSON = "binary_info_config.json"


def load_json(json_file: str):
    with open(json_file, encoding="utf-8") as file:
        json_content = json.load(file)
    return json_content


def get_specified_suffix_file(root_dir, suffix):
    specified_suffix = os.path.join(root_dir, "**/*.{}".format(suffix))
    all_suffix_files = glob.glob(specified_suffix, recursive=True)
    return all_suffix_files


def add_simplified_config(op_type, key, core_type, objfile, config):
    simple_cfg = config.get(BINARY_INFO_CONFIG_JSON)
    op_cfg = simple_cfg.get(op_type)
    if not op_cfg:
        op_cfg = {}
        op_cfg['dynamicRankSupport'] = True
        op_cfg['simplifiedKeyMode'] = 0
        op_cfg['binaryList'] = []
        simple_cfg[op_type] = op_cfg
    bin_list = op_cfg.get('binaryList')
    bin_list.append({'coreType': core_type, 'simplifiedKey': key, 'binPath': objfile})


def add_op_config(op_file, bin_info, config):
    op_cfg = config.get(op_file)
    if not op_cfg:
        op_cfg = {'binList': []}
        config[op_file] = op_cfg
    op_cfg.get('binList').append(bin_info)


def gen_ops_config(json_file, soc, config):
    core_type_map = {
        'MIX': 0,
        'AiCore': 1,
        'VectorCore': 2,
        'MIX_AICORE': 3,
        'MIX_VECTOR_CORE': 4
    }
    contents = load_json(json_file)
    if ('binFileName' not in contents) or ('supportInfo' not in contents):
        return
    json_base_name = os.path.basename(json_file)
    op_dir = os.path.basename(os.path.dirname(json_file))
    support_info = contents.get('supportInfo')
    bin_name = contents.get('binFileName')
    bin_suffix = contents.get('binFileSuffix')
    core_type = core_type_map.get(contents.get("coreType"))
    bin_file_name = bin_name + bin_suffix
    op_type = bin_name.split('_')[0]
    op_file = op_dir + '.json'
    bin_info = {}
    keys = support_info.get('simplifiedKey')
    if keys:
        bin_info["simplifiedKey"] = keys


    bin_info['staticKey'] = support_info.get('staticKey')
    bin_info["int64Mode"] = support_info.get('int64Mode')
    bin_info['inputs'] = support_info.get('inputs')
    bin_info['outputs'] = support_info.get('outputs')
    if support_info.get('attrs'):
        bin_info['attrs'] = support_info.get('attrs')
    bin_info['binInfo'] = {'jsonFilePath': os.path.join(soc, op_dir, json_base_name)}
    add_op_config(op_file, bin_info, config)


def gen_all_config(root_dir, soc, out_dir, skip_binary_info_config):
    suffix = 'json'
    config = {BINARY_INFO_CONFIG_JSON: {}}
    all_json_files = get_specified_suffix_file(root_dir, suffix)

    for _json in all_json_files:
        gen_ops_config(_json, soc, config)
        file_path = soc + _json.split(soc)[1]
        with open(_json, "r+") as f:
            data = json.load(f)
            data["filePath"] = file_path
            f.seek(0)
            json.dump(data, f, indent=" ")
            f.truncate()

    for cfg_key in config.keys():
        if skip_binary_info_config and cfg_key == BINARY_INFO_CONFIG_JSON:
            continue
        cfg_file = os.path.join(out_dir, cfg_key)
        with os.fdopen(os.open(cfg_file, const_var.WFLAGS, const_var.WMODES), 'w') as fd:
            json.dump(config.get(cfg_key), fd, indent='  ')


# Parse multiple soc_versions ops in single path.
def gen_all_soc_config(all_path):
    soc_roots = glob.glob(os.path.join(all_path, "ascend*"))

    for soc_root in soc_roots:
        soc = os.path.basename(soc_root)
        gen_all_config(soc_root, soc, soc_root, True)
        cfg_files = glob.glob(os.path.join(soc_root, "*.json"))
        cfg_path = os.path.join(all_path, "config", soc)
        os.makedirs(cfg_path, exist_ok=True)
        for cfg_file in cfg_files:
            new_file = os.path.join(cfg_path, os.path.basename(cfg_file))
            os.rename(cfg_file, new_file)


def args_prase():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--path',
                        nargs='?',
                        required=True,
                        help='Parse the path of the json file.')

    parser.add_argument('-s',
                        '--soc',
                        nargs='?',
                        required=True,
                        help='Parse the soc_version of ops.')

    parser.add_argument('-o',
                        '--out',
                        nargs='?',
                        help='Output directory.')

    parser.add_argument('--skip-binary-info-config',
                        action='store_true',
                        help='binary_info_config.json file is not parsed.')

    return parser.parse_args()


def main():
    args = args_prase()
    if args.out is None:
        out_dir = args.path
    else:
        out_dir = args.out

    gen_all_config(args.path, args.soc, out_dir, args.skip_binary_info_config)


if __name__ == '__main__':
    main()