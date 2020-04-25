import enum


class AttemptStatus(enum.Enum):
    attempted = 'attempted'
    submitted = 'submitted'
    unattempted = 'unattempted'