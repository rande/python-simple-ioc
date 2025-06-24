#
# Copyright 2014-2025 Thomas Rabaix <thomas.rabaix@gmail.com>
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

class UnknownService(Exception):
    pass

class UnknownParameter(Exception):
    pass

class RecursiveParameterResolutionError(Exception):
    pass

class CyclicReference(Exception):
    pass
    
class LoadingError(Exception):
    pass

class DuplicateServiceDefinition(Exception):
    pass

class ParameterHolderIsFrozen(Exception):
    pass

class AbstractDefinitionInitialization(Exception):
    pass
