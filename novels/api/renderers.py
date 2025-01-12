from rest_framework.renderers import BaseRenderer
from proto import novels_pb2  # Ensure this imports the correct generated Protobuf file

class ProtobufRenderer(BaseRenderer):
    """
    A custom renderer that serializes data to Protobuf format.
    """
    media_type = 'application/x-protobuf'
    format = 'proto'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''

        # Check if the data is already a Protobuf object
        if isinstance(data, novels_pb2.NovelList):
            return data.SerializeToString()
        
        # If the data is not a Protobuf object, raise an error
        raise TypeError("Data must be a Protobuf message object, not a {0}".format(type(data)))
