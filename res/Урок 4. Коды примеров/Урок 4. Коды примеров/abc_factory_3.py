import abc

# Семейство классов для VK
class VkParser:
    def parse(self):
        print('Vk parser work')

class VkAnalizer:
    pass

class VkSender:
    pass

# Семейство классов для одноклассников
class OdParser:
    def parse(self):
        print('Od parser work')

class OdAnalizer:
    pass

class OdSender:
    pass

# Семейство классов для твиттера
class TwParser:
    def parse(self):
        print('Tw parser work')

class TwAnalizer:
    pass

class TwSender:
    pass


class AbstractFactory(abc.ABC):

    @staticmethod
    def create_factory(network_name):
        NETWORKS = {
            'Vk': VkFactory,
            'Od': OdFactory,
            'Tw': TwFactory
        }

        return NETWORKS[network_name]()



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

class TwFactory(AbstractFactory):
    def create_parser(self):
        return TwParser()

    def create_analizer(self):
        return TwAnalizer()

    def create_sender(self):
        return TwSender()


# from abc_factory_3 import AbstractFactory

factory = AbstractFactory.create_factory('Od')


parser = factory.create_parser()
analizer = factory.create_analizer()
sender = factory.create_sender()

parser.parse()
