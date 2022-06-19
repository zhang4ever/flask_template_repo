from enum import Enum, unique


@unique
class RiskLevel(Enum):
    HIGH = '高'
    MIDDLE = '中'
    LOW = '低'

    @classmethod
    def mame_of(cls, risk: str):

        if risk == '高':
            return cls.HIGH
        elif risk == '中':
            return cls.MIDDLE
        else:
            return cls.LOW
