#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os.path
from abc import ABC

from robot.errors import DataError, TimeoutError
from robot.model import BodyItem
from robot.utils import (get_error_details, Importer, safe_str,
                         split_args_from_name_or_path, type_name)

from .loggerapi import LoggerApi
from .loggerhelper import IsLogged
from .logger import LOGGER


class Listeners(LoggerApi):
    _listeners: 'list[ListenerFacade]'

    def __init__(self, listeners=(), log_level='INFO'):
        self._is_logged = IsLogged(log_level)
        self._listeners = self._import_listeners(listeners)

    def _import_listeners(self, listeners, library=None) -> 'list[ListenerFacade]':
        imported = []
        for listener_source in listeners:
            try:
                listener = self._import_listener(listener_source, library)
            except DataError as err:
                name = listener_source \
                    if isinstance(listener_source, str) else type_name(listener_source)
                msg = f"Taking listener '{name}' into use failed: {err}"
                if library:
                    raise DataError(msg)
                LOGGER.error(msg)
            else:
                imported.append(listener)
        return imported

    def _import_listener(self, listener, library=None) -> 'ListenerFacade':
        if isinstance(listener, str):
            name, args = split_args_from_name_or_path(listener)
            importer = Importer('listener', logger=LOGGER)
            listener = importer.import_class_or_module(os.path.normpath(name),
                                                       instantiate_with_args=args)
        else:
            # Modules have `__name__`, with others better to use `type_name`.
            name = getattr(listener, '__name__', None) or type_name(listener)
        if self._get_version(listener) == 2:
            return ListenerV2Facade(listener, name, library)
        return ListenerV3Facade(listener, name, library)

    def _get_version(self, listener):
        version = getattr(listener, 'ROBOT_LISTENER_API_VERSION', 3)
        try:
            version = int(version)
            if version not in (2, 3):
                raise ValueError
        except (ValueError, TypeError):
            raise DataError(f"Unsupported API version '{version}'.")
        return version

    # Must be property to allow LibraryListeners to override it.
    @property
    def listeners(self):
        return self._listeners

    def start_suite(self, data, result):
        for listener in self.listeners:
            listener.start_suite(data, result)

    def end_suite(self, data, result):
        for listener in self.listeners:
            listener.end_suite(data, result)

    def start_test(self, data, result):
        for listener in self.listeners:
            listener.start_test(data, result)

    def end_test(self, data, result):
        for listener in self.listeners:
            listener.end_test(data, result)

    def start_keyword(self, data, result):
        for listener in self.listeners:
            listener.start_keyword(data, result)

    def end_keyword(self, data, result):
        for listener in self.listeners:
            listener.end_keyword(data, result)

    def start_user_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.start_user_keyword(data, implementation, result)

    def end_user_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.end_user_keyword(data, implementation, result)

    def start_library_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.start_library_keyword(data, implementation, result)

    def end_library_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.end_library_keyword(data, implementation, result)

    def start_invalid_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.start_invalid_keyword(data, implementation, result)

    def end_invalid_keyword(self, data, implementation, result):
        for listener in self.listeners:
            listener.end_invalid_keyword(data, implementation, result)

    def start_for(self, data, result):
        for listener in self.listeners:
            listener.start_for(data, result)

    def end_for(self, data, result):
        for listener in self.listeners:
            listener.end_for(data, result)

    def start_for_iteration(self, data, result):
        for listener in self.listeners:
            listener.start_for_iteration(data, result)

    def end_for_iteration(self, data, result):
        for listener in self.listeners:
            listener.end_for_iteration(data, result)

    def start_while(self, data, result):
        for listener in self.listeners:
            listener.start_while(data, result)

    def end_while(self, data, result):
        for listener in self.listeners:
            listener.end_while(data, result)

    def start_while_iteration(self, data, result):
        for listener in self.listeners:
            listener.start_while_iteration(data, result)

    def end_while_iteration(self, data, result):
        for listener in self.listeners:
            listener.end_while_iteration(data, result)

    def start_if(self, data, result):
        for listener in self.listeners:
            listener.start_if(data, result)

    def end_if(self, data, result):
        for listener in self.listeners:
            listener.end_if(data, result)

    def start_if_branch(self, data, result):
        for listener in self.listeners:
            listener.start_if_branch(data, result)

    def end_if_branch(self, data, result):
        for listener in self.listeners:
            listener.end_if_branch(data, result)

    def start_try(self, data, result):
        for listener in self.listeners:
            listener.start_try(data, result)

    def end_try(self, data, result):
        for listener in self.listeners:
            listener.end_try(data, result)

    def start_try_branch(self, data, result):
        for listener in self.listeners:
            listener.start_try_branch(data, result)

    def end_try_branch(self, data, result):
        for listener in self.listeners:
            listener.end_try_branch(data, result)

    def start_return(self, data, result):
        for listener in self.listeners:
            listener.start_return(data, result)

    def end_return(self, data, result):
        for listener in self.listeners:
            listener.end_return(data, result)

    def start_continue(self, data, result):
        for listener in self.listeners:
            listener.start_continue(data, result)

    def end_continue(self, data, result):
        for listener in self.listeners:
            listener.end_continue(data, result)

    def start_break(self, data, result):
        for listener in self.listeners:
            listener.start_break(data, result)

    def end_break(self, data, result):
        for listener in self.listeners:
            listener.end_break(data, result)

    def start_error(self, data, result):
        for listener in self.listeners:
            listener.start_error(data, result)

    def end_error(self, data, result):
        for listener in self.listeners:
            listener.end_error(data, result)

    def start_var(self, data, result):
        for listener in self.listeners:
            listener.start_var(data, result)

    def end_var(self, data, result):
        for listener in self.listeners:
            listener.end_var(data, result)

    def set_log_level(self, level):
        self._is_logged.set_level(level)

    def log_message(self, message):
        if self._is_logged(message.level):
            for listener in self.listeners:
                listener.log_message(message)

    def message(self, message):
        for listener in self.listeners:
            listener.message(message)

    def imported(self, import_type, name, attrs):
        for listener in self.listeners:
            listener.imported(import_type, name, attrs)

    def output_file(self, file_type, path):
        for listener in self.listeners:
            listener.output_file(file_type, path)

    def close(self):
        for listener in self.listeners:
            listener.close()

    def __bool__(self):
        return bool(self.listeners)


