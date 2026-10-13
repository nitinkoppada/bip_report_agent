"""A tiny stand-in for the parts of BeautifulSoup the crawler uses (standard library only).

Supports: find / find_all (tag name or list of names, recursive=, attribute filters such as
href=True, limit=), find_all_next / find_all_previous (document order), get_text(sep, strip),
.name, .get(attr), .body, and find(string=True, recursive=False) for a direct text child.
"""
from __future__ import annotations

from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
        "source", "track", "wbr"}
# Tags whose open element is closed implicitly by a sibling of the same kind.
AUTOCLOSE = {"p": {"p", "div", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "pre"},
             "li": {"li"}, "tr": {"tr"}, "td": {"td", "th", "tr"}, "th": {"td", "th", "tr"},
             "option": {"option"}}


class Node:
    def __init__(self, name: str | None, attrs: dict | None = None, parent: "Node | None" = None):
        self.name = name
        self.attrs = attrs or {}
        self.parent = parent
        self.children: list = []  # Node or str
        self.order = 0

    # ---- attributes ------------------------------------------------------
    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def __getitem__(self, key):
        return self.attrs[key]

    # ---- traversal -------------------------------------------------------
    def _iter(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c._iter()

    @staticmethod
    def _match(node: "Node", name, attrs: dict) -> bool:
        if name is not None:
            names = {name} if isinstance(name, str) else set(name)
            if node.name not in names:
                return False
        for k, v in attrs.items():
            if v is True:
                if k not in node.attrs:
                    return False
            elif node.attrs.get(k) != v:
                return False
        return True

    def find_all(self, name=None, recursive=True, limit=None, string=None, **attrs):
        if string is not None:
            texts = [c for c in self.children if isinstance(c, str) and c.strip()] if not recursive else \
                [t for t in self._texts()]
            return texts[:limit] if limit else texts
        pool = self._iter() if recursive else (c for c in self.children if isinstance(c, Node))
        out = []
        for n in pool:
            if self._match(n, name, attrs):
                out.append(n)
                if limit and len(out) >= limit:
                    break
        return out

    def find(self, name=None, recursive=True, string=None, **attrs):
        r = self.find_all(name, recursive=recursive, limit=1, string=string, **attrs)
        return r[0] if r else None

    def _root(self):
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    def find_all_next(self, name=None, limit=None, **attrs):
        out = []
        for n in self._root()._doc():
            if n.order > self.order and self._match(n, name, attrs):
                out.append(n)
                if limit and len(out) >= limit:
                    break
        return out

    def find_all_previous(self, name=None, limit=None, **attrs):
        out = []
        for n in reversed(self._root()._doc()):
            if n.order < self.order and n is not self and self._match(n, name, attrs):
                out.append(n)
                if limit and len(out) >= limit:
                    break
        return out

    def _doc(self):
        if not hasattr(self, "_doc_cache"):
            self._doc_cache = list(self._iter())
        return self._doc_cache

    # ---- text ------------------------------------------------------------
    def _texts(self):
        for c in self.children:
            if isinstance(c, str):
                yield c
            elif c.name not in ("script", "style"):
                yield from c._texts()

    def get_text(self, separator: str = "", strip: bool = False) -> str:
        parts = list(self._texts())
        if strip:
            parts = [p.strip() for p in parts if p.strip()]
        return separator.join(parts)

    @property
    def body(self):
        return self.find("body")


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("[document]")
        self.cur = self.root
        self.n = 0

    def _open(self, tag, attrs):
        close_on = AUTOCLOSE
        # implicit close: e.g. <p> ... <p>, <li> ... <li>, <td> ... <td>
        node = self.cur
        while node is not self.root and node.name in close_on and tag in close_on[node.name]:
            node = node.parent
            self.cur = node
        self.n += 1
        el = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur)
        el.order = self.n
        self.cur.children.append(el)
        return el

    def handle_starttag(self, tag, attrs):
        el = self._open(tag, attrs)
        if tag not in VOID:
            self.cur = el

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs)

    def handle_endtag(self, tag):
        node = self.cur
        while node is not self.root and node.name != tag:
            node = node.parent
        if node is not self.root:
            self.cur = node.parent

    def handle_data(self, data):
        if data:
            self.cur.children.append(data)


def BeautifulSoup(html: str, _parser: str = "html.parser") -> Node:  # noqa: N802 - mirrors bs4
    b = _Builder()
    b.feed(html)
    b.close()
    return b.root
