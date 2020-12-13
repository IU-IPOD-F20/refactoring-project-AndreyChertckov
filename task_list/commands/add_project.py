from typing import List

from task_list.data_modules import ProjectSet, Project

from . import Command, CommandResponse, Parameters, ParseError


class AddProjectParameters(Parameters):

    def __init__(self, project_name: str):
        self.project_name = project_name

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'AddProjectParameters':
        try:
            return cls(project_name=inp[0])
        except IndexError:
            raise ParseError("Missing Argument")


class AddProjectCommand(Command):

    def __init__(self, parameters: AddProjectParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        if not projects.get_project_by_name(self.parameters.project_name) is None:
            return CommandResponse(message=f"Project with name {self.parameters.project_name} already exists.", new_state=projects)
        project = Project(name=self.parameters.project_name)
        projects.append(project)
        return CommandResponse(message="", new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return AddProjectParameters