class LibraryListeners(Listeners):
    _listeners: 'list[list[ListenerFacade]]'

    def __init__(self, log_level='INFO'):
        super().__init__(log_level=log_level)

    @property
    def listeners(self):
        return self._listeners[-1] if self._listeners else []

    def new_suite_scope(self):
        self._listeners.append([])

    def discard_suite_scope(self):
        self._listeners.pop()

    def register(self, library):
        listeners = self._import_listeners(library.listeners, library=library)
        self._listeners[-1].extend(listeners)

    def close(self):
        pass

    def unregister(self, library, close=False):
        remaining = []
        for listener in self._listeners[-1]:
            if listener.library is not library:
                remaining.append(listener)
            elif close:
                listener.close()
        self._listeners[-1] = remaining


class ListenerFacade(LoggerApi, ABC):

    def __init__(self, listener, name, library=None):
        self.listener = listener
        self.name = name
        self.library = library

    def output_file(self, type_: str, path: str):
        method = self._get_method(f'{type_.lower()}_file')
        method(path)

    def _get_method(self, name):
        for method_name in self._get_method_names(name):
            method = getattr(self.listener, method_name, None)
            if method:
                return ListenerMethod(method, self.name)
        return ListenerMethod(None, self.name)

    def _get_method_names(self, name):
        names = [name, self._to_camelCase(name)] if '_' in name else [name]
        if self.library is not None:
            names += ['_' + name for name in names]
        return names

    def _to_camelCase(self, name):
        first, *rest = name.split('_')
        return ''.join([first] + [part.capitalize() for part in rest])


