#!/usr/bin/env python3
"""Generate an eBay UK product description from 1688 product data."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ProductData:
    title: str
    category: str = ""
    brand: str = ""
    model: str = ""
    material: str = ""
    size: str = ""
    color: str = ""
    weight: str = ""
    features: List[str] = field(default_factory=list)
    package_contents: List[str] = field(default_factory=list)
    moq: str = ""
    price_range: str = ""
    images: List[str] = field(default_factory=list)
    notes: str = ""


def _listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(";")]
        return [part for part in parts if part]
    return [str(value).strip()]


def parse_product_data(payload: Dict[str, Any]) -> ProductData:
    return ProductData(
        title=str(payload.get("title", "")).strip(),
        category=str(payload.get("category", "")).strip(),
        brand=str(payload.get("brand", "")).strip(),
        model=str(payload.get("model", "")).strip(),
        material=str(payload.get("material", "")).strip(),
        size=str(payload.get("size", "")).strip(),
        color=str(payload.get("color", "")).strip(),
        weight=str(payload.get("weight", "")).strip(),
        features=_listify(payload.get("features")),
        package_contents=_listify(payload.get("package_contents")),
        moq=str(payload.get("moq", "")).strip(),
        price_range=str(payload.get("price_range", "")).strip(),
        images=_listify(payload.get("images")),
        notes=str(payload.get("notes", "")).strip(),
    )


def _bullet_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items if item)


def _spec_table(product: ProductData) -> str:
    rows = [
        ("Category", product.category),
        ("Brand", product.brand),
        ("Model", product.model),
        ("Material", product.material),
        ("Size", product.size),
        ("Colour", product.color),
        ("Weight", product.weight),
        ("MOQ", product.moq),
        ("1688 Price Range", product.price_range),
    ]
    filtered = [(label, value) for label, value in rows if value]
    return "\n".join(f"| {label} | {value} |" for label, value in filtered)


def generate_markdown(product: ProductData) -> str:
    features = _bullet_list(product.features) or "- Please see item specifics."
    package = _bullet_list(product.package_contents) or "- 1 x Item as described"
    specs = _spec_table(product)

    notes = product.notes.strip()
    if notes:
        notes = f"\n\n**Notes from supplier**\n{notes}"

    return f"""# {product.title or 'Product Title'}\n\n**UK-friendly highlights**\n{features}\n\n**What you get**\n{package}\n\n**Specifications**\n| Field | Details |\n| --- | --- |\n{specs}\n\n**Shipping & Returns**\n- UK dispatch location: Please update with your fulfilment address.\n- Handling time: Update based on your stock availability.\n- Returns accepted within 30 days (buyer pays return postage unless item is faulty).\n\n**Compliance reminder**\n- Ensure the item meets UK regulations and include any required safety markings.\n\n**Last updated**: {date.today().isoformat()}\n{notes}\n"""


def generate_html(product: ProductData) -> str:
    features = "".join(f"<li>{item}</li>" for item in product.features if item) or "<li>Please see item specifics.</li>"
    package = "".join(f"<li>{item}</li>" for item in product.package_contents if item) or "<li>1 x Item as described</li>"

    specs_rows = []
    for label, value in [
        ("Category", product.category),
        ("Brand", product.brand),
        ("Model", product.model),
        ("Material", product.material),
        ("Size", product.size),
        ("Colour", product.color),
        ("Weight", product.weight),
        ("MOQ", product.moq),
        ("1688 Price Range", product.price_range),
    ]:
        if value:
            specs_rows.append(f"<tr><th>{label}</th><td>{value}</td></tr>")

    notes = f"<h3>Notes from supplier</h3><p>{product.notes}</p>" if product.notes else ""

    return f"""<h1>{product.title or 'Product Title'}</h1>
<h3>UK-friendly highlights</h3>
<ul>{features}</ul>
<h3>What you get</h3>
<ul>{package}</ul>
<h3>Specifications</h3>
<table>
{''.join(specs_rows)}
</table>
<h3>Shipping &amp; Returns</h3>
<ul>
  <li>UK dispatch location: Please update with your fulfilment address.</li>
  <li>Handling time: Update based on your stock availability.</li>
  <li>Returns accepted within 30 days (buyer pays return postage unless item is faulty).</li>
</ul>
<h3>Compliance reminder</h3>
<ul>
  <li>Ensure the item meets UK regulations and include any required safety markings.</li>
</ul>
<p><strong>Last updated</strong>: {date.today().isoformat()}</p>
{notes}
"""


def load_payload(path: Optional[str]) -> Dict[str, Any]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an eBay UK product description from 1688 product data.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a JSON file exported from 1688 (or piped via stdin).",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format for the listing description.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload = load_payload(args.input)
    product = parse_product_data(payload)

    if args.format == "html":
        output = generate_html(product)
    else:
        output = generate_markdown(product)

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
