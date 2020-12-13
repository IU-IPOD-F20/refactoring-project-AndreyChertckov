from typing import List

from task_list.data_modules import ProjectSet, Project, TaskUid

from . import Command, CommandResponse, Parameters, ParseError


class DeleteParameters(Parameters):

    def __init__(self, task_id: str):
        self.task_id = task_id

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'DeleteParameters':
        try:
            return cls(task_id=TaskUid.from_string(inp[0]))
        except IndexError:
            raise ParseError("Missing Argument")


class DeleteCommand(Command):

    def __init__(self, parameters: DeleteParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        for (_, project) in projects:
            task = project.get_task_by_id(self.parameters.task_id)
            if task is None:
                continue
            project.delete_task_by_id(self.parameters.task_id)
            break
        else:
            return CommandResponse(message=f"Task with id {self.parameters.task_id} not found", new_state=projects)
        return CommandResponse(message="", new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return DeleteParameters
