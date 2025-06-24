#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


# Import the build function directly
from ioc.helper import build

# Make helper and misc modules available
# def __getattr__(name):
#     if name == 'helper':
#         from ioc import helper
#         return helper
#     elif name == 'misc':
#         from ioc import misc  
#         return misc
#     raise AttributeError(f"module 'ioc' has no attribute '{name}'")
