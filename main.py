from scraper import Scraper
from file_builder import FileBuilder
import gc


FileBuilder(Scraper())

gc.collect()
print(len(gc.get_objects()))
