#!/usr/bin/env python3
"""macdnie.com link checker (stdlib only).

For every .html file under www/ it verifies that:
  - each internal href/src resolves to an existing file, and
  - each fragment (#anchor) exists as an id in the target document.
It also does a structural sanity pass (unclosed/mismatched tags) and prints
the deduplicated list of external URLs so they can be spot-checked.

Usage:  python3 scripts/check-links.py   (from www/)
Exit code 0 = all good, 1 = problems found.
"""
import html.parser
import pathlib
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class Scan(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.stack, self.errors = set(), [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if key in a and a[key]:
                self.refs.append((a[key], self.getpos()[0]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> with no open tag")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> (opened line {line})")


def main() -> int:
    pages = sorted(ROOT.rglob("*.html"))
    docs = {}
    for p in pages:
        s = Scan()
        s.feed(p.read_text(encoding="utf-8"))
        if s.stack:
            for tag, line in s.stack:
                s.errors.append(f"line {line}: <{tag}> never closed")
        docs[p] = s

    problems, externals = [], set()
    for page, doc in docs.items():
        rel = page.relative_to(ROOT)
        for err in doc.errors:
            problems.append(f"{rel}: STRUCTURE {err}")
        for ref, line in doc.refs:
            u = urllib.parse.urlparse(ref)
            if u.scheme in ("http", "https"):
                externals.add(ref)
                continue
            if u.scheme in ("mailto", "tel", "data"):
                continue
            path, frag = u.path, u.fragment
            if path.startswith("/"):
                target = ROOT / path.lstrip("/")
            elif path:
                target = (page.parent / path).resolve()
            else:
                target = page                      # same-page #fragment
            if path and not target.exists():
                problems.append(f"{rel}:{line}: broken href {ref!r}")
                continue
            if frag:
                tdoc = docs.get(pathlib.Path(target))
                if tdoc is None:
                    continue                        # fragment into a non-HTML asset
                if frag not in tdoc.ids:
                    problems.append(f"{rel}:{line}: missing anchor #{frag} in {target.name}")

    print(f"pages scanned : {len(pages)}")
    print(f"external URLs : {len(externals)}")
    for u in sorted(externals):
        print(f"  - {u}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("\ninternal links, anchors and tag structure: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