class ListenerV3Facade(ListenerFacade):

    def __init__(self, listener, name, library=None):
        super().__init__(listener, name, library)
        # Suite
        self.start_suite = self._get_method('start_suite')
        self.end_suite = self._get_method('end_suite')
        # Test
        self.start_test = self._get_method('start_test')
        self.end_test = self._get_method('end_test')
        # Keywords
        self.start_keyword = self._get_method('start_keyword')
        self.end_keyword = self._get_method('end_keyword')
        self._start_user_keyword = self._get_method('start_user_keyword')
        self._end_user_keyword = self._get_method('end_user_keyword')
        self._start_library_keyword = self._get_method('start_library_keyword')
        self._end_library_keyword = self._get_method('end_library_keyword')
        self._start_invalid_keyword = self._get_method('start_invalid_keyword')
        self._end_invalid_keyword = self._get_method('end_invalid_keyword')
        # IF
        self.start_if = self._get_method('start_if')
        self.end_if = self._get_method('end_if')
        self.start_if_branch = self._get_method('start_if_branch')
        self.end_if_branch = self._get_method('end_if_branch')
        # TRY
        self.start_try = self._get_method('start_try')
        self.end_try = self._get_method('end_try')
        self.start_try_branch = self._get_method('start_try_branch')
        self.end_try_branch = self._get_method('end_try_branch')
        # FOR
        self.start_for = self._get_method('start_for')
        self.end_for = self._get_method('end_for')
        self.start_for_iteration = self._get_method('start_for_iteration')
        self.end_for_iteration = self._get_method('end_for_iteration')
        # WHILE
        self.start_while = self._get_method('start_while')
        self.end_while = self._get_method('end_while')
        self.start_while_iteration = self._get_method('start_while_iteration')
        self.end_while_iteration = self._get_method('end_while_iteration')
        # VAR
        self.start_var = self._get_method('start_var')
        self.end_var = self._get_method('end_var')
        # BREAK
        self.start_break = self._get_method('start_break')
        self.end_break = self._get_method('end_break')
        # CONTINUE
        self.start_continue = self._get_method('start_continue')
        self.end_continue = self._get_method('end_continue')
        # RETURN
        self.start_return = self._get_method('start_return')
        self.end_return = self._get_method('end_return')
        # ERROR
        self.start_error = self._get_method('start_error')
        self.end_error = self._get_method('end_error')
        # Messages
        self.log_message = self._get_method('log_message')
        self.message = self._get_method('message')
        # Close
        self.close = self._get_method('close')

    def start_user_keyword(self, data, implementation, result):
        if self._start_user_keyword:
            self._start_user_keyword(data, implementation, result)
        else:
            self.start_keyword(data, result)

    def end_user_keyword(self, data, implementation, result):
        if self._end_user_keyword:
            self._end_user_keyword(data, implementation, result)
        else:
            self.end_keyword(data, result)

    def start_library_keyword(self, data, implementation, result):
        if self._start_library_keyword:
            self._start_library_keyword(data, implementation, result)
        else:
            self.start_keyword(data, result)

    def end_library_keyword(self, data, implementation, result):
        if self._end_library_keyword:
            self._end_library_keyword(data, implementation, result)
        else:
            self.end_keyword(data, result)

    def start_invalid_keyword(self, data, implementation, result):
        if self._start_invalid_keyword:
            self._start_invalid_keyword(data, implementation, result)
        else:
            self.start_keyword(data, result)

    def end_invalid_keyword(self, data, implementation, result):
        if self._end_invalid_keyword:
            self._end_invalid_keyword(data, implementation, result)
        else:
            self.end_keyword(data, result)


