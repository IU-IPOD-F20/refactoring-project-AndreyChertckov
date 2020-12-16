from typing import Dict, Union, List
from task_list.commands import (
    Command,
    AddProjectCommand,
    AddTaskCommand,
    ShowByProjectCommand,
    CheckCommand,
    UnCheckCommand,
    HelpCommand,
    DeadlineCommand,
    DeleteCommand,
    ShowByDeadlineCommand,
    ShowByDateCommand,
)


class RouteNotFound(Exception):
    pass

class Router:
    def __init__(self):
        self.routes = {
            "add": {"project": AddProjectCommand, "task": AddTaskCommand},
            "view": {
                "by": {
                    "project": ShowByProjectCommand,
                    "deadline": ShowByDeadlineCommand,
                    "date": ShowByDateCommand,
                }
            },
            "check": CheckCommand,
            "uncheck": UnCheckCommand,
            "help": HelpCommand,
            "deadline": DeadlineCommand,
            "delete": DeleteCommand,
        }

    def __call__(self, inp: str) -> Command:
        def recursive_go(
            routes: Dict[str, Union[type, dict]], inp_list: List[str]
        ) -> Command:
            if not len(inp_list):
                raise RouteNotFound(f"Command {inp} not found")
            try:
                current_ind, *inp_list = inp_list
                current = routes[current_ind]
            except KeyError:
                raise RouteNotFound(f"Command {inp} not found")

            if isinstance(current, type):
                parameters_class = current.get_parameters_class()
                parameters = parameters_class.parse_input_to_parameters(inp_list)
                return current(parameters)
            else:
                return recursive_go(current, inp_list)

        return recursive_go(self.routes, inp.split(" "))
