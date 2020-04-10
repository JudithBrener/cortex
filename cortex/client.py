import gzip
import traceback
from pathlib import Path

from cortex.uploader import Upload
from cortex.reader import Reader


def upload_sample(host, port, path):
    """"
    a client which streams cognition snapshots to a server
    :param host: host of the server.
    :param port: port of the server.
    :param path: path to the file.
    """
    cortex_file = open_file(path)
    try:
        reader = Reader(cortex_file)
        user = reader.user

        uploader = Upload(host, port, user)
        for snapshot in reader:
            uploader.upload(snapshot)
    except FileNotFoundError:
        print(f'FileNotFoundError - upload failed')
    except Exception as error:
        print(f'ERROR: {error} - upload failed')
        print(traceback.format_exc())
        return 1


def open_file(path):
    if path.endswith('.gz'):
        return gzip.GzipFile(path, mode='rb')
    return Path(path).open('rb')
