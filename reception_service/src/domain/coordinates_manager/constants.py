from enum import Enum


class FileStatus(str, Enum):
    IN_PROCESS = 'in_process'
    PROCESSED = 'processed'


class CoordinateProcessStatus(str, Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    NOT_FOUND = 'not_found'
