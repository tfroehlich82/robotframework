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

from robot.errors import DataError
from robot.result import Keyword as KeywordResult
from robot.variables import VariableAssignment

from .arguments import EmbeddedArguments
from .model import Keyword
from .statusreporter import StatusReporter
from .keywordimplementation import KeywordImplementation


class InvalidKeyword(KeywordImplementation):
    type = KeywordImplementation.INVALID_KEYWORD

    def _get_embedded(self, name) -> 'EmbeddedArguments|None':
        try:
            return super()._get_embedded(name)
        except DataError:
            return None

    def create_runner(self, name, languages=None):
        return InvalidKeywordRunner(self, name)

    def bind(self, data: Keyword) -> 'InvalidKeyword':
        return self.copy(parent=data.parent)


class InvalidKeywordRunner:

    def __init__(self, keyword, name=None):
        self.keyword = keyword
        self.name = name or keyword.name

    def run(self, data, context, run=True):
        kw = self.keyword.bind(data)
        result = KeywordResult(name=self.name,
                               owner=kw.owner.name if kw.owner else None,
                               args=data.args,
                               assign=tuple(VariableAssignment(data.assign)),
                               type=data.type)
        with StatusReporter(data, result, context, run, implementation=kw):
            if run:
                raise DataError(kw.error)

    dry_run = run
