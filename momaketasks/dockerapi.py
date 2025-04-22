from datetime import datetime
from subprocess import PIPE
from subprocess import Popen
from uuid import UUID

from momake.dependency import Dependency
from momake.exceptions import TaskFailed
from momake.task import Task
from momaketasks.mount import MountQQ


def docker(args: list):
    cmd = ["/usr/bin/docker-compose"] + args
    with Popen(cmd, stdout=PIPE) as proc:
        assert proc.stdout
        return proc.stdout.read().decode("utf8")


def ps():
    stdout = docker(["ps"])
    lines = stdout.split("\n")
    headers = [col.strip() for col in lines[0].split(" ") if col.strip() != ""]
    columns = []
    for header in headers:
        columns.append(
            {
                "name": header,
                "start": lines[0].index(header),
            }
        )
    for index, column in enumerate(columns):
        if index < len(columns) - 1:
            column["end"] = columns[index + 1]["start"] - 1
        else:
            column["end"] = None
    processes = {}
    for line in lines[1:]:
        if line.strip() == "":
            continue
        row = {}
        for column in columns:
            row[column["name"]] = line[column["start"] : column["end"]].strip()
        processes[row["NAME"]] = row

    return processes


def is_service_running(name: str) -> bool:
    for process in ps().values():
        if process["SERVICE"] == name:
            return process["STATUS"].startswith("Up")
    return False


class DockerServiceShouldRunDependency(Dependency):
    def __init__(self, service: str):
        self.service = service

    def has_changed(self, last_runtime: datetime, run_id: UUID) -> bool:
        return not is_service_running(self.service)


class DockerUpTask(Task):
    name = "dockerup"

    dependecies = [
        MountQQ(),
        DockerServiceShouldRunDependency("webapi"),
        DockerServiceShouldRunDependency("frontend"),
        DockerServiceShouldRunDependency("postgres"),
        DockerServiceShouldRunDependency("traefik"),
    ]

    def action(self):
        cmd = ["/usr/bin/docker-compose", "up", "-d"]
        if Popen(cmd).wait() != 0:
            raise TaskFailed(self.name)
