from typing import List

from task_list.data_modules import ProjectSet, Project
from task_list.task import Task

from . import Command, CommandResponse, Parameters


class ShowParameters(Parameters):

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'ShowParameters':
        return cls()


class ShowCommand(Command):

    def __init__(self, parameters: ShowParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        response = ""
        for (project_name, project) in projects:
            response += f"{project.name}\n"
            for task in project:
                response += f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}\n"
            response += "\n"
        response = response[:-1]
        return CommandResponse(message=response, new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return ShowParameters
