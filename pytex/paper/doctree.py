from pylatex import Section, Subsection, Subsubsection, Package, Command, NoEscapeStr
from pylatex.base_classes import LatexObject
import sympy as sp
from .section import Section

marker_prefix = ["section", "subsection", "subsubsection"]
font = ["hb", "hc", "hc"]


class DocTreeNode(Section):
    def __init__(self, struct, top=0, auto_font=False):
        if auto_font:
            super().__init__(NoEscapeStr(Command(font[top], struct["title"]).dumps()))
        else:
            super().__init__(struct["title"])

        self._latex_name = marker_prefix[top]
        if type(struct["content"]) is list:
            for i, content in enumerate(struct["content"]):
                if type(content) is dict:
                    self.append(DocTreeNode(content, top+1))
        elif type(struct["content"]) is dict:
            self.append(DocTreeNode(struct["content"], top+1))
        else:
            self.append(struct["content"])
        self.dumps_packages()


class DocTree(LatexObject):
    def __init__(self, *structs, packages=None, top=0, auto_font=False):
        super().__init__()
        self.data = []
        self.packages = []
        for struct in structs:
            self.data.append(DocTreeNode(struct, top, auto_font))
        if packages is not None:
            for package in packages:
                self.packages.append(package)
        for node in self.data:
            self.packages.extend(node.packages)

    def __repr__(self):
        return self.dumps()

    def dumps(self):
        out = ""
        for node in self.data:
            out += node.dumps()
        return out
