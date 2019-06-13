import msgpack
import msgpack_numpy as m
from core import run_shell
import os
import tensorflow as tf

def to_mpack(data, fname):
    packer = msgpack.Packer(default=m.encode)
    with open(fname, "wb") as file:
        file.write(packer.pack(data))


def load_mpack(fname):
    return msgpack.unpack(open(fname, "rb"), object_hook=m.decode)


def mpack_loader(fname):
    return msgpack.Unpacker(open(fname, "rb"), object_hook=m.decode)


# save/load from buckets
def is_exist_in_bucket(*fnames):
    fname = os.path.join(*fnames)
    res = run_shell("gsutil -q stat {}".format(fname))
    return res.returncode == 0


def save_to_bucket(bucket_directory, fname):
  tf.gfile.MakeDirs(bucket_directory)
  bucket_fname = os.path.join(bucket_directory, fname)
  run_shell("gsutil cp {} {}".format(fname, bucket_fname))


def load_from_bucket(bucket_directory, fname):
  bucket_fname = os.path.join(bucket_directory, fname)
  run_shell("gsutil cp {} {}".format(bucket_fname,fname))


def load_or_execute(bucket_directory, fname, func, force_execution = False, load=True):
    if force_execution or not is_exist_in_bucket(bucket_directory, fname):
        print("file {} doesn't exist in {}. execute function...".format(fname, bucket_directory))
        func()
        save_to_bucket(bucket_directory, fname)
    else:
        if load:
            print("file {} exist in {}. load file...".format(fname, bucket_directory))
            load_from_bucket(bucket_directory, fname)


def bucket_dir(bucket_name, *dir_names):
    bucket_name = 'gs://{}'.format(bucket_name)
    dir_name =  os.path.join(*dir_names)
    return os.path.join(bucket_name, dir_name)