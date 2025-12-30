/* -------------------------------------------------------------------------
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
 * ------------------------------------------------------------------------- */

#ifndef GE_OP_CONV2_D_TIK_H
#define GE_OP_CONV2_D_TIK_H
#include "graph/operator_reg.h"
namespace ge {

REG_OP(Conv2DTik)
    .INPUT(x1, TensorType({DT_FLOAT,DT_FLOAT16}))
    .INPUT(x2, TensorType({DT_FLOAT,DT_FLOAT16}))
    .OUTPUT(y, TensorType({DT_FLOAT,DT_FLOAT16}))
    .ATTR(strides, ListInt, [1,1,1,1])
    .ATTR(pads, ListInt, [1,1,1,1])
    .ATTR(dilations, ListInt, [1,1,1,1])
    .OP_END_FACTORY_REG(Conv2DTik)
}
#endif //GE_OP_CONV2_D_TIK_H
