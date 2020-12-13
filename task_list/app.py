from typing import Dict, List, Union

from task_list.console import Console
from task_list.data_modules import ProjectSet
from task_list.commands import Command, CommandResponse, ParseError, AddProjectCommand, AddTaskCommand, ShowCommand, CheckCommand, UnCheckCommand, HelpCommand, DeadlineCommand, TodayCommand


class RouteNotFound(Exception):
    pass

class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:
        self.console = console
        self.last_id: int = 0
        self.projects: ProjectSet = ProjectSet()
        self.routes = { "add": {"project": AddProjectCommand, "task": AddTaskCommand}, "show": ShowCommand, "check": CheckCommand, "uncheck": UnCheckCommand , "help": HelpCommand, "deadline": DeadlineCommand, "today": TodayCommand}

    def run(self) -> None:
        while True:
            inp = self.console.input("> ")
            if inp == self.QUIT:
                break
            try:
                command = self.router(inp)
                self.execute(command)
            except RouteNotFound:
                self.error(inp)
            except ParseError as exc:
                self.console.print(f"Parsing command return: {exc}")

    def router(self, inp: str) -> Command:

        def recursive_go(routes: Dict[str, Union[type, dict]], inp_list: List[str]) -> Command:
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

    def execute(self, command: Command) -> None:
        command_response = command.execute(self.projects)
        self.projects = command_response.new_state
        if command_response.message:
            self.console.print(command_response.message)


    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def error(self, command: str) -> None:
        self.console.print(f"I don't know what the command {command} is.")
        self.console.print()
