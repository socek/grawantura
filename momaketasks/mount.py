from subprocess import Popen

from momake.dependency import FileDependency
from momake.exceptions import TaskFailed
from momake.task import Task


class MountQQ(Task):
    name = "MountQQ"
    dependecies = [
        FileDependency("backend/code/qq/", "__init__.py"),
    ]

    def action(self):
        cmd = [
            "sudo",
            "mount",
            "-o",
            "bind",
            "/home/socek/projects/sapp/qq",
            "backend/code/qq",
        ]
        if Popen(cmd).wait() != 0:
            raise TaskFailed(self.name)
