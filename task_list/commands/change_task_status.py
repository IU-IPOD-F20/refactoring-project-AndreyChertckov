from typing import List

from task_list.data_modules import ProjectSet, Project, TaskUid

from . import Command, CommandResponse, Parameters, ParseError


class ChangeStateParameters(Parameters):

    def __init__(self, task_id: str):
        self.task_id = task_id

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'ChangeStateParameters':
        try:
            return cls(task_id=TaskUid.from_string(inp[0]))
        except IndexError:
            raise ParseError("Missing Argument")


class ChangeStateBaseCommand(Command):

    def __init__(self, parameters: ChangeStateParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        for (_, project) in projects:
            task = project.get_task_by_id(self.parameters.task_id)
            if task is None:
                continue
            task.set_done(self.get_check())
            break
        else:
            return CommandResponse(message=f"Task with id {self.parameters.task_id} not found", new_state=projects)
            pass
        return CommandResponse(message="", new_state=projects)

    def get_check(self) -> bool:
        pass

    @classmethod
    def get_parameters_class(cls) -> type:
        return ChangeStateParameters


class CheckCommand(ChangeStateBaseCommand):
    def get_check(self) -> bool:
        return True

class UnCheckCommand(ChangeStateBaseCommand):
    def get_check(self) -> bool:
        return False
