
/*
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
 * Description: api of Conv2D
 */

#ifndef _CONV2_D_KERNELS_H_
#define _CONV2_D_KERNELS_H_

#include "cpu_kernel.h"

namespace aicpu {
class Conv2DCpuKernel : public CpuKernel {
public:
    ~Conv2DCpuKernel() = default;
    virtual uint32_t Compute(CpuKernelContext &ctx) override;
};
} // namespace aicpu
#endif
