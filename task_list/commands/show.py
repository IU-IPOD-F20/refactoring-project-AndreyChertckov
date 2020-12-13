from typing import List
from datetime import datetime

from task_list.data_modules import ProjectSet, Project, Task

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
                if self.filter(task):
                    response += f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}\n"
            response += "\n"
        response = response[:-1]
        return CommandResponse(message=response, new_state=projects)

    def filter(self, task: Task) -> bool:
        return True

    @classmethod
    def get_parameters_class(cls) -> type:
        return ShowParameters


class TodayCommand(ShowCommand):
    
    def filter(self, task: Task):
        today = datetime.today()
        return today.date() == task.deadline.date()
