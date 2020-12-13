
from dataclasses import dataclass, field
from typing import Dict, Set, Optional, Iterator

from task_list.task import Task

@dataclass
class TaskUid:
    uid: int

    @classmethod
    def uid_generator(cls) -> Iterator:
        i = 1
        while True:
            yield cls(uid=i)
            i += 1

    def __hash__(self):
        return hash(self.uid)

    def __str__(self):
        return str(self.uid)

    @classmethod
    def from_string(cls, string: str) -> 'TaskUid':
        return cls(uid=int(string))


@dataclass
class Project:
    name: str
    tasks: Dict[TaskUid, Task] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.name)

    def add_task(self, task_uid: TaskUid, task: Task):
        self.tasks[task_uid] = task

    def __iter__(self):
        return iter(self.tasks.values())

    def get_task_by_id(self, uid: TaskUid) -> Optional[Task]:
        return self.tasks.get(uid, None)


@dataclass
class ProjectSet:
    projects: Dict[str, Project] = field(default_factory=dict)

    def append(self, project: Project):
        self.projects[project.name] = project

    def get_project_by_name(self, name: str) -> Optional[Project]:
        return self.projects.get(name, None)
    
    def __iter__(self):
        return iter(self.projects.items())
