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

"""
Module for testing the relay pyxir frontend


"""

import warnings
import unittest
import numpy as np

try:
    # ! To import tvm
    import pyxir.frontend.tvm

    import tvm
    from tvm import relay
    from tvm.relay import testing

    from pyxir.frontend.tvm import relay as xf_relay

    skip = False
except Exception as e:
    skip = True


class TestRelayL10TemporaryOperationConversions(unittest.TestCase):

    @unittest.skipIf(skip, "Could not import TVM and/or TVM frontend")
    def test_nn_adaptive_avg_pool2d_1(self):
        warnings.filterwarnings("ignore")
        data = relay.var(
            "data",
            relay.TensorType((-1, 4, 5, 5), "float32")
        )

        net = relay.nn.adaptive_avg_pool2d(
            data, output_size=(3, 3), layout='NCHW')

        net = relay.Function(relay.analysis.free_vars(net), net)

        mod, params = testing.create_workload(net)

        xgraph = xf_relay.from_relay(mod, params)

        layers = xgraph.get_layers()

        assert layers[0].type[0] == 'Input'
        assert layers[1].type[0] == 'Pooling'
        assert layers[1].shapes.tolist() == [-1, 4, 3, 3]
        assert layers[1].attrs['padding'] == [[0, 0], [0, 0], [0, 0], [0, 0]]
        assert layers[1].attrs['insize'] == [5, 5]
        assert layers[1].attrs['outsize'] == [3, 3]
        assert layers[1].attrs['data_layout'] == 'NCHW'
        assert layers[1].attrs['strides'] == [1, 1]
        assert layers[1].attrs['kernel_size'] == [3, 3]
        assert layers[1].attrs['pool_type'] == 'Avg'

    @unittest.skipIf(skip, "Could not import TVM and/or TVM frontend")
    def test_nn_adaptive_avg_pool2d_2(self):
        warnings.filterwarnings("ignore")
        data = relay.var(
            "data",
            relay.TensorType((-1, 4, 6, 6), "float32")
        )

        net = relay.nn.adaptive_avg_pool2d(
            data, output_size=(3, 3), layout='NCHW')

        net = relay.Function(relay.analysis.free_vars(net), net)

        mod, params = testing.create_workload(net)

        xgraph = xf_relay.from_relay(mod, params)

        layers = xgraph.get_layers()

        assert layers[0].type[0] == 'Input'
        assert layers[1].type[0] == 'Pooling'
        assert layers[1].shapes.tolist() == [-1, 4, 3, 3]
        assert layers[1].attrs['padding'] == [[0, 0], [0, 0], [0, 0], [0, 0]]
        assert layers[1].attrs['insize'] == [6, 6]
        assert layers[1].attrs['outsize'] == [3, 3]
        assert layers[1].attrs['data_layout'] == 'NCHW'
        assert layers[1].attrs['strides'] == [2, 2]
        assert layers[1].attrs['kernel_size'] == [2, 2]
        assert layers[1].attrs['pool_type'] == 'Avg'

    @unittest.skipIf(skip, "Could not import TVM and/or TVM frontend")
    def test_nn_adaptive_avg_pool2d_3(self):
        warnings.filterwarnings("ignore")
        data = relay.var(
            "data",
            relay.TensorType((-1, 6, 6, 4), "float32")
        )

        net = relay.nn.adaptive_avg_pool2d(
            data, output_size=(6, 6), layout='NHWC')

        net = relay.Function(relay.analysis.free_vars(net), net)

        mod, params = testing.create_workload(net)

        xgraph = xf_relay.from_relay(mod, params)

        layers = xgraph.get_layers()

        assert layers[0].type[0] == 'Input'
        assert layers[1].type[0] == 'Pooling'
        assert layers[1].shapes.tolist() == [-1, 6, 6, 4]
        assert layers[1].attrs['padding'] == [[0, 0], [0, 0], [0, 0], [0, 0]]
        assert layers[1].attrs['insize'] == [6, 6]
        assert layers[1].attrs['outsize'] == [6, 6]
        assert layers[1].attrs['data_layout'] == 'NHWC'
        assert layers[1].attrs['strides'] == [1, 1]
        assert layers[1].attrs['kernel_size'] == [1, 1]
        assert layers[1].attrs['pool_type'] == 'Avg'

    @unittest.skipIf(skip, "Could not import TVM and/or TVM frontend")
    def test_nn_adaptive_avg_pool2d_4(self):
        warnings.filterwarnings("ignore")
        data = relay.var(
            "data",
            relay.TensorType((-1, 5, 5, 4), "float32")
        )

        net = relay.nn.adaptive_avg_pool2d(
            data, output_size=(1, 1), layout='NHWC')

        net = relay.Function(relay.analysis.free_vars(net), net)

        mod, params = testing.create_workload(net)

        xgraph = xf_relay.from_relay(mod, params)

        layers = xgraph.get_layers()

        assert layers[0].type[0] == 'Input'
        assert layers[1].type[0] == 'Pooling'
        assert layers[1].shapes.tolist() == [-1, 1, 1, 4]
        assert layers[1].attrs['padding'] == [[0, 0], [0, 0], [0, 0], [0, 0]]
        assert layers[1].attrs['insize'] == [5, 5]
        assert layers[1].attrs['outsize'] == [1, 1]
        assert layers[1].attrs['data_layout'] == 'NHWC'
        assert layers[1].attrs['strides'] == [5, 5]
        assert layers[1].attrs['kernel_size'] == [5, 5]
        assert layers[1].attrs['pool_type'] == 'Avg'
