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
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_COMPILER gcc)

# add source files
aux_source_directory(. SRCS)

if("x${SRCS}" STREQUAL "x")
    add_custom_target(${OP_PROTO_TARGET}
            COMMAND mkdir -p ${OP_PROTO_TARGET_OUT_DIR}
            COMMAND echo "no source to make lib${OP_PROTO_TARGET}.so")
    return(0)
endif()

set(LIBRARY_OUTPUT_PATH ${OP_PROTO_TARGET_OUT_DIR})

message( STATUS "OP_PROTO_TARGET=${OP_PROTO_TARGET}")
add_library(${OP_PROTO_TARGET} SHARED ${SRCS})

target_link_libraries(${OP_PROTO_TARGET} ${ASCEND_INC}/../lib64/libgraph.so)
