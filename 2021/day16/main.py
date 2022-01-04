from sys import stdin
from math import prod
from operator import gt, lt, eq

lines = [line.strip() for line in stdin.readlines()]
transmission = lines[0]

def hex_to_bin(hex_string):
    value = int(hex_string, 16)
    bits = bin(value)[2:]
    padded = bits.zfill(len(hex_string) * 4)
    return (bit for bit in padded)

def consume_bits(bits, n):
    return (next(bits) for _ in range(n))

def read_int(bits, n):
    binary_string = ''.join(consume_bits(bits, n))
    return int(binary_string, 2)

def consume_subpackets_by_size(bits, size):
    subpackets = consume_bits(bits, size)
    packets = []

    try:
        while True:
            packet = parse_packet(subpackets)
            packets.append(packet)
    except StopIteration:
        # Forgive me for using exceptions as control flow.
        # Python generators are... lacking
        pass
    finally:
        return packets

def consume_subpackets_by_count(bits, count):
    packets = []

    for _ in range(count):
        packet = parse_packet(bits)
        packets.append(packet)

    return packets

def read_operator(bits):
    length_type = read_int(bits, 1)

    if length_type == 0:
        size = read_int(bits, 15)
        return consume_subpackets_by_size(bits, size)
    else:
        count = read_int(bits, 11)
        return consume_subpackets_by_count(bits, count)

def read_literal(bits):
    prefix, literal = 1, 0

    while prefix == 1:
        prefix = read_int(bits, 1)
        value = read_int(bits, 4)

        literal = literal << 4
        literal += value

    return literal

OPERATOR_MAP = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda packets: int(gt(*packets)),
    6: lambda packets: int(lt(*packets)),
    7: lambda packets: int(eq(*packets)),
}

def parse_packet(packet):
    version = read_int(packet, 3)
    type_id = read_int(packet, 3)

    node = {
        'version': version,
        'type': type_id,
        'children': []
    }

    if type_id == 4:
        literal = read_literal(packet)
        node['kind'] = 'literal'
        node['value'] = literal
        return node

    subpackets = read_operator(packet)
    node['kind'] = 'operator'
    node['children'] = subpackets
    node['operator'] = OPERATOR_MAP[type_id]
    return node

def version_sum(tree):
    version = tree['version']
    subpackets = tree['children']
    return version + sum(map(version_sum, subpackets))

def evaluate(tree):
    kind = tree['kind']

    if kind == 'literal':
        return tree['value']

    operator = tree['operator']
    children = map(evaluate, tree['children'])
    return operator(children)

tree = parse_packet(hex_to_bin(transmission))
print(version_sum(tree))
print(evaluate(tree))
