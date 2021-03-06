# Copyright 2020 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Module for registering DPUCZDX8G zcu104 target """

import os
import pyxir
import logging

from pyxir.graph.transformers import subgraph

from .common import xgraph_dpu_optimizer, xgraph_dpu_quantizer
from .vai_c import VAICompiler

logger = logging.getLogger('pyxir')


def xgraph_dpu_zcu104_build_func(xgraph, work_dir=os.getcwd(), **kwargs):

    # TODO here or in optimizer, both?
    # DPU layers are in NHWC format because of the tensorflow
    #   intemediate structure we use to communicate with
    #   DECENT/DNNC

    return subgraph.xgraph_build_func(
        xgraph=xgraph,
        target='DPUCZDX8G-zcu104',
        xtype='DPU',
        layout='NHWC',
        work_dir=work_dir
    )


def xgraph_dpu_zcu104_compiler(xgraph, **kwargs):

    meta = {
        "lib": "/usr/local/lib/libn2cube.so",
        # "vitis_dpu_kernel": "tf_resnet50_0",
        "pre_processing_pool": 4,
        "post_processing_pool": 4,
        "dpu_thread_pool": 3,
        "dpu_task_pool": 16
    }

    # Vitis-AI 1.1
    old_arch = "/opt/vitis_ai/compiler/arch/dpuv2/ZCU104/ZCU104.json"
    # Vitis-AI 1.2 - ...
    new_arch = "/opt/vitis_ai/compiler/arch/DPUCZDX8G/ZCU104/arch.json"

    if os.path.exists(new_arch):
        arch = new_arch
    else:
        arch = old_arch

    compiler = VAICompiler(xgraph, arch=arch, meta=meta, **kwargs)
    c_xgraph = compiler.compile()

    return c_xgraph


pyxir.register_target('DPUCZDX8G-zcu104',
                      xgraph_dpu_optimizer,
                      xgraph_dpu_quantizer,
                      xgraph_dpu_zcu104_compiler,
                      xgraph_dpu_zcu104_build_func)