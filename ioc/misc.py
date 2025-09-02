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


"""
    The default yaml loader does not respect the ordering key while loading a dictionay.
    This can lead to error while ordering is defining key by key

    reference: https://gist.github.com/enaeseth/844388

"""

from typing import Any, Iterator, Optional, Union
import yaml
import yaml.constructor

from collections import OrderedDict

def deepcopy(value: Any) -> Any:
    """
    The default copy.deepcopy seems to copy all objects and some are not
    `copy-able`.

    We only need to make sure the provided data is a copy per key, object does
    not need to be copied.
    """

    if not isinstance(value, (dict, list, tuple)):
        return value

    if isinstance(value, dict):
        copy = {}
        for k, v in value.items():
            copy[k] = deepcopy(v)
        return copy
            
    if isinstance(value, tuple):
        copy = list(range(len(value)))

        for k in get_keys(list(value)):
            copy[k] = deepcopy(value[k])

        return tuple(copy)

    if isinstance(value, list):
        copy = list(range(len(value)))

        for k in get_keys(value):
            copy[k] = deepcopy(value[k])

        return copy

    return value

def is_string(value: Any) -> bool:
    return isinstance(value, (str))

def is_iterable(value: Any) -> bool:
    return isinstance(value, (dict, list))

def get_keys(arguments: Union[list[Any], dict[str, Any]]) -> Union[range, Any, list[Any]]:
    if isinstance(arguments, (list)):
        return range(len(arguments))

    if isinstance(arguments, (dict)):
        return arguments.keys()

    return []

class Dict(object):
    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        self.data = data or {}

    def get(self, name: str, default: Optional[Any] = None) -> Any:
        data = self.data
        for name in name.split("."):
            if name in data:
                data = data[name]
            else:
                return default

        return data

    def get_dict(self, name: str, default: Optional[dict[str, Any]] = None) -> 'Dict':
        default = default or {}
        value = self.get(name, default)

        if not isinstance(value, Dict):
            value = Dict(value)

        return value

    def get_int(self, name: str, default: Optional[int] = None) -> int:
        return int(self.get(name, default))

    def get_all(self, name: str, default: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return self.get_dict(name, default).all()

    def all(self) -> dict[str, Any]:
        def walk(data: Any) -> Any:
            all = {}

            if not isinstance(data, dict):
                return data

            for v, d in data.items():
                if isinstance(d, Dict):
                    all[v] = d.all()
                else:
                    all[v] = d

                if is_iterable(all[v]):
                    walk(all[v])

            return all

        return walk(self.data)

    def iteritems(self) -> Iterator[Any]:
        return self.data.items()

    def __iter__(self) -> Iterator[Any]:
        return iter(self.data)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor('tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor('tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node: Any) -> Any:
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node: Any, deep: bool = False) -> OrderedDict:
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                                                    'expected a mapping node, but found %s' % node.id,
                                                    node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            # key = self.construct_object(key_node, deep=deep)

            key = key_node.value
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                                                        node.start_mark,
                                                        'found unacceptable key (%s)' % exc,
                                                        key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping
