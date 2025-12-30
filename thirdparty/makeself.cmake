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

include(ExternalProject)

set(MAKESLF_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../op_project_templates/op_project_tmpl/cmake/util/makeself)

ExternalProject_Add(makeself_third
  URL               ${_makeself_url}
                    https://ascend-cann.obs.cn-north-4.myhuaweicloud.com/makeself/release-2.4.2.zip
  PREFIX            ${MAKESLF_PATH}
  CONFIGURE_COMMAND ""
  BUILD_COMMAND     ""
  INSTALL_COMMAND   ""
)

ExternalProject_Get_Property(makeself_third SOURCE_DIR)
ExternalProject_Get_Property(makeself_third BINARY_DIR)

add_custom_target(makeself_code ALL DEPENDS makeself_third
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/COPYING ${MAKESLF_PATH}
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/makeself.1 ${MAKESLF_PATH}
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/makeself.lsm ${MAKESLF_PATH}
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/*.sh ${MAKESLF_PATH}
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/README.md ${MAKESLF_PATH}
                 COMMAND cp ${MAKESLF_PATH}/src/makeself_third/VERSION ${MAKESLF_PATH}
                 COMMAND rm -rf ${MAKESLF_PATH}/src
                 COMMAND rm -rf ${MAKESLF_PATH}/tmp)