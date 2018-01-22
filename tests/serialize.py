from datetime import date
from os import remove
from unittest import TestCase

from avalonplex_core.model import Episode, Show, Actor, Movie
from avalonplex_core.serialize import XmlSerializer

__all__ = ["TestSerialize", "TestDeserialize"]


class TestSerialize(TestCase):
    def test_serialize_episode(self):
        x = XmlSerializer()
        x.serialize(test_episode, "1.xml")

        with open("example/episode.xml", "r", encoding="utf-8") as example:
            data = example.read()
            with open("1.xml", "r", encoding="utf-8") as output:
                test_output = output.read()
                self.assertEqual(test_output, data)
            remove("1.xml")

    def test_serialize_show(self):
        x = XmlSerializer()
        x.serialize(test_show, "1.xml")

        with open("example/tvshow.xml", "r", encoding="utf-8") as example:
            data = example.read()
            with open("1.xml", "r", encoding="utf-8") as output:
                test_output = output.read()
                self.assertEqual(test_output, data)
            remove("1.xml")

    def test_serialize_movie(self):
        x = XmlSerializer()
        x.serialize(test_movie, "1.xml")

        with open("example/movie (2010).xml", "r", encoding="utf-8") as example:
            data = example.read()
            with open("1.xml", "r", encoding="utf-8") as output:
                test_output = output.read()
                self.assertEqual(test_output, data)
            remove("1.xml")


class TestDeserialize(TestCase):
    def test_deserialize_episode(self):
        x = XmlSerializer()
        self.assertEqual(x.deserialize("example/episode.xml"), test_episode)

    def test_deserialize_show(self):
        x = XmlSerializer()
        self.assertEqual(x.deserialize("example/tvshow.xml"), test_show)

    def test_deserialize_movie(self):
        x = XmlSerializer()
        self.assertEqual(x.deserialize("example/movie (2010).xml"), test_movie)


test_episode = Episode("赤い夜 ~ piros éjszaka", 1, date(2009, 10, 7), "TV-14",
                       "皐月駆は幼馴染の水奈瀬ゆかと平凡な生活を送っていた。辛い過去を背負う駆だが、クラスメイトの匡や香央里といった明るい二人と、やさしく接してくれるゆかとの学生生活を過ごしていた。\n\n"
                       "だが、ある日生まれつき見えない右目に激痛がはしったとたん、赤く染まる不気味な世界に迷い込むことに…。",
                       ["下田正美"], ["金巻兼一"], 5)

test_actor1 = Actor("小野大輔", "皐月駆", "https://example.com/cast/小野大輔.jpg")
test_actor2 = Actor("後藤麻衣", "水奈瀬ゆか", "https://example.com/cast/後藤麻衣.jpg")
test_show = Show("11eyes", "11eyes", "いれぶんあいず", ["11eyes -罪と罰と贖いの少女-"], "TV-14",
                 "平凡な生活を送っていた皐月駆だが、ある日幼なじみの水奈瀬ゆかと共に、突然不気味な異世界へ迷い込んでしまうことに…。\n\n"
                 "血の色にも似た不気味に赤く染まる空に、漆黒の巨大な月。そんな『赤い夜』の世界に、呆気にとられる駆とゆか…。\n\n"
                 "さらに、二人の周りに異形の怪物が現れ、襲いかかる。", "11eyes", 4.2, date(2009, 10, 6), "動画工房",
                 ["憂鬱", "ハーレム", "エロい", "現代ファンタジー", "アクション"], [test_actor1, test_actor2])

test_actor3 = Actor("諏訪部順一", "アーチャー", "https://example.com/cast/諏訪部順一.jpg")
test_actor4 = Actor("杉山紀彰", "衛宮士郎", "https://example.com/cast/杉山紀彰.jpg")
test_movie = Movie("Fate/stay night UNLIMITED BLADE WORKS", "Fate/stay night UNLIMITED BLADE WORKS",
                   "ふぇいと すていないと あんりみてっどぶれいどわーくす", ["Fate/stay night"], "PG12",
                   "街を焼き尽くす大災害が発生し、衛宮士郎は全てを失う。士郎は、魔術師を名乗る人物に引き取られる。それから10"
                   "年間、士郎は養父の想いを継いで、“正義の味方”になろうと魔術の鍛錬を重ねる。しかし魔術師の家系でないためその才能のない士郎は、1"
                   "つしか魔術を身につけることができなかった。ある日士郎は、“聖杯戦争”という魔術師同士の戦いに巻き込まれてしまう。"
                   "それは、手にした者の願いを叶えるという聖杯を巡る戦いだった。そして偶然、サーヴァントと呼ばれる使い魔の1人・セイバーと契約を交わす。"
                   "こうして意にそぐわないままマスターとなった士郎だったが、10年前の大災害も聖杯戦争が原因であると知ると、あの惨劇を繰り返さないために戦いに、身を投じる覚悟を決める。",
                   "我に従え―― ならばこの運命、汝が剣に預けよう", 6.8, date(2010, 1, 23), "スタジオディーン", ["山口祐司"], ["佐藤卓哉"],
                   ["魔法", "現代ファンタジー", "ファンタジー"], [test_actor3, test_actor4])
