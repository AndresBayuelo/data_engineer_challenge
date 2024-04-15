from enum import Enum


class FileStatus(str, Enum):
    IN_PROCESS = 'in_process'
    PROCESSED = 'processed'
