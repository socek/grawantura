from subprocess import Popen

from momake.dependency import AlwaysDependency
from momake.exceptions import TaskFailed
from momake.task import Task
from momaketasks.dockerapi import DockerServiceShouldRunDependency


class PsqlShellTask(Task):
    name = "psql"

    dependecies = [
        DockerServiceShouldRunDependency("postgres"),
        AlwaysDependency(),
    ]

    def action(self):
        cmd = ["/usr/bin/docker-compose", "exec", "postgres", "psql", "-U", "fajabot"]
        if Popen(cmd).wait() != 0:
            raise TaskFailed(self.name)
