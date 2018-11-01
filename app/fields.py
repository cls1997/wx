from app.utils import cdata, etree

class Field:
    def __init__(self, name, is_cdata, **args):
        self.name = name
        self.is_cdata = is_cdata

    def __str__(self):
        return "<%s : CDATA: %s>" % (self.name, self.is_cdata)
    
    def get_element(self):
        raise NotImplementedError()


class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, False)

    def get_element(self, text):
        elem = etree.Element(self.name)
        elem.text = str(text)
        return elem


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, True)
    
    def get_element(self,text):
        elem = etree.Element(self.name)
        elem.append(cdata(text))
        return elem
