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

#ifndef GE_OP_BUCKETIZE_H
#define GE_OP_BUCKETIZE_H
#include "graph/operator_reg.h"
namespace ge {

REG_OP(Bucketize)
    .INPUT(input, TensorType({DT_INT32}))
    .OUTPUT(output, TensorType({DT_INT32}))
    .REQUIRED_ATTR(boundaries, ListFloat)
    .OP_END_FACTORY_REG(Bucketize)
}
#endif //GE_OP_BUCKETIZE_H