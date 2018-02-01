from xml import etree
# noinspection PyProtectedMember
from xml.etree.ElementTree import Element, Comment, ProcessingInstruction, _escape_cdata, \
    _escape_attrib, QName

from avalonplex_core.model import Model, Episode, Show, Movie, Actor
from avalonplex_core.normalize import normalize
from avalonplex_core.serialize import XmlSerializer

__all__ = [Model, Episode, Show, Movie, Actor, normalize, XmlSerializer]


# ============================  Hack Start  ============================

def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements, addintend="    ", intend="", newl="\n",
                   **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is Comment:
        write(intend + "<!--%s-->" % text)
    elif tag is ProcessingInstruction:
        write(intend + "<?%s?>" % text)
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_xml(write, e, qnames, None, addintend=addintend, intend=addintend + intend, newl=newl,
                               short_empty_elements=short_empty_elements)
        else:
            write(intend + "<" + tag)
            items = list(elem.items())
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(),
                                       key=lambda x: x[1]):  # sort on prefix
                        if k:
                            k = ":" + k
                        write(" xmlns%s=\"%s\"" % (
                            k,
                            _escape_attrib(v)
                        ))
                for k, v in sorted(items):  # lexical order
                    if isinstance(k, QName):
                        k = k.text
                    if isinstance(v, QName):
                        v = qnames[v.text]
                    else:
                        v = _escape_attrib(v)
                    write(" %s=\"%s\"" % (qnames[k], v))
            if text or len(elem) or not short_empty_elements:
                write(">")
                if text is not None:
                    write(_escape_cdata(text))
                else:
                    if len(elem.getchildren()) > 0:
                        write(newl)
                for e in elem:
                    _serialize_xml(write, e, qnames, None, addintend=addintend, intend=addintend + intend, newl=newl,
                                   short_empty_elements=short_empty_elements)
                if len(elem.getchildren()) > 0:
                    write(intend)
                write("</" + tag + ">" + newl)
            else:
                write(" />" + newl)
    if elem.tail:
        write(_escape_cdata(elem.tail))


etree.ElementTree._serialize_xml = _serialize_xml
# noinspection PyProtectedMember
etree.ElementTree._serialize["xml"] = _serialize_xml

# ============================   Hack End   ============================
