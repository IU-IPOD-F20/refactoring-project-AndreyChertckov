from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Set, Optional, Iterator, List

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
class Task:
    id: TaskUid
    description: str
    done: bool
    deadline: Optional[datetime] = None

    def set_done(self, done: bool):
        self.done = done

    def is_done(self) -> bool:
        return self.done

    def set_deadline(self, deadline):
        self.deadline = deadline

@dataclass
class Project:
    name: str
    tasks: Dict[TaskUid, Task] = field(default_factory=dict)
    tasks_deadline: Dict[datetime, List[TaskUid]] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.name)

    def add_task(self, task_uid: TaskUid, task: Task):
        self.tasks[task_uid] = task
        if task.deadline:
            if task_uid not in self.tasks_deadline:
                self.tasks_deadline[task.deadline] = []
            self.tasks_deadline[task.deadline] += [task_uid]

    def __iter__(self):
        return iter(self.tasks.values())

    def get_task_by_id(self, uid: TaskUid) -> Optional[Task]:
        return self.tasks.get(uid, None)

    def pop_task_by_id(self, uid: TaskUid) -> Optional[Task]:
        return self.tasks.pop(uid, None)

    def delete_task_by_id(self, uid: TaskUid):
        task = self.tasks.pop(uid)
        if task.deadline:
            self.tasks_deadline[task.deadline].remove(uid)


@dataclass
class ProjectSet:
    projects: Dict[str, Project] = field(default_factory=dict)

    def append(self, project: Project):
        self.projects[project.name] = project

    def get_project_by_name(self, name: str) -> Optional[Project]:
        return self.projects.get(name, None)
    
    def __iter__(self):
        return iter(self.projects.items())

