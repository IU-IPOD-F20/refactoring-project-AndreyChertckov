from typing import List

from task_list.data_modules import ProjectSet, Project, TaskUid

from . import Command, CommandResponse, Parameters, ParseError


class HelpParameters(Parameters):

    def __init__(self):
        pass

    @classmethod
    def parse_input_to_parameters(cls, inp: List[str]) -> 'HelpParameters':
        return cls()


class HelpCommand(Command):

    def __init__(self, parameters: HelpParameters):
        pass

    def execute(self, projects: ProjectSet) -> CommandResponse:
        response = "Commands:\n"
        response += "  show\n"
        response += "  add project <project name>\n"
        response += "  add task <project name> <task description>\n"
        response += "  check <task ID>\n"
        response += "  uncheck <task ID>\n"
        return CommandResponse(message=response, new_state=projects)

    @classmethod
    def get_parameters_class(cls) -> type:
        return HelpParameters
