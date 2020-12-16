from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from task_list.data_modules import ProjectSet

@dataclass
class CommandResponse:
    message: str
    new_state: ProjectSet


class Parameters(ABC):
    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'Parameters':
        pass

class Command(ABC):

    @abstractmethod
    def execute(self, projects: ProjectSet) -> CommandResponse:
        pass
    

    @classmethod
    def get_parameters_class(cls) -> Parameters:
        pass
