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

#ifndef GE_OP_CONV2_D_H
#define GE_OP_CONV2_D_H
#include "graph/operator_reg.h"
namespace ge {

REG_OP(Conv2D)
    .INPUT(x, TensorType({DT_FLOAT16,DT_FLOAT32}))
    .INPUT(filter, TensorType({DT_FLOAT16,DT_FLOAT32}))
    .OUTPUT(y, TensorType({DT_FLOAT16,DT_FLOAT32}))
    .ATTR(strides, ListInt, {1, 1, 1, 1})
    .ATTR(pads, ListInt, {1, 1, 1, 1})
    .REQUIRED_ATTR(dilations, ListInt)
    .OP_END_FACTORY_REG(Conv2D)
}
#endif //GE_OP_CONV2_D_H
