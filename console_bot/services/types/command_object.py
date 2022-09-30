from dataclasses import dataclass


@dataclass
class Command:
    name: str
    phone: str
    birthday: str = None
