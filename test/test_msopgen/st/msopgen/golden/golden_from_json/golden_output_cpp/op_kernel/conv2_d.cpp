#include "kernel_operator.h"
#include "conv2_d_tiling.h"

extern "C" __global__ __aicore__ void conv2_d(GM_ADDR x, GM_ADDR filter, GM_ADDR y, GM_ADDR workspace, GM_ADDR tiling) {
    REGISTER_TILING_DEFAULT(Conv2DTilingData);
    GET_TILING_DATA(tilingData, tiling);
    // TODO: user kernel impl
}