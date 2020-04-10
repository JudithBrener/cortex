import gzip
from pathlib import Path


def upload_sample(host, port, path):
    open_file(path)


def open_file(path):
    if path.endswith('.gz'):
        return gzip.GzipFile(path, mode='rb')
    return Path(path).open('rb')
