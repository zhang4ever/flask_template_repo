from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Person(DataClassJsonMixin):
    name: str
    age: int
    address: str
    job: str

