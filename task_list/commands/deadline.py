from typing import List
from datetime import datetime

from task_list.data_modules import ProjectSet, Project, TaskUid

from . import Command, CommandResponse, Parameters, ParseError


class DeadlineParameters(Parameters):

    def __init__(self, task_id: TaskUid, deadline: datetime):
        self.task_id = task_id
        self.deadline = deadline

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'AddProjectParameters':
        try:
            task_id_str, *datetime_str = inp
            datetime_str = " ".join(datetime_str)
            task_id = TaskUid.from_string(task_id_str)
            deadline = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
            return cls(task_id, deadline)
        except IndexError:
            raise ParseError("Missing Arguments")


class DeadlineCommand(Command):

    def __init__(self, parameters: DeadlineParameters):
        self.parameters = parameters

    def execute(self, projects: ProjectSet) -> CommandResponse:
        for (_, project) in projects:
            task = project.get_task_by_id(self.parameters.task_id)
            if task is None:
                continue

            task.set_deadline(self.parameters.deadline)
            break
        else:
            return CommandResponse(message=f"Task with id {self.parameters.task_id} not found", new_state=projects)
            pass
        return CommandResponse(message="", new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return DeadlineParameters
