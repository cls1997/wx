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


etree._serialize_xml = etree._serialize['xml'] = _serialize_xml


def parse_wechat_message(xml):
    return etree.fromstring(xml)


def build_wechat_message(root):
    tree =  etree.ElementTree(root)
    return etree.tostring(root)
