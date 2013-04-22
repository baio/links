# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from converters.contrib2gexf import parse_line


class TestContrib2Gexf(unittest.TestCase):

    def test_empty(self):
        with self.assertRaisesRegexp(ValueError, "STR_EMPTY"):
            parse_line(None, None)
        with self.assertRaisesRegexp(ValueError, "STR_EMPTY"):
            parse_line("", None)
        with self.assertRaisesRegexp(ValueError, "STR_EMPTY"):
            parse_line("      ", None)

    def test_total_mess(self):
        with self.assertRaisesRegexp(ValueError, "STR_FORMAT"):
            parse_line("totalmess:7893475290*&*)^*GOBGOIUGHU*Oy78oolglsih;ujwef\rndksf;bhdlhwefuhwiufylgdwkl;kkebjbjh", None)
        with self.assertRaisesRegexp(ValueError, "STR_FORMAT"):
            parse_line("totalmess:7893475290*&*)--^*GOBGOIUGHU*Oy78--oolglsih;ujwef\rndksf;bhdlhwefuhwiufylgdwkl;kkebjbjh", None)
        with self.assertRaisesRegexp(ValueError, "STR_FORMAT"):
            parse_line("totalmess:7893475290*&*)-^*GOBGOIUGHU*Oy78-o-olglsih;ujwef\rndksf;bhdlhwefuhwiufylgdwkl;kke-bjbjh\r\n", None)
        with self.assertRaisesRegexp(ValueError, "STR_FORMAT"):
            parse_line("totalmess:7893475290*&*)-^*GOBGOIUGHU*Oy78--oolglsih;ujwef\rndksf;bhdlhwefuhwiufylgdwkl;kkebjbjh", None)

    def test_entry_not_empty(self):
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба.http://goo.gl/ohEX4", None)
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-", None)
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "")
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба", None)
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба,dghjkk,fgdfg,", None)
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба,dghjkk,fgdfg", None)
        with self.assertRaisesRegexp(ValueError, "STR_ENTRY_EMPTY"):
            parse_line("елена скрынник-виктор христенко-брат.служба,,,,,", None)

    def test_name(self):
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("елена скрынник паррр-виктор христенко-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("елена скрынник-виктор христенко заррр-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("елена скрынник паррр-виктор христенко заррр-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("елена gogog-виктор христенко-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("елена gogog-aaff христенко-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("-aaff христенко-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line(" -aaff христенко-брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line("--брат.служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_NAME_FORMAT"):
            parse_line(" -    -брат.служба", "link")

    def test_tags(self):
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат?служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.,служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат...служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат,служба", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-8900999888рат^&*(&(*^*$^", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-РАТ.", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-БР АТ", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-.брат", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат..брат", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-..брат", "link")
        with self.assertRaisesRegexp(ValueError, "STR_TAG_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат..", "link")

    def test_link(self):
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "http://goo.gl/ohEX4?test=1")
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "http://goo.gl/ohEX4&yuiyuiyi")
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "http://goo/ohEX4&yuiyuiyi")
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "abcd.gl/ohEX4")
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "http://goo.gl/")
        with self.assertRaisesRegexp(ValueError, "STR_LINK_FORMAT"):
            parse_line("елена скрынник-виктор христенко-брат.служба", "http://docs.python.org/2/library/functions.html#filter")

    def test_format(self):

        buck = parse_line("елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4", None)
        self.assertEquals("елена скрынник", buck[0])
        self.assertEquals("виктор христенко", buck[1])
        self.assertEquals(2, len(buck[2]))
        self.assertEquals("брат", buck[2][0])
        self.assertEquals("служба", buck[2][1])
        self.assertEquals("http://goo.gl/ohEX4", buck[3])

        buck = parse_line("елена скрынник-виктор христенко-брат.служба", "http://goo.gl/ohEX4")
        self.assertEquals("елена скрынник", buck[0])
        self.assertEquals("виктор христенко", buck[1])
        self.assertEquals(2, len(buck[2]))
        self.assertEquals("брат", buck[2][0])
        self.assertEquals("служба", buck[2][1])
        self.assertEquals("http://goo.gl/ohEX4", buck[3])

    """
    def test_names_similarity(self):
        pass

    def test_tags_in_list(self):
        pass
    """

if __name__ == '__main__':
    unittest.main()
