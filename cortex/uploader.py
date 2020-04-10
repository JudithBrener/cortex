from bson import dumps
import requests
from google.protobuf.json_format import MessageToDict


class Upload:
    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user

    def upload(self, snapshot):
        """
        Upload received snapshot as BSON to the server
        :param snapshot: snapshot to upload.
        """
        server_url = f'http://{self.host}:{self.port}/snapshot'
        try:
            snapshot_dict = MessageToDict(snapshot, including_default_value_fields=True,
                                          preserving_proto_field_name=True)
            user_dict = MessageToDict(snapshot, including_default_value_fields=True, preserving_proto_field_name=True)
            snapshot_data = {'user': user_dict, 'snapshot': snapshot_dict}
            requests.put(server_url, data=dumps(snapshot_data))
        except ConnectionError:
            print(f'ConnectionError to {self.host}:{self.port} - upload failed')
        except Exception as error:
            print(f'ERROR: {error} - upload failed')
