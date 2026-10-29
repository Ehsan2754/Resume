#!/usr/bin/env python3
"""Fail if a PDF contains text that a human would not see: tiny fonts, (near-)white fill, or glyphs outside the page box.
This is the honesty gate from the Style Guide §3.4 — resumes must read the same to a screener and to a person."""
import sys
try:
    import pymupdf as fitz  # PyMuPDF >= 1.24.3
except ImportError:
  try:
    import fitz  # older PyMuPDF
  except ImportError:
    print("hidden_text_check: PyMuPDF not installed — skipping (pip install pymupdf)")
    sys.exit(0)

MIN_PT = 6.0
problems = []
doc = fitz.open(sys.argv[1])
for pno, page in enumerate(doc, 1):
    box = page.rect
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for span in line["spans"]:
                txt = span["text"].strip()
                if not txt:
                    continue
                size = span["size"]
                color = span["color"]
                r, g, bl = (color >> 16) & 255, (color >> 8) & 255, color & 255
                bbox = fitz.Rect(span["bbox"])
                if size < MIN_PT:
                    problems.append(f"p{pno}: font {size:.1f}pt < {MIN_PT}pt: {txt[:40]!r}")
                if min(r, g, bl) > 235:
                    problems.append(f"p{pno}: near-white text #{r:02x}{g:02x}{bl:02x}: {txt[:40]!r}")
                if not box.intersects(bbox):
                    problems.append(f"p{pno}: text outside page box: {txt[:40]!r}")
if problems:
    print("FAIL: hidden-text check")
    print("\n".join(problems))
    sys.exit(1)
print("hidden-text check: OK")
