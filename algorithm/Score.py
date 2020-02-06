from abc import ABC, abstractmethod

class Score(ABC):
    def __init__(self, key: str):
        self.key = key

    @property
    @abstractmethod
    def value(self) -> float:
        return 0

    # @abstractmethod
    # def __add__(self, other):
    # 	pass

    @abstractmethod
    def __iadd__(self, other):
        pass

    def __str__(self):
        return "%s: %.4f" % (self.key, self.value)

class AccScore(Score):
    def __init__(self, key: str, correct: int, total: int):
        super(AccScore, self).__init__(key)
        self.correct = correct
        self.total = total

    @property
    def value(self) -> float:
        if self.total == 0: return 0
        return self.correct / self.total

    # def __add__(self, other):
    # 	assert type(other) is AccScore and self.key == other.key
    # 	return AccScore(self.key, self.correct + other.correct, self.total + other.total)

    def __iadd__(self, other):
        assert type(other) is AccScore and self.key == other.key
        self.correct += other.correct
        self.total += other.total
        return self


class CRF1Score(Score):
    def __init__(self, key: str, pre: AccScore, rec: AccScore):
        super(CRF1Score, self).__init__(key)
        self.pre = pre
        self.rec = rec

    @property
    def value(self) -> float:
        if self.pre.total == 0: return 0
        if self.rec.total == 0: return 0
        if (self.pre.value + self.rec.value) == 0: return 0
        return 2 * self.pre.value * self.rec.value / (self.pre.value + self.rec.value)

    def __iadd__(self, other):
        return self
