#!/usr/bin/env python3
"""
Generate a polished academic practical report for
MTH00051 Project 1 — Color Compression via K-Means.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image as RLImage,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "report_assets"
OUT_PDF = ROOT / "Lab1.pdf"
BUILD = ROOT / ".report_build"
BUILD.mkdir(exist_ok=True)

# Noto Serif: academic face + Vietnamese + italic
pdfmetrics.registerFont(TTFont("Serif", "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", "/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf"))
pdfmetrics.registerFontFamily(
    "Serif",
    normal="Serif",
    bold="Serif-Bold",
    italic="Serif-Italic",
    boldItalic="Serif-BoldItalic",
)

NAVY = colors.HexColor("#1F2A44")
RULE = colors.HexColor("#2C3E50")
SOFT = colors.HexColor("#F4F6F8")
LINE = colors.HexColor("#C5CDD6")


class HLine(Flowable):
    def __init__(self, width, stroke=RULE, thickness=0.8, space_before=4, space_after=10):
        super().__init__()
        self.width = width
        self.stroke = stroke
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after
        self.height = thickness + space_before + space_after

    def draw(self):
        self.canv.setStrokeColor(self.stroke)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after
        self.canv.line(0, y, self.width, y)


def clean_image(src: Path, dst: Path, max_side: int = 1000) -> Path:
    im = Image.open(src).convert("RGB")
    gray = ImageOps.grayscale(im)
    bbox = ImageOps.invert(gray).getbbox()
    if bbox:
        l, t, r, b = bbox
        pad = 2
        im = im.crop(
            (
                max(0, l - pad),
                max(0, t - pad),
                min(im.width, r + pad),
                min(im.height, b + pad),
            )
        )
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(dst, optimize=True)
    return dst


def prepare_assets() -> dict[str, Path]:
    names = [
        "logo",
        "original",
        "k3_in",
        "k3_rand",
        "k5_in",
        "k5_rand",
        "k7_in",
        "k7_rand",
    ]
    paths = {}
    for name in names:
        src = ASSETS / f"{name}.png"
        dst = BUILD / f"{name}.png"
        if name == "logo":
            Image.open(src).convert("RGBA").save(dst)
        else:
            clean_image(src, dst)
        paths[name] = dst
    return paths


def render_equation(tex: str, name: str, fontsize: int = 13) -> Path:
    """Render a LaTeX-like equation to a transparent PNG via Matplotlib."""
    out = BUILD / f"eq_{name}.png"
    fig = plt.figure(figsize=(7.2, 0.55))
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.text(
        0.5,
        0.5,
        f"${tex}$",
        fontsize=fontsize,
        ha="center",
        va="center",
        color="#111111",
    )
    fig.savefig(out, dpi=220, transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    return out


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_uni": ParagraphStyle(
            "cover_uni",
            parent=base["Normal"],
            fontName="Serif-Bold",
            fontSize=12.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=1,
        ),
        "cover_faculty": ParagraphStyle(
            "cover_faculty",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=11.5,
            leading=15,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=14,
        ),
        "cover_kicker": ParagraphStyle(
            "cover_kicker",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=RULE,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Normal"],
            fontName="Serif-Bold",
            fontSize=20,
            leading=25,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=6,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontName="Serif-Italic",
            fontSize=12.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
            spaceAfter=8,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            spaceBefore=2,
        ),
        "cover_label": ParagraphStyle(
            "cover_label",
            parent=base["Normal"],
            fontName="Serif-Bold",
            fontSize=10.5,
            leading=13,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Serif-Bold",
            fontSize=13.5,
            leading=17,
            spaceBefore=2,
            spaceAfter=7,
            textColor=NAVY,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Serif-Bold",
            fontSize=11.5,
            leading=15,
            spaceBefore=9,
            spaceAfter=4,
            textColor=colors.HexColor("#243447"),
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Serif-Bold",
            fontSize=10.8,
            leading=14,
            spaceBefore=7,
            spaceAfter=3,
            textColor=colors.HexColor("#2B3648"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=10.7,
            leading=15.2,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            firstLineIndent=14,
        ),
        "body0": ParagraphStyle(
            "body0",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=10.7,
            leading=15.2,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Serif-Italic",
            fontSize=9,
            leading=11.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
            spaceBefore=2,
            spaceAfter=8,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=10.8,
            leading=17,
            alignment=TA_LEFT,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=10.7,
            leading=14.8,
            alignment=TA_JUSTIFY,
            spaceAfter=2,
        ),
        "ref": ParagraphStyle(
            "ref",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=10,
            leading=13.5,
            leftIndent=16,
            firstLineIndent=-16,
            spaceAfter=5,
            alignment=TA_JUSTIFY,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=9.3,
            leading=12.2,
            alignment=TA_LEFT,
        ),
        "cell_c": ParagraphStyle(
            "cell_c",
            parent=base["Normal"],
            fontName="Serif",
            fontSize=9.3,
            leading=12.2,
            alignment=TA_CENTER,
        ),
        "th": ParagraphStyle(
            "th",
            parent=base["Normal"],
            fontName="Serif-Bold",
            fontSize=9.3,
            leading=12.2,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "eq_note": ParagraphStyle(
            "eq_note",
            parent=base["Normal"],
            fontName="Serif-Italic",
            fontSize=9,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475569"),
            spaceAfter=6,
        ),
    }


def add_page_number(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    if page >= 3:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        y = 1.45 * cm
        canvas.line(2.0 * cm, y + 4, A4[0] - 2.0 * cm, y + 4)
        canvas.setFillColor(colors.HexColor("#475569"))
        canvas.setFont("Serif-Italic", 8)
        canvas.drawString(2.0 * cm, y - 6, "MTH00051 · Practical Report 1")
        canvas.setFont("Serif", 9)
        canvas.drawCentredString(A4[0] / 2.0, y - 6, str(page))
        canvas.setFont("Serif-Italic", 8)
        canvas.drawRightString(A4[0] - 2.0 * cm, y - 6, "Color Compression")
    canvas.restoreState()


def rl_image(path: Path, width: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    img = RLImage(str(path), width=width, height=width * (h / float(w)))
    img.hAlign = "CENTER"
    return img


def equation_block(path: Path, label: str, styles, width=14.5 * cm):
    img = rl_image(path, width=min(width, 14.5 * cm))
    note = Paragraph(label, styles["eq_note"])
    return KeepTogether([Spacer(1, 2), img, note, Spacer(1, 2)])


def two_figs(p1: Path, c1: str, p2: Path, c2: str, styles, width=7.2 * cm):
    table = Table(
        [
            [rl_image(p1, width), rl_image(p2, width)],
            [Paragraph(c1, styles["caption"]), Paragraph(c2, styles["caption"])],
        ],
        colWidths=[width + 0.35 * cm, width + 0.35 * cm],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    return table


def styled_table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
                ("BOX", (0, 0), (-1, -1), 0.7, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def build():
    assets = prepare_assets()
    styles = make_styles()

    # Pre-render key equations
    eq_pixels = render_equation(
        r"X=\{x_i\in\mathbb{R}^{3}\mid i=1,\ldots,N\},\quad N=H\cdot W",
        "pixels",
        12,
    )
    eq_wcss = render_equation(
        r"J(C,\ell)=\sum_{i=1}^{N}\|x_i-c_{\ell(i)}\|_{2}^{2}",
        "wcss",
        13,
    )
    eq_assign = render_equation(
        r"\ell(i)=\arg\min_{j\in\{1,\ldots,k\}}\|x_i-c_j\|_{2}^{2}",
        "assign",
        12,
    )
    eq_update = render_equation(
        r"c_j\leftarrow\frac{1}{|S_j|}\sum_{i\in S_j}x_i,\quad S_j=\{i\mid\ell(i)=j\}",
        "update",
        12,
    )
    eq_mse = render_equation(
        r"\mathrm{MSE}=\frac{1}{N}\sum_{i=1}^{N}\|x_i-\hat{x}_i\|_{2}^{2}=\frac{J(C,\ell)}{N}",
        "mse",
        12,
    )

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=2.1 * cm,
        rightMargin=2.1 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.9 * cm,
        title="Practical Report 1: Color Compression via K-Means Clustering",
        author="Nguyễn Thế Hiển — 22127107",
        subject="MTH00051 Applied Mathematics and Statistics",
        creator="Academic report generator",
    )

    story = []
    content_width = A4[0] - doc.leftMargin - doc.rightMargin

    # ========================= COVER =========================
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("VIETNAM NATIONAL UNIVERSITY — HO CHI MINH CITY", styles["cover_uni"]))
    story.append(Paragraph("UNIVERSITY OF SCIENCE", styles["cover_uni"]))
    story.append(Paragraph("Faculty of Information Technology", styles["cover_faculty"]))
    story.append(rl_image(assets["logo"], 3.4 * cm))
    story.append(Spacer(1, 0.55 * cm))
    story.append(HLine(content_width, thickness=1.1, space_before=2, space_after=8))
    story.append(Paragraph("PRACTICAL REPORT 1", styles["cover_kicker"]))
    story.append(
        Paragraph(
            "COLOR COMPRESSION<br/>VIA K-MEANS CLUSTERING",
            styles["cover_title"],
        )
    )
    story.append(
        Paragraph(
            "An unsupervised learning approach to RGB palette reduction",
            styles["cover_subtitle"],
        )
    )
    story.append(HLine(content_width, thickness=0.7, space_before=2, space_after=12))
    story.append(
        Paragraph(
            "Course: <b>MTH00051 — Applied Mathematics and Statistics</b>",
            styles["cover_meta"],
        )
    )
    story.append(Spacer(1, 1.1 * cm))
    story.append(Paragraph("STUDENT", styles["cover_label"]))
    story.append(Paragraph("Nguyễn Thế Hiển", styles["cover_meta"]))
    story.append(Paragraph("Student ID: 22127107 · Class: 22CLC08", styles["cover_meta"]))
    story.append(Paragraph("INSTRUCTORS", styles["cover_label"]))
    for name in [
        "Mr. Vũ Quốc Hoàng",
        "Mr. Nguyễn Văn Quang Huy",
        "Mr. Nguyễn Ngọc Toàn",
        "Mrs. Phan Thị Phương Uyên",
    ]:
        story.append(Paragraph(name, styles["cover_meta"]))
    story.append(Spacer(1, 1.6 * cm))
    story.append(Paragraph("Ho Chi Minh City, 2024", styles["cover_meta"]))
    story.append(PageBreak())

    # ========================= FRONT MATTER =========================
    story.append(Paragraph("Acknowledgments", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(
        Paragraph(
            "This practical exercise forms part of MTH00051 — Applied Mathematics and "
            "Statistics, a foundational course for students of Information Technology. "
            "Through the Color Compression project, I had the opportunity to connect "
            "clustering theory with a concrete computational application.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "I gratefully acknowledge the guidance of Mr. Vũ Quốc Hoàng, Mr. Nguyễn Văn "
            "Quang Huy, Mr. Nguyễn Ngọc Toàn, and Mrs. Phan Thị Phương Uyên. Their "
            "lectures and laboratory support clarified both the mathematical principles "
            "and the engineering constraints of the assignment. I also thank my classmates "
            "in 22CLC08 for constructive discussion throughout the course.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Any remaining errors in the implementation or in this report are my own.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Abstract", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(
        Paragraph(
            "Digital RGB images admit up to 256<sup>3</sup> distinct colors, which makes "
            "naive storage expensive. Color compression (color quantization) seeks a "
            "compact palette of <i>k</i> representative colors while preserving the "
            "visual identity of the scene. In this report, each pixel is modeled as a "
            "point in ℝ<sup>3</sup> and clustered by the K-Means algorithm "
            "implemented from first principles in Python.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "We formalize the optimization objective as minimization of the "
            "within-cluster sum of squares, describe Lloyd’s alternating minimization "
            "procedure, and compare two centroid-initialization schemes required by the "
            "course specification: <i>random</i> and <i>in_pixels</i>. Qualitative "
            "experiments for <i>k</i> ∈ {3, 5, 7} show that larger palettes recover "
            "finer tonal structure, whereas initialization mainly affects which local "
            "minimum is attained. The study illustrates how a classical unsupervised "
            "method links Euclidean geometry, iterative optimization, and practical "
            "image processing.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Keywords:</b> color quantization; K-Means clustering; Lloyd iteration; "
            "Euclidean distance; image compression; unsupervised learning.",
            styles["body0"],
        )
    )
    story.append(PageBreak())

    # ========================= TOC =========================
    story.append(Paragraph("Contents", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=10))
    toc = [
        ("1.", "Introduction", "4"),
        ("2.", "Problem Formulation", "4"),
        ("3.", "Theoretical Background", "5"),
        ("", "3.1  K-Means as an Optimization Procedure", "5"),
        ("", "3.2  Centroid Initialization Strategies", "5"),
        ("4.", "Implementation", "6"),
        ("", "4.1  Software Environment", "6"),
        ("", "4.2  Functional Architecture", "6"),
        ("", "4.3  Main Program Workflow", "7"),
        ("5.", "Experimental Results", "7"),
        ("", "5.1  Experimental Setup", "7"),
        ("", "5.2  Visual Comparison for k = 3, 5, 7", "8"),
        ("", "5.3  Qualitative Summary", "9"),
        ("6.", "Discussion", "10"),
        ("7.", "Conclusion", "10"),
        ("", "References", "11"),
    ]
    for num, title, page in toc:
        left = f"{num}&nbsp;&nbsp;{title}" if num else f"&nbsp;&nbsp;&nbsp;&nbsp;{title}"
        row = Table(
            [[Paragraph(left, styles["toc"]), Paragraph(page, styles["toc"])]],
            colWidths=[14.2 * cm, 1.5 * cm],
        )
        row.setStyle(
            TableStyle(
                [
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.25, LINE),
                ]
            )
        )
        story.append(row)

    story.append(Spacer(1, 0.55 * cm))
    story.append(Paragraph("List of Figures", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    figs = [
        "Figure 1. Original test image prior to compression.",
        "Figure 2. Reconstructions for k = 3 (in_pixels vs random).",
        "Figure 3. Reconstructions for k = 5 (in_pixels vs random).",
        "Figure 4. Reconstructions for k = 7 (in_pixels vs random).",
    ]
    for f in figs:
        story.append(Paragraph(f, styles["toc"]))
    story.append(PageBreak())

    # ========================= 1. INTRODUCTION =========================
    story.append(Paragraph("1. Introduction", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(Paragraph("1.1. Student Information", styles["h2"]))
    info = [
        [Paragraph("<b>Full name</b>", styles["cell"]), Paragraph("Nguyễn Thế Hiển", styles["cell"])],
        [Paragraph("<b>Student ID</b>", styles["cell"]), Paragraph("22127107", styles["cell"])],
        [Paragraph("<b>Class</b>", styles["cell"]), Paragraph("22CLC08", styles["cell"])],
        [
            Paragraph("<b>Course</b>", styles["cell"]),
            Paragraph("MTH00051 — Applied Mathematics and Statistics", styles["cell"]),
        ],
        [
            Paragraph("<b>Project</b>", styles["cell"]),
            Paragraph("Project 01 — Color Compression", styles["cell"]),
        ],
    ]
    info_t = Table(info, colWidths=[3.8 * cm, 12.0 * cm])
    info_t.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("BACKGROUND", (0, 0), (0, -1), SOFT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(info_t)

    story.append(Paragraph("1.2. Motivation and Objectives", styles["h2"]))
    story.append(
        Paragraph(
            "A color photograph is stored as a rectangular array of pixels. In the RGB "
            "model, every pixel carries three channel intensities, each typically encoded "
            "by one byte. The resulting discrete color cube {0,1,…,255}<sup>3</sup> "
            "contains up to 256<sup>3</sup> ≈ 1.68×10<sup>7</sup> admissible colors. Natural "
            "images rarely use the entire cube, yet the number of observed colors is still "
            "large enough to inflate storage and transmission cost.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Color compression (also called color quantization) replaces the original "
            "palette by a much smaller set of prototypes. From the viewpoint of applied "
            "statistics, the task is unsupervised clustering in a three-dimensional "
            "feature space: similar colors are grouped, and each group is summarized by "
            "its centroid. The objectives of this practical report are therefore:",
            styles["body"],
        )
    )
    objectives = [
        "to formalize color quantization as an optimization problem on pixel vectors;",
        "to implement K-Means from scratch with the two prescribed initializations;",
        "to provide an interactive program that exports reconstructed images as png, jpg, or pdf;",
        "to evaluate visual quality for several palette sizes and discuss the results rigorously.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(o, styles["bullet"]), leftIndent=8, bulletColor=NAVY) for o in objectives],
            bulletType="1",
            start="1",
        )
    )

    # ========================= 2. PROBLEM =========================
    story.append(Paragraph("2. Problem Formulation", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(
        Paragraph(
            "Let an RGB image of height <i>H</i> and width <i>W</i> be represented by the "
            "collection of pixel vectors",
            styles["body0"],
        )
    )
    story.append(equation_block(eq_pixels, "(1)", styles))
    story.append(
        Paragraph(
            "Given an integer palette size <i>k</i>, one seeks centroids "
            "C = {c<sub>1</sub>, …, c<sub>k</sub>} ⊂ ℝ<sup>3</sup> and an assignment map "
            "ℓ : {1,…,N} → {1,…,k} that minimize the within-cluster "
            "sum of squares (WCSS)",
            styles["body0"],
        )
    )
    story.append(equation_block(eq_wcss, "(2)", styles))
    story.append(
        Paragraph(
            "The compressed image is then reconstructed by x̂<sub>i</sub> = c<sub>ℓ(i)</sub>. "
            "Consequently, at most <i>k</i> distinct colors appear in the output. "
            "Reconstruction fidelity in RGB geometry may be measured by the mean "
            "squared error",
            styles["body0"],
        )
    )
    story.append(equation_block(eq_mse, "(3)", styles))
    story.append(
        Paragraph(
            "Equation (3) coincides with the normalized objective (2). Lower MSE "
            "indicates a closer Euclidean approximation; perceptual quality, however, "
            "also depends on the human visual system and is therefore examined visually "
            "in Section 5.",
            styles["body"],
        )
    )

    # ========================= 3. THEORY =========================
    story.append(Paragraph("3. Theoretical Background", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(Paragraph("3.1. K-Means as an Optimization Procedure", styles["h2"]))
    story.append(
        Paragraph(
            "Exact global minimization of (2) is NP-hard in general. The classical "
            "Lloyd iteration therefore alternates two conditionally optimal steps.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Assignment step.</b> For fixed centroids, every pixel is labeled by the "
            "nearest prototype under the squared Euclidean metric:",
            styles["body0"],
        )
    )
    story.append(equation_block(eq_assign, "(4)", styles))
    story.append(
        Paragraph(
            "<b>Update step.</b> For a fixed assignment, each nonempty cluster is "
            "summarized by its sample mean—the unique minimizer of the quadratic loss "
            "on that subset:",
            styles["body0"],
        )
    )
    story.append(equation_block(eq_update, "(5)", styles))
    story.append(
        Paragraph(
            "If a cluster becomes empty, the implementation retains the previous "
            "centroid to preserve numerical stability. Iteration stops when centroids "
            "change by less than a prescribed absolute tolerance (10<sup>−4</sup> in this "
            "project) or when a maximum iteration budget is exhausted. Because neither "
            "step increases <i>J</i>, the sequence of objective values is monotonically "
            "non-increasing and converges to a local minimum.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.2. Centroid Initialization Strategies", styles["h2"]))
    story.append(
        Paragraph(
            "K-Means is sensitive to the initial configuration of centroids. Following "
            "the assignment statement, two schemes are implemented.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>random.</b> Each centroid coordinate is drawn independently and uniformly "
            "from [0, 255]. This explores the full RGB cube and may place prototypes "
            "outside the empirical color support of the image, occasionally producing "
            "empty clusters in early iterations.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>in_pixels.</b> Centroids are sampled uniformly without replacement from "
            "observed pixels. The initial palette therefore lies inside the data cloud, "
            "which typically yields a more favorable starting value of <i>J</i> and more "
            "stable early assignments.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Neither strategy guarantees a global optimum. Comparing both initializations "
            "for the same <i>k</i> provides empirical insight into the variability of "
            "local solutions.",
            styles["body"],
        )
    )

    # ========================= 4. IMPLEMENTATION =========================
    story.append(Paragraph("4. Implementation", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(Paragraph("4.1. Software Environment", styles["h2"]))
    story.append(
        Paragraph(
            "The solution is developed in a Jupyter Notebook and uses only the libraries "
            "permitted by the course specification. Pre-built clustering routines "
            "(for example, <font face='Courier'>sklearn.cluster.KMeans</font>) are "
            "excluded from the submission.",
            styles["body"],
        )
    )
    lib = [
        [
            Paragraph("Library", styles["th"]),
            Paragraph("Purpose in this project", styles["th"]),
        ],
        [
            Paragraph("NumPy", styles["cell"]),
            Paragraph(
                "Vectorized distance computation, centroid updates, and array reshaping.",
                styles["cell"],
            ),
        ],
        [
            Paragraph("Pillow (PIL)", styles["cell"]),
            Paragraph(
                "Image I/O, explicit RGB conversion, and export to png / jpg / pdf.",
                styles["cell"],
            ),
        ],
        [
            Paragraph("Matplotlib", styles["cell"]),
            Paragraph(
                "Display of original and reconstructed images during experimentation.",
                styles["cell"],
            ),
        ],
    ]
    story.append(styled_table(lib, [3.4 * cm, 12.4 * cm]))
    story.append(Spacer(1, 0.15 * cm))

    story.append(Paragraph("4.2. Functional Architecture", styles["h2"]))
    story.append(
        Paragraph(
            "The program is decomposed into documented helper functions. The design "
            "keeps mathematical operations (clustering) separate from I/O and "
            "visualization, which facilitates testing and reuse.",
            styles["body"],
        )
    )
    funcs = [
        (
            "read_img(img_path)",
            "Opens an image, converts it to RGB, and returns a floating-point array of shape (H, W, 3).",
        ),
        (
            "show_img / save_img",
            "Visualize an image with Matplotlib, or clip intensities to [0, 255] and write an 8-bit file.",
        ),
        (
            "convert_img_to_1d(img_2d)",
            "Reshapes the image into an (N, 3) design matrix suitable for clustering.",
        ),
        (
            "kmeans(...)",
            "Executes Lloyd iteration with random or in_pixels initialization; returns centroids and labels.",
        ),
        (
            "generate_2d_img(...)",
            "Maps every pixel to its centroid color and restores the spatial layout (H, W, 3).",
        ),
        (
            "reconstruction_error(...)",
            "Computes the MSE in (3), providing a quantitative complement to visual inspection.",
        ),
    ]
    for title, desc in funcs:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", styles["body0"]))

    story.append(Paragraph("4.3. Main Program Workflow", styles["h2"]))
    story.append(
        Paragraph(
            "The interactive <font face='Courier'>main</font> procedure satisfies the "
            "course interface requirements. At each execution the user supplies:",
            styles["body0"],
        )
    )
    inputs = [
        "the path of the input image;",
        "the number of clusters <i>k</i> and the maximum number of iterations;",
        "the initialization mode (<i>random</i>, <i>in_pixels</i>, or both);",
        "the output format chosen from {png, jpg, pdf};",
        "a base filename for the reconstructed image(s).",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(x, styles["bullet"]), leftIndent=8, bulletColor=NAVY) for x in inputs],
            bulletType="bullet",
            start="•",
        )
    )
    story.append(Spacer(1, 0.08 * cm))
    story.append(
        Paragraph(
            "The pipeline then flattens the image, runs K-Means for each requested "
            "initialization, displays the reconstruction, reports the MSE, and exports "
            "the file in the selected format. Supporting checks are collected in "
            "<font face='Courier'>test_functions</font>.",
            styles["body"],
        )
    )

    # ========================= 5. EXPERIMENTS =========================
    story.append(Paragraph("5. Experimental Results", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(Paragraph("5.1. Experimental Setup", styles["h2"]))
    story.append(
        Paragraph(
            "Experiments are conducted on a natural beach photograph containing smooth "
            "illumination gradients (sky and water) together with a high-contrast "
            "silhouette. Such content is informative for quantization: coarse palettes "
            "posterize the sky, while larger palettes restore intermediate tones. Both "
            "initialization strategies are evaluated for <i>k</i> ∈ {3, 5, 7} with a "
            "sufficient iteration budget to reach practical convergence.",
            styles["body"],
        )
    )
    story.append(rl_image(assets["original"], 9.2 * cm))
    story.append(
        Paragraph(
            "Figure 1. Original test image prior to color compression.",
            styles["caption"],
        )
    )

    story.append(Paragraph("5.2. Visual Comparison for k = 3, 5, 7", styles["h2"]))
    story.append(
        Paragraph(
            "For <i>k</i> = 3 (Figure 2), both initializations reduce the scene to a "
            "silhouette, a mid-tone band, and a sky tone. Fine water reflections are "
            "largely suppressed, yet the semantic layout remains recognizable. The close "
            "agreement of the two methods suggests that the dominant chromatic modes are "
            "stable under different starts.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k3_in"],
            "Figure 2a. in_pixels initialization, k = 3.",
            assets["k3_rand"],
            "Figure 2b. random initialization, k = 3.",
            styles,
        )
    )
    story.append(
        Paragraph(
            "For <i>k</i> = 5 (Figure 3), additional centroids capture transitional hues "
            "near the horizon and richer reflections. Differences between initialization "
            "schemes become more noticeable: random sampling may allocate a centroid to a "
            "less frequent region of RGB space, slightly altering the tonal balance "
            "relative to in_pixels.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k5_in"],
            "Figure 3a. in_pixels initialization, k = 5.",
            assets["k5_rand"],
            "Figure 3b. random initialization, k = 5.",
            styles,
        )
    )
    story.append(
        Paragraph(
            "When <i>k</i> = 7 (Figure 4), reconstructions approach the original more "
            "closely. Gradients in the sky and specular highlights on wet sand reappear "
            "as distinct palette entries. Residual discrepancies between the two "
            "initializations illustrate that K-Means may converge to distinct local "
            "minima even for moderate palette sizes.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k7_in"],
            "Figure 4a. in_pixels initialization, k = 7.",
            assets["k7_rand"],
            "Figure 4b. random initialization, k = 7.",
            styles,
        )
    )

    story.append(Paragraph("5.3. Qualitative Summary", styles["h2"]))
    summary = [
        [
            Paragraph("<i>k</i>", styles["th"]),
            Paragraph("Visual fidelity", styles["th"]),
            Paragraph("Effect of initialization", styles["th"]),
        ],
        [
            Paragraph("3", styles["cell_c"]),
            Paragraph(
                "Strong posterization; content preserved only at a coarse semantic level.",
                styles["cell"],
            ),
            Paragraph(
                "Minor differences; dominant colors are recovered consistently.",
                styles["cell"],
            ),
        ],
        [
            Paragraph("5", styles["cell_c"]),
            Paragraph(
                "Improved mid-tones and horizon detail; water structure becomes clearer.",
                styles["cell"],
            ),
            Paragraph(
                "Noticeable palette shifts between random and in_pixels.",
                styles["cell"],
            ),
        ],
        [
            Paragraph("7", styles["cell_c"]),
            Paragraph(
                "Closer to the original; smoother apparent gradients and richer reflections.",
                styles["cell"],
            ),
            Paragraph(
                "Local minima remain visible but are less disruptive perceptually.",
                styles["cell"],
            ),
        ],
    ]
    story.append(styled_table(summary, [1.4 * cm, 7.2 * cm, 7.2 * cm]))

    # ========================= 6. DISCUSSION =========================
    story.append(Paragraph("6. Discussion", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(
        Paragraph(
            "The experiments confirm the classical complexity–fidelity trade-off of "
            "prototype methods. Small <i>k</i> yields aggressive compression and a "
            "piecewise-constant appearance; larger <i>k</i> reduces distortion and "
            "restores chromatic nuance at the expense of a bigger palette. In "
            "mathematical terms, the feasible set of reconstructions expands with "
            "<i>k</i>, so the minimal attainable value of <i>J</i> is monotonically "
            "non-increasing in the palette size.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Concerning initialization, universal claims that one scheme is always "
            "“faster” or “better” are not warranted without measuring iteration counts "
            "and objective values over repeated trials. The evidence available here "
            "supports a more cautious statement: <i>in_pixels</i> places centroids on "
            "the data manifold and therefore tends to avoid pathological empty-cluster "
            "configurations, whereas <i>random</i> exploration can discover alternative "
            "local minima. For images with concentrated color histograms the two "
            "strategies often agree; divergence becomes more likely as <i>k</i> grows.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Several limitations should be acknowledged. First, Euclidean distance in "
            "RGB is only an approximate proxy for perceptual dissimilarity; distances "
            "in CIELAB would align more closely with human judgment. Second, forming a "
            "full distance tensor has memory cost <i>O</i>(<i>Nk</i>) and may require chunked "
            "evaluation for very large images. Third, a single photograph does not "
            "exhaust the diversity of natural scenes; a broader benchmark would "
            "strengthen statistical conclusions.",
            styles["body"],
        )
    )

    # ========================= 7. CONCLUSION =========================
    story.append(Paragraph("7. Conclusion", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    story.append(
        Paragraph(
            "This practical exercise shows that K-Means clustering provides a clear and "
            "effective mechanism for color compression. By casting pixels as points in "
            "ℝ<sup>3</sup> and minimizing a quadratic distortion criterion, one "
            "obtains a reduced palette that retains the essential visual narrative of "
            "an image. The implemented system fulfills the project requirements: a "
            "from-scratch K-Means routine with both prescribed initializations, an "
            "interactive main program supporting png/jpg/pdf export, and a systematic "
            "qualitative evaluation for multiple values of <i>k</i>.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Natural extensions include K-Means++ initialization, multi-run selection of "
            "the best local minimum, and quantitative reporting of MSE/PSNR across a "
            "curated image set. Such enhancements would further connect the algorithmic "
            "prototype developed here with contemporary practice in statistical image "
            "analysis.",
            styles["body"],
        )
    )

    # ========================= REFERENCES =========================
    story.append(Paragraph("References", styles["h1"]))
    story.append(HLine(content_width, thickness=0.8, space_before=0, space_after=8))
    refs = [
        "[1] MacQueen, J. (1967). Some methods for classification and analysis of "
        "multivariate observations. <i>Proceedings of the Fifth Berkeley Symposium on "
        "Mathematical Statistics and Probability</i>, 1, 281–297.",
        "[2] Lloyd, S. (1982). Least squares quantization in PCM. "
        "<i>IEEE Transactions on Information Theory</i>, 28(2), 129–137.",
        "[3] Arthur, D., &amp; Vassilvitskii, S. (2007). k-means++: The advantages of "
        "careful seeding. <i>Proceedings of the Eighteenth Annual ACM-SIAM Symposium "
        "on Discrete Algorithms</i>, 1027–1035.",
        "[4] Bishop, C. M. (2006). <i>Pattern Recognition and Machine Learning</i>. "
        "Springer. (Chapter 9: Mixture models and EM; background on prototype-based clustering).",
        "[5] Harris, C. R., et al. (2020). Array programming with NumPy. "
        "<i>Nature</i>, 585, 357–362. https://numpy.org/doc/",
        "[6] Clark, A., and contributors. (n.d.). <i>Pillow (PIL Fork) Documentation</i>. "
        "https://pillow.readthedocs.io/en/stable/",
        "[7] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. "
        "<i>Computing in Science &amp; Engineering</i>, 9(3), 90–95. "
        "https://matplotlib.org/stable/",
    ]
    for r in refs:
        story.append(Paragraph(r, styles["ref"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size:,} bytes, academic rebuild)")


if __name__ == "__main__":
    build()
