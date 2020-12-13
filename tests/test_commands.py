import unittest
from datetime import datetime

from task_list.data_modules import ProjectSet, Project, Task, TaskUid
from task_list.commands import AddProjectCommand, AddTaskCommand, CheckCommand, UnCheckCommand, ShowCommand, DeadlineCommand, TodayCommand, DeleteCommand


class TestCommands(unittest.TestCase):
    
    def test_add_project(self):
        projects = ProjectSet()
        parameters_class = AddProjectCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["test"])
        command = AddProjectCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {})})
        self.assertEqual(expected_projects,result_projects)

    def test_add_task(self):
        projects = ProjectSet({"test": Project("test", {})})
        parameters_class = AddTaskCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["test", "task"])
        command = AddTaskCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})})
        self.assertEqual(expected_projects,result_projects)

    def test_check_task(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})})
        parameters_class = CheckCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = CheckCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})})
        self.assertEqual(expected_projects,result_projects)

    def test_uncheck_task(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})})
        parameters_class = UnCheckCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = UnCheckCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})})
        self.assertEqual(expected_projects,result_projects)

    def test_show(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})})
        parameters_class = ShowCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters([])
        command = ShowCommand(parameters)
        message = command.execute(projects).message
        expected_message = """test\n  [x] 1: task\n"""
        self.assertEqual(expected_message, message)

    def test_deadline(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True)})})
        parameters_class = DeadlineCommand.get_parameters_class()
        datetime_str = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        parameters = parameters_class.parse_input_to_parameters(["1", *datetime_str.split(" ")])
        command = DeadlineCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True, datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S"))})})
        self.assertEqual(expected_projects,result_projects)

    def test_today(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", True, datetime.today())})})
        parameters_class = TodayCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters([])
        command = TodayCommand(parameters)
        message = command.execute(projects).message
        expected_message = """test\n  [x] 1: task\n"""
        self.assertEqual(expected_message, message)

    def test_delete_task(self):
        projects = ProjectSet({"test": Project("test", {TaskUid(1): Task(TaskUid(1), "task", False)})})
        parameters_class = DeleteCommand.get_parameters_class()
        parameters = parameters_class.parse_input_to_parameters(["1"])
        command = DeleteCommand(parameters)
        result_projects = command.execute(projects).new_state
        expected_projects = ProjectSet({"test": Project("test", {})})
        self.assertEqual(expected_projects,result_projects)
