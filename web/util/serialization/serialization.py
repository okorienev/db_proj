STR_LIMIT = 64
STR_ENCODING = 'utf_8'


def serialize(o: object, strategy: str):
    """
    static method to serialize object into bytes
    :param o: object to serialize
    :param strategy: type of serializable object e.g. "img", "str", "txt", "num"
    :return: bytes
    """

    if strategy == 'img':
        import base64
        return base64.b64encode(o)
    elif strategy == 'str':
        if len(o) >= STR_LIMIT:
            raise ValueError(f'str larger than {STR_LIMIT}')
        return o.encode(STR_ENCODING)
    elif strategy == 'txt':
        return o.encode(STR_ENCODING)
    elif strategy == 'num':
        return str(o).encode(STR_ENCODING)

def deserialize(dump: bytes, strategy: str):
    """
    :param dump: bytes to deserialize
    :param strategy: type of serializable object e.g. "img", "str", "txt", "num"
    :return: object
    """

    if strategy == 'img':
        import base64
        return base64.b64decode(dump)
    elif strategy in ('str', 'txt'):
        return dump.decode(STR_ENCODING)
    elif strategy == 'num':
        return int(dump.decode(STR_ENCODING))

