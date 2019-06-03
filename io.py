import msgpack
import msgpack_numpy as m


def to_mpack(data, fname):
    packer = msgpack.Packer(default=m.encode)
    with open(fname, "wb") as file:
        file.write(packer.pack(data))


def load_mpack(fname):
    return msgpack.unpack(open(fname, "rb"), object_hook=m.decode)


def mpack_loader(fname):
    return msgpack.Unpacker(open(fname, "rb"), object_hook=m.decode)
