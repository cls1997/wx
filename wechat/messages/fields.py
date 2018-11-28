from .utils import cdata, etree


class Field:
    converter = None

    def __init__(self, name, is_cdata, **args):
        self.name = name
        self.is_cdata = is_cdata

    def __str__(self):
        return "<%s : CDATA: %s>" % (self.name, self.is_cdata)

    def get_element(self, data):
        raise NotImplementedError()


class IntegerField(Field):
    converter = int

    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, data):
        elem = etree.Element(self.name)
        elem.text = str(data)
        return elem


class FloatField(Field):
    converter = float

    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, data):
        elem = etree.Element(self.name)
        elem.text = str(data)
        return elem


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, True)

    def get_element(self, data):
        elem = etree.Element(self.name)
        elem.append(cdata(data))
        return elem


class ImageField(Field):
    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, data):
        image = etree.Element("Image")
        elem = etree.Element(self.name)
        elem.append(cdata(data))
        image.append(elem)
        return image


class VoiceField(Field):
    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, data):
        voice = etree.Element("Voice")
        elem = etree.Element(self.name)
        elem.append(cdata(data))
        voice.append(elem)
        return voice


class VideoField(Field):
    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, data):
        video = etree.Element("Video")
        elem = etree.Element(self.name)
        elem.append(cdata(data))
        video.append(elem)
        return video
