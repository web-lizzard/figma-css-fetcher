from scraper import Scraper
from file_builder import FileBuilder
import gc


FileBuilder(Scraper())


print(len(gc.get_objects()))
