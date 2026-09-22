# Renders specific pages of a source PDF into compressed JPEGs sized for
# Selected Work cards (1600px wide, quality 78 — matches every existing
# entry, keeps each image well under 250KB).
#
# Requires: pip install pymupdf Pillow
#
# Usage:
#   python render_pdf.py "<source.pdf>" "<out_dir>" 1:slug-1 3:slug-2
#
# Each PAGE:NAME arg renders 1-indexed PAGE to <out_dir>/<NAME>.jpg.
# Run with no PAGE:NAME args to just print the page count, so you can decide
# which pages to render before spending time on all of them.

import sys
import os
import pymupdf

MAX_WIDTH = 1600
QUALITY = 78

def main():
    if len(sys.argv) < 3:
        print("usage: render_pdf.py <source.pdf> <out_dir> [page:name ...]")
        sys.exit(1)

    src, out_dir = sys.argv[1], sys.argv[2]
    jobs = []
    for arg in sys.argv[3:]:
        page_str, name = arg.split(":", 1)
        jobs.append((int(page_str), name))

    os.makedirs(out_dir, exist_ok=True)
    doc = pymupdf.open(src)
    print(f"pages: {doc.page_count}")

    for page_num, name in jobs:
        page = doc[page_num - 1]
        scale = MAX_WIDTH / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
        out_path = os.path.join(out_dir, f"{name}.jpg")
        pix.pil_save(out_path, "JPEG", quality=QUALITY, optimize=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"{name}.jpg -> {pix.width}x{pix.height}, {size_kb:.0f} KB")

    doc.close()

if __name__ == "__main__":
    main()
