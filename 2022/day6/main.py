from sys import stdin
from itertools import islice

def sliding_windows(items, size):
    """ Generates sliding windows of length `size` from `items`.

    Example:
    > sliding_windows([1,2,3,4,5], 3)
    ((1,2,3), (2,3,4), (3,4,5))
    """
    iters = (islice(iter(items), i, None) for i in range(size))
    yield from zip(*iters)

def are_all_distinct(items):
    """ Returns True if all items are different. """
    return len(items) == len(set(items))

def find_index(predicate, items):
    """ Finds the first index in `items` where `predicate` is True. """
    for i, item in enumerate(items):
        if predicate(item):
            return i

def find_start_of_marker(datastream, marker_size):
    """ Finds the first index in the datastream following `marker_size` distinct characters. """
    windows = sliding_windows(datastream, marker_size)
    index = find_index(are_all_distinct, windows)
    return (index + marker_size) if index is not None else None

datastream = stdin.read().strip()

# Part 1
START_OF_PACKET_MARKER_SIZE = 4
print(find_start_of_marker(datastream, START_OF_PACKET_MARKER_SIZE))

# Part 2
START_OF_MESSAGE_MARKER_SIZE = 14
print(find_start_of_marker(datastream, START_OF_MESSAGE_MARKER_SIZE))
