from typing import List

from task_list.data_modules import ProjectSet, Project, TaskUid, Task

from . import Command, CommandResponse, Parameters, ParseError


class AddTaskParameters(Parameters):

    def __init__(self, project_name: str, task_uid: TaskUid, description: str):
        self.project_name = project_name
        self.description = description
        self.task_uid = task_uid

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'AddProjectParameters':
        try:
            return cls(inp[0], TaskUid.from_string(inp[1]), ' '.join(inp[2:]))
        except IndexError:
            raise ParseError("Missing Arguments")


class AddTaskCommand(Command):

    def __init__(self, parameters: AddTaskParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        project = projects.get_project_by_name(self.parameters.project_name)
        if project is None:
            return CommandResponse(message=f"Project with name {self.parameters.project_name} does not exists.", new_state=projects)

        project.add_task(self.parameters.task_uid, Task(self.parameters.task_uid, self.parameters.description, done=False))
        return CommandResponse(message="", new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return AddTaskParameters
