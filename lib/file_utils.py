from math import log

_suffixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

# Bytes to human-readable representation
def pp_file_size(size: int) -> str:
    order = int(log(size, 2) / 10) if size else 0
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])
