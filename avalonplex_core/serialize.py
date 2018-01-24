from os.path import join
from typing import Union
from xml.etree.ElementTree import Element, ElementTree, parse

from avalonplex_core.model import Model, Episode, Show, Movie


class XmlSerializer:
    def __init__(self, encoding: str = "utf-8", short_empty_elements: bool = False, ignore_none: bool = True,
                 ignore_empty: bool = True, ignore_blank: bool = True, trim: bool = True):
        self.encoding = encoding  # type: str
        self.short_empty_elements = short_empty_elements  # type: bool
        self.ignore_none = ignore_none  # type: bool
        self.ignore_empty = ignore_empty  # type: bool
        self.ignore_blank = ignore_blank  # type: bool
        self.trim = trim  # type: bool

    def serialize(self, model: Model, name: str, folder: str = ""):
        root = model.as_element(self.ignore_none, self.ignore_empty, self.ignore_blank, self.trim)  # type: Element
        tree = ElementTree(element=root)  # type: ElementTree
        tree.write(join(folder, name), encoding=self.encoding, short_empty_elements=self.short_empty_elements)

    def deserialize(self, path: str) -> Union[Episode, Show, Movie]:
        root = parse(path).getroot()  # type: Element
        if root.tag == "episodedetails":
            return Episode.from_xml(root)
        elif root.tag == "tvshow":
            return Show.from_xml(root)
        elif root.tag == "movie":
            return Movie.from_xml(root)
        else:
            raise NotImplementedError(f"Not supported root tag: {root.tag}")
