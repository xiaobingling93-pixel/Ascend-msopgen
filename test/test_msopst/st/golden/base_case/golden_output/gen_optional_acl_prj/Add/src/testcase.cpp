/**
 * @file testcase.cpp
 *
 * -------------------------------------------------------------------------
 * This file is part of the MindStudio project.
 * Copyright (c) 2025 Huawei Technologies Co.,Ltd.
 *
 * MindStudio is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *          http://license.coscl.org.cn/MulanPSL2
 *
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 * -------------------------------------------------------------------------
 */

#include "op_test.h"
#include "op_execute.h"
using namespace OpTest;


OP_TEST(Add, Test_Add_001_case_001)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{4}, {4}};
    opTestDesc.inputDataType = {ACL_INT32, ACL_INT32};
    opTestDesc.inputFormat = {(aclFormat)1, (aclFormat)1};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_case_001_input_0", "test_data/data/Test_Add_001_case_001_input_1"};
    opTestDesc.inputConst = {false, false};
    // output parameter init
    opTestDesc.outputShape = {{4}};
    opTestDesc.outputDataType = {ACL_INT32};
    opTestDesc.outputFormat = {(aclFormat)1};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_case_001_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_case_001");

}

