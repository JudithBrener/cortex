import importlib
import inspect
import pathlib


def get_available_parsers():
    available_parsers = {}
    current_directory = pathlib.Path(__file__).parent.absolute()
    root = f'{current_directory.parent.name}.{current_directory.name}'
    for path in current_directory.iterdir():
        if path.name.startswith('parser_'):
            module = importlib.import_module(f'.{path.stem}', package=root)
            for name, member in inspect.getmembers(module):
                if hasattr(member, 'field'):
                    if inspect.isfunction(member):
                        available_parsers[member.field] = member
                    if inspect.isclass(member):
                        available_parsers[member.field] = member().parse
    return available_parsers


def run_parser(parser_name, raw_data):
    parsers = get_available_parsers()
    if parser_name not in parsers:
        raise NameError(f'No parser named {parser_name}. Make sure it exists in parsers package.')
    return parser_name[parser_name](raw_data)
