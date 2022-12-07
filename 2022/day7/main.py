from sys import stdin
from typing import Optional, NamedTuple, Iterable

class File(NamedTuple):
    name: str
    size: int
    parent: 'Directory'

class Directory(NamedTuple):
    name: str
    parent: Optional['Directory']
    subdirectories: list['Directory']
    files: list[File]

    def get_directory(self: 'Directory', name: str) -> Optional['Directory']:
        for directory in self.subdirectories:
            if directory.name == name:
                return directory

    def get_file(self: 'Directory', name: str) -> Optional[File]:
        for file in self.files:
            if file.name == name:
                return file

    def get_root(self: 'Directory') -> 'Directory':
        if self.parent is None:
            return self
        return self.parent.get_root()

    def get_size(self: 'Directory') -> int:
        children = sum(sub.size for sub in self.subdirectories)
        files = sum(file.size for file in self.files)
        return children + files

    size = property(get_size)

    def create_directory(self: 'Directory', name: str) -> 'Directory':
        """ Creates a subdirectory called `name`.

            If `name` already exists as a directory, returns the existing directory.

            If `name` already exists as a file, raises an error.
        """
        if self.get_file(name) is not None:
            raise Exception(f'A file with the name "{name}" exists in the {self.name} directory. Can not create a directory with that name.')

        subdirectory = self.get_directory(name)

        if subdirectory is None:
            subdirectory = Directory(name=name, parent=self, subdirectories=[], files=[])
            self.subdirectories.append(subdirectory)

        return subdirectory

    def create_file(self: 'Directory', name: str, size: int) -> File:
        """ Creates a file called `name`, with size `size` bytes.

            If `name` already exists as a file or directory, raises an error.
        """

        if self.get_file(name) is not None:
            raise Exception(f'A file with the name "{name}" exists in the {self.name} directory. Can not create a new file with that name.')

        if self.get_directory(name) is not None:
            raise Exception(f'A directory with the name "{name}" exists in the {self.name} directory. Can not create a new file with that name.')

        file = File(name=name, size=size, parent=self)
        self.files.append(file)

        return file

def parse_log(log: list[str]) -> Directory:
    root: Directory = Directory(name='/', parent=None, subdirectories=[], files=[])
    cwd: Directory= root # Current working directory

    command, output = None, []
    is_command = lambda line: line[0] == '$'

    for line in log:
        # If we're not dealing with a new command, we're dealing with output
        # for the previous command
        if not is_command(line):
            output.append(line)
            continue

        # Before parsing the new command, parse the previous command with
        # the aggregated output
        if command is not None:
            cwd = parse_command(cwd, command, output)

        # Reset things for the new command
        command, output = line[1:].split(), []

    # Parse any outstanding command at the end
    if command is not None:
        parse_command(cwd, command, output)

    return root

def cd_command(cwd: Directory, args: list[str]) -> Directory:
    destination = args[0]

    if destination == '..':
        if cwd.parent is None:
            raise Exception('The root directory does not have a parent to `cd` to.')
        return cwd.parent

    if destination == '/':
        return cwd.get_root()

    directory = cwd.create_directory(destination)
    return directory

def ls_command(cwd: Directory, output: list[str]) -> Directory:
    for line in output:
        components = line.split()

        # Every output line should have 2 components
        if len(components) != 2:
            raise Exception(f'Unsure how to parse the output line "{line}" from the `ls` command.')

        if components[0] == 'dir':
            name = components[1]
            cwd.create_directory(name)
            continue

        if components[0].isnumeric():
            size, name = int(components[0]), components[1]
            cwd.create_file(name, size)

    return cwd

def parse_command(cwd: Directory, components: list[str], output: list[str]) -> Directory:
    command, args = components[0], components[1:]

    if command == 'cd':
        return cd_command(cwd, args)

    if command == 'ls':
        return ls_command(cwd, output)

    raise Exception(f'Unknown command "${command}" with args "${args}"')

def all_directories(root: Directory) -> Iterable[Directory]:
    yield root
    for subdirectory in root.subdirectories:
        yield from all_directories(subdirectory)

loglines = stdin.read().splitlines()
root = parse_log(loglines)

# Part 1
MAX_DIR_SIZE = 100000
print(sum(directory.size for directory in all_directories(root) if directory.size <= MAX_DIR_SIZE))

# Part 2
TOTAL_DISK_CAPACITY = 70000000
MINIMUM_REQUIRED_UPDATE_SPACE = 30000000

available_disk_space = TOTAL_DISK_CAPACITY - root.size
meets_space_requirements = lambda directory: directory.size + available_disk_space >= MINIMUM_REQUIRED_UPDATE_SPACE
candidates = filter(meets_space_requirements, all_directories(root))
winner = min(candidates, key=lambda directory: directory.size)
print(winner.size)
