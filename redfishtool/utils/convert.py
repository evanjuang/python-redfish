
def remove_hex_prefix(hex_str):
    if not hex_str:
        return ''

    res = hex_str

    if hex_str.startswith('0x'):
        res = hex_str[2:]

    return res.zfill(4)


def bytes_to_readable_size(num_of_bytes, base=2, unit=False):
    unit_10 = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_2 = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']

    size_base = 1000 if base == 10 else 1024
    suffixes = unit_10 if base == 10 else unit_2

    if num_of_bytes is None or (not isinstance(num_of_bytes, int)):
        return ''

    i = 0
    while num_of_bytes >= size_base and i < len(suffixes) - 1:
        num_of_bytes /= size_base
        i += 1
    f = ('%.2f' % num_of_bytes).rstrip('0').rstrip('.')

    if unit:
        return '%s %s' % (f, suffixes[i])
    else:
        return f


def mib_to_gib(size_in_mib):
    if isinstance(size_in_mib, int):
        return bytes_to_readable_size(size_in_mib * 1024 * 1024)
    return 0


def mib_to_byte(size_in_mib):
    if isinstance(size_in_mib, int):
        return size_in_mib * 1024 * 1024
    return 0
