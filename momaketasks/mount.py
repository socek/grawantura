from pathlib import Path
from subprocess import Popen

from momake.dependency import FileDependency
from momake.exceptions import TaskFailed
from momake.task import Task

root = Path(__file__).parent.parent
qqpath = str(root / "backend" / "code" / "qq")


class MountQQ(Task):
    name = "MountQQ"
    dependecies = [
        FileDependency(qqpath, "__init__.py"),
    ]

    def action(self):
        cmd = [
            "sudo",
            "mount",
            "-o",
            "bind",
            "/home/socek/projects/sapp/qq",
            qqpath,
        ]
        if Popen(cmd).wait() != 0:
            raise TaskFailed(self.name)
