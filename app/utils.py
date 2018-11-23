import xml.etree.ElementTree as ET


def cdata(text=None):
    element = etree.Element('CDATA')
    element.text = text
    return element


etree = ET
etree._original_serialize_xml = etree._serialize_xml


def _serialize_xml(write, elem, qnames, namespaces,
                   short_empty_elements, **kwargs):
    if elem.tag == 'CDATA':
        write("<![CDATA[%s]]>" %
              elem.text)
        return

    return etree._original_serialize_xml(write, elem, qnames, namespaces,
                                         short_empty_elements, **kwargs)


def __etree_to_dict(elem):
    if len(elem) != 0:
        d = {}

        for e in list(elem):
            k, v = __etree_to_dict(e)
            d[k] = v
            if (k == "CDATA"):
                return (elem.tag, v)
        return (elem.tag, d)
    else:
        return (elem.tag, elem.text)


def etree_to_dict(elem):
    return __etree_to_dict(elem)[1]


etree._serialize_xml = etree._serialize['xml'] = _serialize_xml
