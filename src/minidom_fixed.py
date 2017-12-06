"""
Попытка исправления недостатка xml.dom.minidom, состоящего в том, что
xml.dom.mindom.Document.writexml не сохраняет последовательность атрибутов тэга.
"""

from collections import OrderedDict

from xml.dom.minidom import \
    Document as minidomDocument, \
    Element as minidomElement, \
    Node, \
    _write_data


class Element(minidomElement):
    def _ensure_attributes(self):
        if self._attrs is None:
            self._attrs = OrderedDict()
            self._attrsNS = OrderedDict()

    def writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        writer.write(indent + "<" + self.tagName)

        attrs = self._get_attributes()
        # <SC> Сохраняем оригинальный порядок атрибутов
        # a_names = sorted(attrs.keys())
        a_names = attrs.keys()

        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            writer.write(">")
            if (len(self.childNodes) == 1 and
                    self.childNodes[0].nodeType == Node.TEXT_NODE):
                self.childNodes[0].writexml(writer, '', '', '')
            else:
                writer.write(newl)
                for node in self.childNodes:
                    node.writexml(writer, indent + addindent, addindent, newl)
                writer.write(indent)
            writer.write("</%s>%s" % (self.tagName, newl))
        else:
            writer.write("/>%s" % (newl))


class Document(minidomDocument):
    def createElement(self, tagName):
        e = Element(tagName)
        e.ownerDocument = self
        return e
