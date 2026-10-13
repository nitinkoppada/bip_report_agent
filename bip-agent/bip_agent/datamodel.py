"""BI Publisher data model (.xdm) and sample XML generation from a ReportSpec.

The data model has one SQL data set against the Fusion application database
(ApplicationDB_FSCM) and, when the spec has break columns, a two-level
structure: G_HEADER (break columns) containing G_LINES (detail columns).
"""
from __future__ import annotations

import datetime as _dt
from xml.sax.saxutils import escape, quoteattr

from .spec import ReportSpec

DATA_SOURCE = "ApplicationDB_FSCM"
DATASET = "Q_MAIN"
XSD_TYPES = {"string": "xsd:string", "number": "xsd:double", "date": "xsd:date"}
PARAM_TYPES = {"string": "xsd:string", "number": "xsd:integer", "date": "xsd:date"}


def group_names(spec: ReportSpec) -> tuple[str | None, str]:
    return ("G_HEADER" if spec.break_columns else None, "G_LINES")


def _cdata(text: str) -> str:
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def _element(col, order: int, indent: str) -> str:
    return (f'{indent}<element name="{col.name}" value="{col.name}" label={quoteattr(col.label)} '
            f'dataType="{XSD_TYPES[col.data_type]}" breakOrder="" fieldOrder="{order}"/>')


def build_datamodel(spec: ReportSpec) -> str:
    header, lines = group_names(spec)
    out = [
        "<?xml version = '1.0' encoding = 'utf-8'?>",
        '<dataModel xmlns="http://xmlns.oracle.com/oxp/xmlp" version="2.0" '
        'xmlns:xdm="http://xmlns.oracle.com/oxp/xmlp" xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        f'defaultDataSourceRef="{DATA_SOURCE}">',
        f"   <description>{_cdata(spec.description)}</description>",
        "   <dataProperties>",
        '      <property name="include_parameters" value="true"/>',
        '      <property name="include_null_Element" value="true"/>',
        '      <property name="include_rowsettag" value="false"/>',
        '      <property name="xml_tag_case" value="upper"/>',
        '      <property name="generate_output_format" value="xml"/>',
        '      <property name="optimize_query_executions" value="false"/>',
        "   </dataProperties>",
        "   <dataSets>",
        f'      <dataSet name="{DATASET}" type="simple">',
        f'         <sql dataSourceRef="{DATA_SOURCE}" nsQuery="true" bindMultiValueAsCommaSepStr="false">',
        f"            {_cdata(spec.sql)}",
        "         </sql>",
        "      </dataSet>",
        "   </dataSets>",
        '   <output rootName="DATA_DS" uniqueRowName="false">',
        '      <nodeList name="data-structure">',
        '         <dataStructure tagName="DATA_DS">',
    ]
    ind = " " * 12
    if header:
        out.append(f'{ind}<group name="{header}" label="{header}" source="{DATASET}">')
        for i, c in enumerate(spec.break_columns, 1):
            out.append(_element(c, i, ind + "   ").replace('breakOrder=""', 'breakOrder="ascending"'))
        ind += "   "
    out.append(f'{ind}<group name="{lines}" label="{lines}" source="{DATASET}">')
    for i, c in enumerate(spec.detail_columns, 1):
        out.append(_element(c, i, ind + "   "))
    out.append(f"{ind}</group>")
    if header:
        out.append(f"{ind[:-3]}</group>")
    out += [
        "         </dataStructure>",
        "      </nodeList>",
        "   </output>",
        "   <eventTriggers/>",
        "   <lexicals/>",
        "   <valueSets/>",
        "   <parameters>",
    ]
    for row, p in enumerate(spec.parameters, 1):
        default = f" defaultValue={quoteattr(p.default_value)}" if p.default_value else ""
        mandatory = ' mandatory="true"' if p.required else ""
        out.append(f'      <parameter name="{p.name}"{default} dataType="{PARAM_TYPES[p.data_type]}" '
                   f'rowPlacement="{row}"{mandatory}>')
        if p.data_type == "date":
            out.append(f'         <date label={quoteattr(p.label)} format="yyyy-MM-dd"/>')
        else:
            out.append(f'         <input label={quoteattr(p.label)} size="30"/>')
        out.append("      </parameter>")
    out += ["   </parameters>", "   <bursting/>", "</dataModel>", ""]
    return "\n".join(out)


def _sample_value(col, row: int) -> str:
    if col.data_type == "number":
        return f"{(row * 1234.5) % 9000 + 100:.2f}"
    if col.data_type == "date":
        return (_dt.date(2026, 1, 15) + _dt.timedelta(days=17 * row)).isoformat() + "T00:00:00.000+00:00"
    return f"{col.label} {row}"


def build_sample_xml(spec: ReportSpec, headers: int = 2, lines_per_header: int = 3) -> str:
    """Dummy data shaped like the data model output, for previewing the RTF in Word."""
    header, lines = group_names(spec)
    out = ['<?xml version="1.0" encoding="UTF-8"?>', "<DATA_DS>"]
    for p in spec.parameters:
        out.append(f"   <{p.name}>{escape(p.default_value)}</{p.name}>")
    row = 0
    for h in range(1, (headers if header else 1) + 1):
        ind = "   "
        if header:
            out.append(f"{ind}<{header}>")
            for c in spec.break_columns:
                out.append(f"{ind}   <{c.name}>{escape(_sample_value(c, h))}</{c.name}>")
            ind += "   "
        for _ in range(lines_per_header if header else lines_per_header * headers):
            row += 1
            out.append(f"{ind}<{lines}>")
            for c in spec.detail_columns:
                out.append(f"{ind}   <{c.name}>{escape(_sample_value(c, row))}</{c.name}>")
            out.append(f"{ind}</{lines}>")
        if header:
            out.append(f"   </{header}>")
    out += ["</DATA_DS>", ""]
    return "\n".join(out)
