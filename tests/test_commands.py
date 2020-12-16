import unittest
from datetime import datetime, timedelta

from task_list.data_modules import ProjectSet, Project, Task, TaskUid
from task_list.commands import (
    AddProjectCommand,
    AddTaskCommand,
    CheckCommand,
    UnCheckCommand,
    ShowByProjectCommand,
    DeadlineCommand,
    ShowByDeadlineCommand,
    ShowByDateCommand,
    DeleteCommand,
)


class TestCommands(unittest.TestCase):
    def test_add_project(self):
        projects = ProjectSet()
        parameters_class = AddProjectCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["test"])
        command = AddProjectCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {})})
        self.assertEqual(expected_projects, result_projects)

    def test_add_task(self):
        projects = ProjectSet({"test": Project("test", {})})
        parameters_class = AddTaskCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["test", "task"])
        command = AddTaskCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})}
        )
        self.assertEqual(expected_projects, result_projects)

    def test_check_task(self):
        projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})}
        )
        parameters_class = CheckCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = CheckCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})}
        )
        self.assertEqual(expected_projects, result_projects)

    def test_uncheck_task(self):
        projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})}
        )
        parameters_class = UnCheckCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = UnCheckCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})}
        )
        self.assertEqual(expected_projects, result_projects)

    def test_view_by_project(self):
        projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})}
        )
        parameters_class = ShowByProjectCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters([])
        command = ShowByProjectCommand(parameters)
        message = command.execute(projects).message
        expected_message = """test\n  [x] 1: task\n"""
        self.assertEqual(expected_message, message)

    def test_deadline(self):
        projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})}
        )
        parameters_class = DeadlineCommand.get_parameters_class()
        datetime_str = datetime.today().strftime("%d/%m/%Y")
        _datetime = datetime.strptime(datetime_str, "%d/%m/%Y")
        parameters = parameters_class.parse_input_to_parameters(
            ["1", *datetime_str.split(" ")]
        )
        command = DeadlineCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet(
            {
                "test": Project(
                    "test",
                    tasks_deadline={_datetime: [TaskUid(1)]},
                    tasks={TaskUid(1): Task(TaskUid(1), "task", True, _datetime)},
                )
            }
        )
        self.assertEqual(expected_projects, result_projects)

    def test_view_by_deadline(self):
        projects = ProjectSet(
            {
                "test": Project(
                    "test",
                    {TaskUid(1): Task(TaskUid(1), "task", True, datetime.today())},
                )
            }
        )
        parameters_class = ShowByDeadlineCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters([])
        command = ShowByDeadlineCommand(parameters)
        message = command.execute(projects).message
        expected_message = """test\n  [x] 1: task\n"""
        self.assertEqual(expected_message, message)

    def test_view_by_date(self):
        projects = ProjectSet(
            {
                "test": Project(
                    "test",
                    {
                        TaskUid(1): Task(TaskUid(1), "task", True, datetime.today()),
                        TaskUid(2): Task(TaskUid(2), "task", True, datetime.today()),
                        TaskUid(3): Task(TaskUid(3), "task", False, datetime.today() + timedelta(days=1)),
                    },
                    {
                        datetime.today().date(): [TaskUid(1), TaskUid(2)],
                        (datetime.today() + timedelta(days=1)).date(): [TaskUid(3)],
                    },
                )
            }
        )
        parameters_class = ShowByDateCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters([])
        command = ShowByDateCommand(parameters)
        message = command.execute(projects).message
        expected_message = f"""{datetime.today().strftime("%d/%m/%Y")}\n  [x] 1: task\n  [x] 2: task\n\n{(datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")}\n  [ ] 3: task\n"""
        self.assertEqual(expected_message, message)

    def test_delete_task(self):
        projects = ProjectSet(
            {"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})}
        )
        parameters_class = DeleteCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = DeleteCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {})})
        self.assertEqual(expected_projects, result_projects)
