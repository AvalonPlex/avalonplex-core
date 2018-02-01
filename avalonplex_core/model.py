from datetime import date, datetime
from typing import Optional, List, Dict, Any, Tuple
from xml.etree.ElementTree import Element, SubElement


class Model:
    def __init__(self, root: str):
        self._root = root  # type: str

    def __repr__(self):
        values = ", ".join([f"{attr}={value}" for attr, value in self._get_attributes().items()])
        return f"{self.__class__}({values})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _get_attributes(self) -> Dict[str, Any]:
        mapping = self._mapping()
        attributes_map = {}
        attributes = [name for name in dir(self) if not name.startswith("_")]
        for attribute in attributes:
            value = getattr(self, attribute)
            if not callable(value):
                name = attribute
                if name in mapping:
                    name = mapping[name]
                attributes_map[name] = value
        return attributes_map

    @staticmethod
    def _mapping() -> Dict[str, str]:
        return {}

    def _get_attribute_order(self, attr: Tuple[str, Any]) -> int:
        order_list = self._get_attribute_order_list()
        if order_list is None:
            return -1
        try:
            return order_list.index(attr[0])
        except ValueError:
            return -1

    @staticmethod
    def _get_attribute_order_list() -> Optional[List[str]]:
        return None

    def as_element(self, ignore_none: bool = True, ignore_empty: bool = True, ignore_blank: bool = True,
                   trim: bool = True) -> Element:
        element = Element(self._root)
        attributes = [(tag, value) for tag, value in self._get_attributes().items()]
        attributes.sort(key=self._get_attribute_order)
        for tag, value in attributes:
            self._insert_sub_element(element, tag, value, ignore_none, ignore_empty, ignore_blank, trim)
        return element

    def _insert_sub_element(self, parent: Element, tag: str, value: Any, ignore_none: bool, ignore_empty: bool,
                            ignore_blank: bool, trim: bool):
        if ignore_none and value is None:
            return
        if isinstance(value, date):
            str_value = value.strftime("%Y-%m-%d")
        elif isinstance(value, list):
            for sub_value in value:
                self._insert_sub_element(parent, tag, sub_value, ignore_none, ignore_empty, ignore_blank, trim)
            return
        elif isinstance(value, Model):
            parent.append(value.as_element(ignore_none, ignore_empty, ignore_blank, trim))
            return
        else:
            str_value = str(value) if value is not None else ""
        if trim:
            str_value = str_value.strip()
        if ignore_blank and str_value.isspace():
            return
        if ignore_empty and len(str_value) == 0:
            return
        SubElement(parent, tag).text = str_value


class Episode(Model):
    def __init__(self, title: Optional[str] = None, episode: Optional[int] = None, aired: Optional[date] = None,
                 mpaa: Optional[str] = None, plot: Optional[str] = None, directors: Optional[List[str]] = None,
                 writers: Optional[List[str]] = None, rating: Optional[float] = None):
        super().__init__("episodedetails")
        self.title = title  # type: Optional[str]
        self.episode = episode  # type: Optional[int]
        self.aired = aired  # type: Optional[date]
        self.mpaa = mpaa  # type: Optional[str]
        self.plot = plot  # type: Optional[str]
        self.directors = directors if directors is not None else []  # type: List[str]
        self.writers = writers if writers is not None else []  # type: List[str]
        self.rating = rating  # type: Optional[float]

    @staticmethod
    def _mapping() -> Dict[str, str]:
        return {"directors": "director", "writers": "writer"}

    @staticmethod
    def _get_attribute_order_list() -> Optional[List[str]]:
        return ["title", "episode", "aired", "mpaa", "plot", "director", "writer", "rating"]

    @staticmethod
    def from_xml(root: Element) -> "Episode":
        episode = Episode()
        mapping = Episode._mapping()
        for attr in Episode._get_attribute_order_list():
            attr_key = attr
            for key, value in mapping.items():
                if value == attr:
                    attr_key = key
                    break
            elements = root.findall(attr)  # type: List[Element]
            if len(elements) == 0:
                continue
            try:
                if attr_key == "rating":
                    setattr(episode, attr_key, float(elements[0].text))
                elif attr_key == "episode":
                    setattr(episode, attr_key, int(elements[0].text))
                elif attr_key in ["directors", "writers"]:
                    setattr(episode, attr_key, [e.text for e in elements])
                elif attr_key == "aired":
                    setattr(episode, attr_key, datetime.strptime(elements[0].text, "%Y-%m-%d").date())
                else:
                    setattr(episode, attr_key, elements[0].text)
            except TypeError:
                pass
        return episode


class Actor(Model):
    def __init__(self, name: Optional[str] = None, role: Optional[str] = None, thumb: Optional[str] = None):
        super().__init__("actor")
        self.name = name  # type: Optional[str]
        self.role = role  # type: Optional[str]
        self.thumb = thumb  # type: Optional[str]

    @staticmethod
    def _get_attribute_order_list() -> Optional[List[str]]:
        return ["name", "role", "thumb"]

    @staticmethod
    def from_xml(root: Element) -> "Actor":
        actor = Actor()
        mapping = Actor._mapping()
        for attr in Actor._get_attribute_order_list():
            attr_key = attr
            for key, value in mapping.items():
                if value == attr:
                    attr_key = key
                    break
            elements = root.findall(attr)  # type: List[Element]
            if len(elements) == 0:
                continue
            setattr(actor, attr_key, elements[0].text)
        return actor


