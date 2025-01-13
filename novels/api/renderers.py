import base64
from rest_framework.renderers import BaseRenderer
from proto import novels_pb2, noveldetails_pb2, chapterlist_pb2, chapterdetail_pb2

class ProtobufRenderer(BaseRenderer):
    """
    A custom renderer that serializes data to Protobuf format.
    """
    media_type = 'application/x-protobuf'
    format = 'proto'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        # Dynamically check if data is an instance of any Protobuf class
        protobuf_types = [novels_pb2.NovelList, noveldetails_pb2.NovelDetails, chapterlist_pb2.ChaptersList, chapterdetail_pb2.ChapterDetails] 

        # Check if the data is already a Protobuf object
        if isinstance(data, tuple(protobuf_types)):
            # return data.SerializeToString()
            serialized_data = data.SerializeToString()
            # Base64 encode the serialized data to make it less human-readable
            encoded_data = base64.b64encode(serialized_data).decode('utf-8')
            return encoded_data.encode('utf-8')  # Return Base64 encoded string as bytes

        raise TypeError("Data must be a Protobuf message object, not a {0}".format(type(data)))
