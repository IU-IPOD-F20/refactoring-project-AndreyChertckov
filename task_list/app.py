from typing import Dict, List, Union

from task_list.console import Console
from task_list.data_modules import ProjectSet
from task_list.router import Router, RouteNotFound
from task_list.commands import Command


class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console, router: Router) -> None:
        self.console = console
        self.last_id: int = 0
        self.projects: ProjectSet = ProjectSet()
        self.router = router

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


    def execute(self, command: Command) -> None:
        command_response = command.execute(self.projects)
        self.projects = command_response.new_state
        if command_response.message:
            self.console.print(command_response.message)
