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
aux_source_directory(./proto/caffe PROTO_SRCS)
list(APPEND SRCS ${PROTO_SRCS})

message(STATUS "SRCS = ${SRCS}")

if("x${SRCS}" STREQUAL "x")
    add_custom_target(${CAFFE_PLUGIN_TARGET}
            COMMAND mkdir -p ${CAFFE_PLUGIN_TARGET_OUT_DIR}
            COMMAND echo "no source to make lib${CAFFE_PLUGIN_TARGET}.so")
    return(0)
endif()

set(LIBRARY_OUTPUT_PATH ${CAFFE_PLUGIN_TARGET_OUT_DIR})

include_directories(./proto/caffe)
add_library(${CAFFE_PLUGIN_TARGET} SHARED ${SRCS})
