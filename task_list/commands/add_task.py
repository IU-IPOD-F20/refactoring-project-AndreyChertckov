from typing import List

from task_list.data_modules import ProjectSet, Project, TaskUid
from task_list.task import Task

from . import Command, CommandResponse, Parameters, ParseError


class AddTaskParameters(Parameters):

    def __init__(self, project_name: str, description: str):
        self.project_name = project_name
        self.description = description

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'AddProjectParameters':
        try:
            return cls(inp[0], ' '.join(inp[1:]))
        except IndexError:
            raise ParseError("Missing Arguments")


class AddTaskCommand(Command):

    task_uid_generator = TaskUid.uid_generator()

    def __init__(self, parameters: AddTaskParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        project = projects.get_project_by_name(self.parameters.project_name)
        if project is None:
            return CommandResponse(message=f"Project with name {self.parameters.project_name} does not exists.", new_state=projects)

        uid = next(self.task_uid_generator)
        project.add_task(uid, Task(uid, self.parameters.description, done=False))
        return CommandResponse(message="", new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return AddTaskParameters
