from multiprocessing import Process
from pathlib import Path
import subprocess
import secrets
import math
import os


def convert_seconds_to_human_readable(seconds: int):

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


class ViAuCutter:

    def __init__(self, file: str, part_size_mb: int, out: str, paralell: int):

        self.file = file
        self.part_size_mb = int(part_size_mb)
        self.duration = self.get_duration(file=file)
        self.out = out
        self.paralell = paralell

        self.file_name: str = self.file.split("/")[-1] if "/" in self.file else self.file

        self.base_path: Path = Path(__file__).resolve().parent
        self.file_size: int = os.stat(self.file).st_size
        self.total_parts: int = math.ceil(self.file_size / (self.part_size_mb * 1024 * 1024))
        self.part_duration: int = self.duration / self.total_parts
        self.folder_name: str = os.path.join(out, secrets.token_hex(32))

    @staticmethod
    def get_duration(file: str) -> float:

        command = [
            'ffprobe',
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            file
        ]
        duration_string: str = subprocess.check_output(
            command, stderr=subprocess.STDOUT
        ).decode('utf-8')
        duration: float = float(duration_string)

        return duration

    def initialize_command(self, start: int, end: int, count: int) -> list:

        return [
            "ffmpeg", "-ss", convert_seconds_to_human_readable(start), "-i",
            self.file, "-t",
            convert_seconds_to_human_readable(end), "-c:v", "copy",
            "-c:a", "copy", f"{self.folder_name}/{count}__{self.file_name}"
        ]

    def cut(self) -> None:

        if not os.path.exists(self.out):

            os.mkdir(self.out)

        if not os.path.exists(self.folder_name):

            os.mkdir(self.folder_name)

        paralells: list = []
        for i in range(self.total_parts):

            start_time = i * self.part_duration

            command: list = self.initialize_command(
                start=start_time, end=self.part_duration, count=i + 1
            )
            p: Process = Process(
                target=subprocess.run, args=(command,), kwargs={"capture_output": True}
            )
            paralells.append(p)

            if self.paralell > 0 and len(paralells) == self.paralell:

                for process in paralells:

                    process.start()

                for process in paralells:

                    process.join()

                paralells.clear()

            elif i + 1 == self.total_parts and paralells != self.paralell:

                for process in paralells:

                    process.start()

                for process in paralells:

                    process.join()

                paralells.clear()
