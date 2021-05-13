import abc

# Семейство классов для VK
class VkParser:
    pass

class VkAnalizer:
    pass

class VkSender:
    pass

# Семейство классов для одноклассников
class OdParser:
    pass

class OdAnalizer:
    pass

class OdSender:
    pass


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def create_parser(self):
        pass

    @abc.abstractmethod
    def create_analizer(self):
        pass

    @abc.abstractmethod
    def create_sender(self):
        pass


class VkFactory(AbstractFactory):
    def create_parser(self):
        return VkParser()

    def create_analizer(self):
        return VkAnalizer()

    def create_sender(self):
        return VkSender()

class OdFactory(AbstractFactory):
    def create_parser(self):
        return OdParser()

    def create_analizer(self):
        return OdAnalizer()

    def create_sender(self):
        return OdSender()

