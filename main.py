from fetcher.fetcher import Fetcher
from fetcher.filebuilder import FileBuilder
import gc


fb = FileBuilder(Fetcher())

fb.create_reset_scss()
fb.build_root_file()
fb.build_utilities()

gc.collect()
print(len(gc.get_objects()))