class ListenerV2Facade(ListenerFacade):

    def __init__(self, listener, name, library=None):
        super().__init__(listener, name, library)
        # Suite
        self._start_suite = self._get_method('start_suite')
        self._end_suite = self._get_method('end_suite')
        # Test
        self._start_test = self._get_method('start_test')
        self._end_test = self._get_method('end_test')
        # Keyword and control structures
        self._start_kw = self._get_method('start_keyword')
        self._end_kw = self._get_method('end_keyword')
        # Messages
        self._log_message = self._get_method('log_message')
        self._message = self._get_method('message')
        # Close
        self._close = self._get_method('close')

    def imported(self, import_type: str, name: str, attrs):
        method = self._get_method(f'{import_type.lower()}_import')
        method(name, attrs)

    def start_suite(self, data, result):
        self._start_suite(result.name, self._suite_attrs(data, result))

    def end_suite(self, data, result):
        self._end_suite(result.name, self._suite_attrs(data, result, end=True))

    def start_test(self, data, result):
        self._start_test(result.name, self._test_attrs(data, result))

    def end_test(self, data, result):
        self._end_test(result.name, self._test_attrs(data, result, end=True))

    def start_keyword(self, data, result):
        self._start_kw(result.full_name, self._keyword_attrs(data, result))

    def end_keyword(self, data, result):
        self._end_kw(result.full_name, self._keyword_attrs(data, result, end=True))

    def start_for(self, data, result):
        extra = self._for_extra_attrs(result)
        self._start_kw(result._log_name, self._attrs(data, result, **extra))

    def end_for(self, data, result):
        extra = self._for_extra_attrs(result)
        self._end_kw(result._log_name, self._attrs(data, result, **extra, end=True))

    def _for_extra_attrs(self, result):
        extra = {
            'variables': list(result.assign),
            'flavor': result.flavor or '',
            'values': list(result.values)
        }
        if result.flavor == 'IN ENUMERATE':
            extra['start'] = result.start
        elif result.flavor == 'IN ZIP':
            extra['fill'] = result.fill
            extra['mode'] = result.mode
        return extra

    def start_for_iteration(self, data, result):
        attrs = self._attrs(data, result, variables=dict(result.assign))
        self._start_kw(result._log_name, attrs)

    def end_for_iteration(self, data, result):
        attrs = self._attrs(data, result, variables=dict(result.assign), end=True)
        self._end_kw(result._log_name, attrs)

    def start_while(self, data, result):
        attrs = self._attrs(data, result, condition=result.condition,
                            limit=result.limit, on_limit=result.on_limit,
                            on_limit_message=result.on_limit_message)
        self._start_kw(result._log_name, attrs)

    def end_while(self, data, result):
        attrs = self._attrs(data, result, condition=result.condition,
                            limit=result.limit, on_limit=result.on_limit,
                            on_limit_message=result.on_limit_message, end=True)
        self._end_kw(result._log_name, attrs)

    def start_while_iteration(self, data, result):
        self._start_kw(result._log_name, self._attrs(data, result))

    def end_while_iteration(self, data, result):
        self._end_kw(result._log_name, self._attrs(data, result, end=True))

    def start_if_branch(self, data, result):
        extra = {'condition': result.condition} if result.type != result.ELSE else {}
        self._start_kw(result._log_name, self._attrs(data, result, **extra))

    def end_if_branch(self, data, result):
        extra = {'condition': result.condition} if result.type != result.ELSE else {}
        self._end_kw(result._log_name, self._attrs(data, result, **extra, end=True))

    def start_try_branch(self, data, result):
        extra = self._try_extra_attrs(result)
        self._start_kw(result._log_name, self._attrs(data, result, **extra))

    def end_try_branch(self, data, result):
        extra = self._try_extra_attrs(result)
        self._end_kw(result._log_name, self._attrs(data, result, **extra, end=True))

    def _try_extra_attrs(self, result):
        if result.type == BodyItem.EXCEPT:
            return {
                'patterns': list(result.patterns),
                'pattern_type': result.pattern_type,
                'variable': result.assign
            }
        return {}

    def start_return(self, data, result):
        attrs = self._attrs(data, result, values=list(result.values))
        self._start_kw(result._log_name, attrs)

    def end_return(self, data, result):
        attrs = self._attrs(data, result, values=list(result.values), end=True)
        self._end_kw(result._log_name, attrs)

    def start_continue(self, data, result):
        self._start_kw(result._log_name, self._attrs(data, result))

    def end_continue(self, data, result):
        self._end_kw(result._log_name, self._attrs(data, result, end=True))

    def start_break(self, data, result):
        self._start_kw(result._log_name, self._attrs(data, result))

    def end_break(self, data, result):
        self._end_kw(result._log_name, self._attrs(data, result, end=True))

    def start_error(self, data, result):
        self._start_kw(result._log_name, self._attrs(data, result))

    def end_error(self, data, result):
        self._end_kw(result._log_name, self._attrs(data, result, end=True))

    def start_var(self, data, result):
        extra = self._var_extra_attrs(result)
        self._start_kw(result._log_name, self._attrs(data, result, **extra))

    def end_var(self, data, result):
        extra = self._var_extra_attrs(result)
        self._end_kw(result._log_name, self._attrs(data, result, **extra, end=True))

    def _var_extra_attrs(self, result):
        if result.name.startswith('$'):
            value = (result.separator or ' ').join(result.value)
        else:
            value = list(result.value)
        return {'name': result.name, 'value': value, 'scope': result.scope or 'LOCAL'}

    def log_message(self, message):
        self._log_message(self._message_attributes(message))

    def message(self, message):
        self._message(self._message_attributes(message))

    def _suite_attrs(self, data, result, end=False):
        attrs = {
            'id': data.id,
            'doc': result.doc,
            'metadata': dict(result.metadata),
            'starttime': result.starttime,
            'longname': result.full_name,
            'tests': [t.name for t in data.tests],
            'suites': [s.name for s in data.suites],
            'totaltests': data.test_count,
            'source': str(data.source or '')
        }
        if end:
            attrs.update({
                'endtime': result.endtime,
                'elapsedtime': result.elapsedtime,
                'status': result.status,
                'message': result.message,
                'statistics': result.stat_message
            })
        return attrs

    def _test_attrs(self, data, result, end=False):
        attrs = {
            'id': data.id,
            'doc': result.doc,
            'tags': list(result.tags),
            'lineno': data.lineno,
            'starttime': result.starttime,
            'longname': result.full_name,
            'source': str(data.source or ''),
            'template': data.template or '',
            'originalname': data.name
        }
        if end:
            attrs.update({
                'endtime': result.endtime,
                'elapsedtime': result.elapsedtime,
                'status': result.status,
                'message': result.message,
            })
        return attrs

    def _keyword_attrs(self, data, result, end=False):
        attrs = {
            'doc': result.doc,
            'lineno': data.lineno,
            'type': result.type,
            'status': result.status,
            'starttime': result.starttime,
            'source': str(data.source or ''),
            'kwname': result.name or '',
            'libname': result.owner or '',
            'args':  [a if isinstance(a, str) else safe_str(a) for a in result.args],
            'assign': list(result.assign),
            'tags': list(result.tags)
        }
        if end:
            attrs.update({
                'endtime': result.endtime,
                'elapsedtime': result.elapsedtime
            })
        return attrs

    def _attrs(self, data, result, end=False, **extra):
        attrs = {
            'doc': '',
            'lineno': data.lineno,
            'type': result.type,
            'status': result.status,
            'starttime': result.starttime,
            'source': str(data.source or ''),
            'kwname': result._log_name,
            'libname': '',
            'args':  [],
            'assign': [],
            'tags': []
        }
        attrs.update(**extra)
        if end:
            attrs.update({
                'endtime': result.endtime,
                'elapsedtime': result.elapsedtime
            })
        return attrs

    def _message_attributes(self, msg):
        # Timestamp in our legacy format.
        timestamp = msg.timestamp.isoformat(' ', timespec='milliseconds').replace('-', '')
        attrs = {'timestamp': timestamp,
                 'message': msg.message,
                 'level': msg.level,
                 'html': 'yes' if msg.html else 'no'}
        return attrs

    def close(self):
        self._close()


class ListenerMethod:
    # Flag to avoid recursive listener calls.
    called = False

    def __init__(self, method, name):
        self.method = method
        self.listener_name = name

    def __call__(self, *args):
        if self.method is None:
            return
        if self.called:
            return
        try:
            ListenerMethod.called = True
            self.method(*args)
        except TimeoutError:
            # Propagate possible timeouts:
            # https://github.com/robotframework/robotframework/issues/2763
            raise
        except Exception:
            message, details = get_error_details()
            LOGGER.error(f"Calling method '{self.method.__name__}' of listener "
                         f"'{self.listener_name}' failed: {message}")
            LOGGER.info(f"Details:\n{details}")
        finally:
            ListenerMethod.called = False

    def __bool__(self):
        return self.method is not None
