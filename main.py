from fetcher import Fetcher
from filebuilder import FileBuilder
import gc


fb = FileBuilder(Fetcher())

fb.build_root_file()

gc.collect()
print(len(gc.get_objects()))
