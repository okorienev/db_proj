def serialize(o: object, strategy: str):
    """
    static method to serialize object into bytes
    :param o: object to serialize
    :param strategy: type of serializable object e.g. "img", "str", "txt", "num"
    :return: bytes
    """
    # choose from concrete serializer and serialize
    pass


def deserialize(dump: bytes, strategy: str):
    """
    :param dump: bytes to deserialize
    :param strategy: type of serializable object e.g. "img", "str", "txt", "num"
    :return: object
    """
    # choose from concrete serializer and deserialize
    pass
