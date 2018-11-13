import abc


class AbstractSerializer:
    """
    abstract class to declare serializers interface
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def serialize(self, o: object, strategy: str) -> bytes:
        """
        :param o: object to serialize
        :param strategy: type of object e.g. "str", "img", "txt", "num"
        :return: bytes which represent the given object
        """
        pass

    @abc.abstractmethod
    def deserialize(self, dump: bytes, strategy: str) -> object:
        """
        :param dump: bytes to deserialize
        :param strategy: type of object e.g. "str", "img", "txt", "num"
        :return: object loaded from given bytes
        """
        pass
