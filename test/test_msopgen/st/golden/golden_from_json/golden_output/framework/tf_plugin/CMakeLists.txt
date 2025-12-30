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
aux_source_directory(. SRCS)
message(STATUS "SRCS = ${SRCS}")

if("x${SRCS}" STREQUAL "x")
    add_custom_target(${TF_PLUGIN_TARGET}
            COMMAND mkdir -p ${TF_PLUGIN_TARGET_OUT_DIR}
            COMMAND echo "no source to make lib${TF_PLUGIN_TARGET}.so")
    return(0)
endif()

set(LIBRARY_OUTPUT_PATH ${TF_PLUGIN_TARGET_OUT_DIR})

add_library(${TF_PLUGIN_TARGET} SHARED ${SRCS})

target_compile_definitions(${TF_PLUGIN_TARGET} PRIVATE
    google=ascend_private
)

target_link_libraries(${TF_PLUGIN_TARGET} ${ASCEND_INC}/../lib64/libgraph.so)
