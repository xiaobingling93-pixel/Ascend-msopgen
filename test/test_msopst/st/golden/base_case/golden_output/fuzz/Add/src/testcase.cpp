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


OP_TEST(Add, Test_Add_001_fuzz_case_001_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_001_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_001_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_001_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_001_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_002_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_002_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_002_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_002_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_002_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_003_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_003_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_003_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_003_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_003_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_004_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_004_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_004_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_004_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_004_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_005_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_005_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_005_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_005_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_005_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_006_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_006_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_006_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_006_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_006_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_007_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_007_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_007_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_007_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_007_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_008_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_008_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_008_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_008_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_008_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_009_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_009_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_009_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_009_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_009_ND_float16");

}


OP_TEST(Add, Test_Add_001_fuzz_case_010_ND_float16)
{
    
    std::string opType = "Add";
    OpTestDesc opTestDesc(opType);
    // input parameter init
    opTestDesc.inputShape = {{1, 2}, {2}};
    opTestDesc.inputDataType = {ACL_FLOAT16, ACL_FLOAT16};
    opTestDesc.inputFormat = {(aclFormat)2, (aclFormat)2};
    opTestDesc.inputFilePath = {"test_data/data/Test_Add_001_fuzz_case_010_ND_float16_input_0", "test_data/data/Test_Add_001_fuzz_case_010_ND_float16_input_1"};
    opTestDesc.inputConst = {false, true};
    // output parameter init
    opTestDesc.outputShape = {{1, 2}};
    opTestDesc.outputDataType = {ACL_FLOAT16};
    opTestDesc.outputFormat = {(aclFormat)2};
    opTestDesc.outputFilePath = {"result_files/Test_Add_001_fuzz_case_010_ND_float16_output_0"};
    // attr parameter init
    
    // set deviceId
    const uint32_t deviceId = 0;
    EXPECT_EQ_AND_RECORD(true, OpExecute(opTestDesc, deviceId), opTestDesc, "Test_Add_001_fuzz_case_010_ND_float16");

}

