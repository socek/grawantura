from subprocess import Popen

from momake.dependency import AlwaysDependency
from momake.exceptions import TaskFailed
from momake.task import Task
from momaketasks.dockerapi import DockerUpTask


class ShellTask(Task):
    name = "shell"

    dependecies = [
        DockerUpTask(),
        AlwaysDependency(),
    ]

    def action(self):
        cmd = ["docker-compose", "exec", "webapi", "bash"]
        if Popen(cmd).wait() != 0:
            raise TaskFailed(self.name)
