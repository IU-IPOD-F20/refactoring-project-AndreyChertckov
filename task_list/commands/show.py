from typing import List
from datetime import datetime
from collections import defaultdict

from task_list.data_modules import ProjectSet, Project, Task

from . import Command, CommandResponse, Parameters


class ShowParameters(Parameters):

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'ShowParameters':
        return cls()


class ShowByProjectCommand(Command):

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


class ShowByDeadlineCommand(ShowByProjectCommand):
    
    def filter(self, task: Task):
        if task.deadline is None:
            return False
        today = datetime.today()
        return today.date() == task.deadline.date()


class ShowByDateCommand(Command):
    
    def __init__(self, parameters: ShowParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) ->  CommandResponse:
        date_to_task = defaultdict(list)
        for (_,project) in projects:
            for (date, task_uids) in project.tasks_deadline.items():
                date_to_task[date].extend(map(project.get_task_by_id, task_uids))

        response = ""
        for (date, tasks) in date_to_task.items():
            response += f"{date.strftime('%d/%m/%Y')}\n"
            for task in tasks:
                response += f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}\n"
            response += "\n"

        response = response[:-1]
        return CommandResponse(message=response, new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return ShowParameters
