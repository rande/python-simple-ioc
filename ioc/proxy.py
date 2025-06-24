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

from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ioc.component import Container

class Proxy(object):
    __slots__ = ["_obj", "_container", "_id", "__weakref__"]

    def __init__(self, container: 'Container', id: str) -> None:
        object.__setattr__(self, "_obj", None)
        object.__setattr__(self, "_container", container)
        object.__setattr__(self, "_id", id)
        
    #
    # proxying (special cases)
    #
    def __getattribute__(self, name: str) -> Any:
        build_object(object, self)
        return getattr(object.__getattribute__(self, "_obj"), name)

    def __delattr__(self, name: str) -> None:
        build_object(object, self)
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name: str, value: Any) -> None:
        build_object(object, self)
        setattr(object.__getattribute__(self, "_obj"), name, value)
    
    def __nonzero__(self) -> bool:
        build_object(object, self)
        return bool(object.__getattribute__(self, "_obj"))

    def __str__(self) -> str:
        build_object(object, self)
        return "<Proxy " + str(object.__getattribute__(self, "_obj")) + ">"

    def __repr__(self) -> str:
        build_object(object, self)
        return repr(object.__getattribute__(self, "_obj"))

def build_object(object: type, instance: Proxy) -> None:
    if object.__getattribute__(instance, "_obj") is None:
        container = object.__getattribute__(instance, "_container")
        id = object.__getattribute__(instance, "_id")

        object.__setattr__(instance, "_obj", container.get(id))
