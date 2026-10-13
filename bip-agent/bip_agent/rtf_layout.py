"""A plain RTF layout template with BI Publisher tags.

BI Publisher reads <?...?> tags typed as ordinary text in an RTF document, so
the template needs no Word form fields. Layout: title, parameter values, then
per break group a header line and a table of detail rows with optional totals,
and a grand total at the end.
"""
from __future__ import annotations

from .datamodel import group_names
from .spec import ReportSpec

PAGE_W, PAGE_H, MARGIN = 15840, 12240, 720  # landscape letter, 0.5" margins (twips)
WIDTH_UNITS = {"string": 2.0, "number": 1.2, "date": 1.2}


def rtf_escape(text: str) -> str:
    out = []
    for ch in text:
        if ch in "\\{}":
            out.append("\\" + ch)
        elif ord(ch) > 127:
            code = ord(ch)
            out.append(f"\\u{code if code < 32768 else code - 65536}?")
        elif ch == "\n":
            out.append("\\line ")
        else:
            out.append(ch)
    return "".join(out)


def _field(col) -> str:
    if col.data_type == "number":
        return f"<?format-number:{col.name};'999G999G990D00'?>"
    if col.data_type == "date":
        return f"<?format-date:{col.name};'MEDIUM'?>"
    return f"<?{col.name}?>"


def _row(cells: list[str], edges: list[int], header: bool = False, aligns: list[str] | None = None,
         bold: bool = False) -> str:
    border = "\\clbrdrt\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10\\clbrdrb\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10"
    shade = "\\clcbpat2" if header else ""
    parts = ["\\trowd\\trgaph70\\trleft0" + ("\\trhdr" if header else "")]
    for e in edges:
        parts.append(f"{border}{shade}\\cellx{e}")
    for i, c in enumerate(cells):
        align = (aligns or ["ql"] * len(cells))[i]
        b = "\\b " if (header or bold) else ""
        parts.append(f"\\pard\\intbl\\{align}\\fs18 {b}{c}\\b0\\cell")
    parts.append("\\row")
    return "\n".join(parts)


def build_rtf(spec: ReportSpec) -> str:
    header_group, lines_group = group_names(spec)
    detail = spec.detail_columns
    usable = PAGE_W - 2 * MARGIN
    units = [WIDTH_UNITS[c.data_type] for c in detail]
    edges, acc = [], 0.0
    for u in units:
        acc += u
        edges.append(int(usable * acc / sum(units)))
    aligns = ["qr" if c.data_type == "number" else "ql" for c in detail]

    doc = [
        "{\\rtf1\\ansi\\ansicpg1252\\deff0",
        "{\\fonttbl{\\f0\\fswiss Calibri;}}",
        "{\\colortbl;\\red0\\green0\\blue0;\\red221\\green230\\blue241;}",
        f"\\paperw{PAGE_W}\\paperh{PAGE_H}\\landscape\\margl{MARGIN}\\margr{MARGIN}\\margt{MARGIN}\\margb{MARGIN}",
        f"\\pard\\qc\\b\\fs32 {rtf_escape(spec.title)}\\b0\\par",
    ]
    if spec.parameters:
        params = "   ".join(f"{rtf_escape(p.label)}: <?{p.name}?>" for p in spec.parameters)
        doc.append(f"\\pard\\qc\\fs18 {params}\\par")
    doc.append("\\pard\\par")

    def table_block(sum_path: str, total_label: str) -> list[str]:
        block = [_row([rtf_escape(c.label) for c in detail], edges, header=True, aligns=aligns)]
        cells = [_field(c) for c in detail]
        cells[0] = f"<?for-each:{lines_group}?>" + cells[0]
        cells[-1] = cells[-1] + "<?end for-each?>"
        block.append(_row(cells, edges, aligns=aligns))
        if any(c.total for c in detail):
            totals = []
            for i, c in enumerate(detail):
                if c.total:
                    totals.append(f"<?format-number:sum({sum_path}{c.name});'999G999G990D00'?>")
                else:
                    totals.append(total_label if i == 0 else "")
            block.append(_row(totals, edges, aligns=aligns, bold=True))
        block.append("\\pard\\par")
        return block

    if header_group:
        doc.append(f"\\pard\\fs4 <?for-each:{header_group}?>\\par")
        heading = "   ".join(f"{rtf_escape(c.label)}: {_field(c)}" for c in spec.break_columns)
        doc.append(f"\\pard\\keepn\\b\\fs22 {heading}\\b0\\par")
        doc += table_block(f"{lines_group}/", "Subtotal")
        doc.append("\\pard\\fs4 <?end for-each?>\\par")
        grand = [c for c in detail if c.total]
        if grand:
            parts = "   ".join(
                f"{rtf_escape(c.label)}: <?format-number:sum(.//{lines_group}/{c.name});'999G999G990D00'?>"
                for c in grand)
            doc.append(f"\\pard\\b\\fs20 Grand total   {parts}\\b0\\par")
    else:
        doc += table_block(f".//{lines_group}/", "Total")
    doc.append("}")
    return "\n".join(doc) + "\n"
