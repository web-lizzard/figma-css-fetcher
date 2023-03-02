import gc

from fetcher import Fetcher
from filebuilder import FileBuilder


def main():
    file_builder = FileBuilder(Fetcher())

    file_builder.create_reset_scss()
    file_builder.build_root_file()
    file_builder.build_utilities()


main()
gc.collect()
print(len(gc.get_objects()))