class Show(Model):
    def __init__(self, title: Optional[str] = None, original_title: Optional[str] = None,
                 sort_title: Optional[str] = None, sets: Optional[List[str]] = None, mpaa: Optional[str] = None,
                 plot: Optional[str] = None, tag_line: Optional[str] = None, rating: Optional[float] = None,
                 premiered: Optional[date] = None, studio: Optional[str] = None, genres: Optional[List[str]] = None,
                 actors: Optional[List[Actor]] = None):
        super().__init__("tvshow")
        self.title = title  # type: Optional[str]
        self.original_title = original_title  # type: Optional[str]
        self.sort_title = sort_title  # type: Optional[str]
        self.sets = sets if sets is not None else []  # type: List[str]
        self.mpaa = mpaa  # type: Optional[str]
        self.plot = plot  # type: Optional[str]
        self.tag_line = tag_line  # type: Optional[str]
        self.rating = rating  # type: Optional[float]
        self.premiered = premiered  # type: Optional[date]
        self.studio = studio  # type: Optional[str]
        self.genres = genres if genres is not None else []  # type: List[str]
        self.actors = actors if actors is not None else []  # type: List[Actor]

    @staticmethod
    def _mapping() -> Dict[str, str]:
        return {"original_title": "originaltitle", "sort_title": "sorttitle", "sets": "set", "tag_line": "tagline",
                "genres": "genre", "actors": "actor"}

    @staticmethod
    def _get_attribute_order_list() -> Optional[List[str]]:
        return ["title", "originaltitle", "sorttitle", "set", "mpaa", "plot", "tagline", "rating", "premiered",
                "studio", "genre", "actor"]

    @staticmethod
    def from_xml(root: Element) -> "Show":
        show = Show()
        mapping = Show._mapping()
        for attr in Show._get_attribute_order_list():
            attr_key = attr
            for key, value in mapping.items():
                if value == attr:
                    attr_key = key
                    break
            elements = root.findall(attr)  # type: List[Element]
            if len(elements) == 0:
                continue
            try:
                if attr_key == "rating":
                    setattr(show, attr_key, float(elements[0].text))
                elif attr_key in ["sets", "genres"]:
                    setattr(show, attr_key, [e.text for e in elements])
                elif attr_key == "actors":
                    setattr(show, attr_key, [Actor.from_xml(e) for e in elements])
                elif attr_key == "premiered":
                    setattr(show, attr_key, datetime.strptime(elements[0].text, "%Y-%m-%d").date())
                else:
                    setattr(show, attr_key, elements[0].text)
            except TypeError:
                pass
        return show


class Movie(Model):
    def __init__(self, title: Optional[str] = None, original_title: Optional[str] = None,
                 sort_title: Optional[str] = None, sets: Optional[List[str]] = None, mpaa: Optional[str] = None,
                 plot: Optional[str] = None, tag_line: Optional[str] = None, rating: Optional[float] = None,
                 release_date: Optional[date] = None, studio: Optional[str] = None,
                 directors: Optional[List[str]] = None, writers: Optional[List[str]] = None,
                 genres: Optional[List[str]] = None, actors: Optional[List[Actor]] = None):
        super().__init__("movie")
        self.title = title  # type: Optional[str]
        self.original_title = original_title  # type: Optional[str]
        self.sort_title = sort_title  # type: Optional[str]
        self.sets = sets if sets is not None else []  # type: List[str]
        self.mpaa = mpaa  # type: Optional[str]
        self.plot = plot  # type: Optional[str]
        self.tag_line = tag_line  # type: Optional[str]
        self.rating = rating  # type: Optional[float]
        self.release_date = release_date  # type: Optional[date]
        self.studio = studio  # type: Optional[str]
        self.directors = directors if directors is not None else []  # type: List[str]
        self.writers = writers if writers is not None else []  # type: List[str]
        self.genres = genres if genres is not None else []  # type: List[str]
        self.actors = actors if actors is not None else []  # type: List[Actor]

    @staticmethod
    def _mapping() -> Dict[str, str]:
        return {"original_title": "originaltitle", "sort_title": "sorttitle", "sets": "set",
                "release_date": "releasedate", "tag_line": "tagline", "directors": "director", "writers": "writer",
                "genres": "genre", "actors": "actor"}

    @staticmethod
    def _get_attribute_order_list() -> Optional[List[str]]:
        return ["title", "originaltitle", "sorttitle", "set", "mpaa", "plot", "tagline", "rating", "releasedate",
                "studio", "director", "writer", "genre", "actor"]

    @staticmethod
    def from_xml(root: Element) -> "Movie":
        movie = Movie()
        mapping = Movie._mapping()
        for attr in Movie._get_attribute_order_list():
            attr_key = attr
            for key, value in mapping.items():
                if value == attr:
                    attr_key = key
                    break
            elements = root.findall(attr)  # type: List[Element]
            if len(elements) == 0:
                continue
            try:
                if attr_key == "rating":
                    setattr(movie, attr_key, float(elements[0].text))
                elif attr_key in ["sets", "genres", "directors", "writers"]:
                    setattr(movie, attr_key, [e.text for e in elements])
                elif attr_key == "actors":
                    setattr(movie, attr_key, [Actor.from_xml(e) for e in elements])
                elif attr_key == "release_date":
                    setattr(movie, attr_key, datetime.strptime(elements[0].text, "%Y-%m-%d").date())
                else:
                    setattr(movie, attr_key, elements[0].text)
            except TypeError:
                pass
        return movie


__all__ = [Model, Episode, Show, Movie, Actor]
