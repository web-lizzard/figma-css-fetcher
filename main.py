import gc

from converter import Converter
from fetcher import FigmaFetcher
from filebuilder import FileBuilder


def main():
    converter = Converter(fetcher=FigmaFetcher())
    file_builder = FileBuilder(converter=converter)
    converter.convert_values()
    file_builder.create_reset_scss()
    file_builder.build_root_file()
    file_builder.build_utilities()


main()
gc.collect()
print(len(gc.get_objects()))


if __name__ == "__main__":
    main()
