#downloaded from:
# https://github.com/IfcOpenShell/IfcOpenShell/blob/d01b89473416d1e5922f4e12ccbd818801a74545/src/ifcopenshell-python/ifcopenshell/guid.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid
import string

from functools import reduce

chars = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_$'


def compress(g):
    bs = [int(g[i:i + 2], 16) for i in range(0, len(g), 2)]

    def b64(v, l=4):
        return ''.join([chars[(v // (64 ** i)) % 64] for i in range(l)][::-1])

    return ''.join([b64(bs[0], 2)] + [b64((bs[i] << 16) + (bs[i + 1] << 8) + bs[i + 2]) for i in range(1, 16, 3)])


def expand(g):
    def b64(v):
        return reduce(lambda a, b: a * 64 + b, map(lambda c: chars.index(c), v))

    bs = [b64(g[0:2])]
    for i in range(5):
        d = b64(g[2 + 4 * i:6 + 4 * i])
        bs += [(d >> (8 * (2 - j))) % 256 for j in range(3)]
    return ''.join(['%02x' % b for b in bs])


def split(g):
    return '{%s-%s-%s-%s-%s}' % (g[:8], g[8:12], g[12:16], g[16:20], g[20:])


def new():
    return compress(uuid.uuid4().hex)

