from abc import ABC, abstractmethod

from models.models import Color


class Fetcher(ABC):
    font_families: set[str]
    font_weights: set[str]
    letter_spacing: set[str]
    colors_set: set[Color]
    font_sizes: set[int]

    @abstractmethod
    def fetch_values(self, data):
        pass
