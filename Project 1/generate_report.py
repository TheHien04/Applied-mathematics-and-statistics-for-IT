#!/usr/bin/env python3
"""Generate an academic practical report for Project 1 - Color Compression."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
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

# Serif family with broad Unicode coverage (Vietnamese + math symbols)
pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
# DejaVu Serif has no italic face here; map italic to regular for stability
pdfmetrics.registerFontFamily(
    "Body",
    normal="Body",
    bold="Body-Bold",
    italic="Body",
    boldItalic="Body-Bold",
)

ASSETS = Path(__file__).resolve().parent / "report_assets"
OUT_PDF = Path(__file__).resolve().parent / "Lab1.pdf"
ROOT = Path(__file__).resolve().parent
CLEAN = Path(__file__).resolve().parent / ".report_build"
CLEAN.mkdir(exist_ok=True)


def clean_image(src: Path, dst: Path, max_side: int = 900) -> Path:
    im = Image.open(src).convert("RGB")
    # Remove near-white borders if present
    gray = ImageOps.grayscale(im)
    bbox = ImageOps.invert(gray).getbbox()
    if bbox:
        # Expand slightly but keep inside
        l, t, r, b = bbox
        pad = 2
        l = max(0, l - pad)
        t = max(0, t - pad)
        r = min(im.width, r + pad)
        b = min(im.height, b + pad)
        im = im.crop((l, t, r, b))
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
        dst = CLEAN / f"{name}.png"
        if name == "logo":
            Image.open(src).convert("RGBA").save(dst)
        else:
            clean_image(src, dst)
        paths[name] = dst
    return paths


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_uni": ParagraphStyle(
            "cover_uni",
            parent=base["Normal"],
            fontName="Body-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "cover_faculty": ParagraphStyle(
            "cover_faculty",
            parent=base["Normal"],
            fontName="Body",
            fontSize=12,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Normal"],
            fontName="Body-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontName="Body-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontName="Body",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=4,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Body-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor("#111111"),
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Body-Bold",
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Body-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
            firstLineIndent=12,
        ),
        "body_noindent": ParagraphStyle(
            "body_noindent",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Body",
            fontSize=9.5,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=10,
        ),
        "formula": ParagraphStyle(
            "formula",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=18,
            alignment=TA_LEFT,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Body",
            fontSize=9,
            alignment=TA_CENTER,
        ),
        "table_cell": ParagraphStyle(
            "table_cell",
            parent=base["Normal"],
            fontName="Body",
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
        ),
        "table_header": ParagraphStyle(
            "table_header",
            parent=base["Normal"],
            fontName="Body-Bold",
            fontSize=9.5,
            leading=12,
            alignment=TA_CENTER,
        ),
        "ref": ParagraphStyle(
            "ref",
            parent=base["Normal"],
            fontName="Body",
            fontSize=10.5,
            leading=14,
            leftIndent=18,
            firstLineIndent=-18,
            spaceAfter=5,
            alignment=TA_JUSTIFY,
        ),
    }
    return styles


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 2:
        canvas.setFont("Body", 9)
        canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"{page}")
        canvas.setFont("Body", 8)
        canvas.drawString(2 * cm, 1.2 * cm, "MTH00051 — Practical Report 1")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Color Compression")
    canvas.restoreState()


def rl_image(path: Path, width: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    img = RLImage(str(path), width=width, height=width * (h / float(w)))
    img.hAlign = "CENTER"
    return img


def fig(path: Path, width: float, caption: str, styles):
    return KeepTogether(
        [rl_image(path, width), Paragraph(caption, styles["caption"])]
    )


def two_figs(p1: Path, c1: str, p2: Path, c2: str, styles, width=7.0 * cm):
    """Place two images side by side without nesting KeepTogether in a Table."""
    img1 = rl_image(p1, width)
    img2 = rl_image(p2, width)
    cap1 = Paragraph(c1, styles["caption"])
    cap2 = Paragraph(c2, styles["caption"])
    table = Table(
        [[img1, img2], [cap1, cap2]],
        colWidths=[width + 0.5 * cm, width + 0.5 * cm],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def build():
    assets = prepare_assets()
    styles = make_styles()

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=2.0 * cm,
        title="Practical Report 1: Color Compression",
        author="Nguyễn Thế Hiển - 22127107",
        subject="MTH00051 Applied Mathematics and Statistics",
    )

    story = []

    # ---------------- Cover ----------------
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("VIETNAM NATIONAL UNIVERSITY — HO CHI MINH CITY", styles["cover_uni"]))
    story.append(Paragraph("UNIVERSITY OF SCIENCE", styles["cover_uni"]))
    story.append(Paragraph("Faculty of Information Technology", styles["cover_faculty"]))
    story.append(RLImage(str(assets["logo"]), width=3.6 * cm, height=2.8 * cm))
    story.append(Spacer(1, 1.2 * cm))
    story.append(Paragraph("PRACTICAL REPORT 1", styles["cover_title"]))
    story.append(Paragraph("COLOR COMPRESSION<br/>VIA K-MEANS CLUSTERING", styles["cover_subtitle"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        Paragraph(
            "Course: <b>MTH00051 — Applied Mathematics and Statistics</b>",
            styles["cover_meta"],
        )
    )
    story.append(Spacer(1, 1.6 * cm))
    story.append(Paragraph("<b>Student</b>", styles["cover_meta"]))
    story.append(Paragraph("Nguyễn Thế Hiển — 22127107 — Class 22CLC08", styles["cover_meta"]))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("<b>Instructors</b>", styles["cover_meta"]))
    story.append(Paragraph("Mr. Vũ Quốc Hoàng", styles["cover_meta"]))
    story.append(Paragraph("Mr. Nguyễn Văn Quang Huy", styles["cover_meta"]))
    story.append(Paragraph("Mr. Nguyễn Ngọc Toàn", styles["cover_meta"]))
    story.append(Paragraph("Mrs. Phan Thị Phương Uyên", styles["cover_meta"]))
    story.append(Spacer(1, 2.0 * cm))
    story.append(Paragraph("Ho Chi Minh City, 2024", styles["cover_meta"]))
    story.append(PageBreak())

    # ---------------- Abstract ----------------
    story.append(Paragraph("Abstract", styles["h1"]))
    story.append(
        Paragraph(
            "This report investigates color quantization of digital RGB images through "
            "the K-Means clustering algorithm implemented from first principles in Python. "
            "Each pixel is treated as a point in <font face='Body'>R</font><super>3</super>, "
            "and the algorithm partitions the color space into <font face='Body'>k</font> "
            "clusters whose centroids form a reduced palette. Replacing every pixel by its "
            "nearest centroid yields a compressed representation that preserves global visual "
            "structure while substantially decreasing the number of distinct colors.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "We formalize the optimization objective, describe two centroid-initialization "
            "strategies (<font face='Body'>random</font> and "
            "<font face='Body'>in_pixels</font>), and evaluate qualitative results "
            "for <font face='Body'>k</font> in {3, 5, 7}. Empirical observations "
            "indicate that larger <font face='Body'>k</font> recovers finer tonal "
            "gradations, whereas initialization primarily affects the attained local "
            "minimum of the within-cluster sum of squares. The study illustrates how a "
            "classical unsupervised learning method connects linear algebra, distance "
            "geometry, and practical image processing.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Keywords:</b> color quantization, K-Means clustering, Euclidean distance, "
            "image compression, unsupervised learning.",
            styles["body_noindent"],
        )
    )
    story.append(PageBreak())

    # ---------------- TOC ----------------
    story.append(Paragraph("Table of Contents", styles["h1"]))
    toc_items = [
        "1. Introduction ............................................................. 4",
        "2. Problem Formulation ...................................................... 4",
        "3. Theoretical Background ................................................... 5",
        "   3.1. K-Means as an Optimization Procedure ................................ 5",
        "   3.2. Centroid Initialization Strategies .................................. 5",
        "4. Implementation ........................................................... 6",
        "   4.1. Software Environment and Libraries .................................. 6",
        "   4.2. Functional Design ................................................... 6",
        "   4.3. Main Program Workflow ............................................... 7",
        "5. Experimental Results ..................................................... 8",
        "   5.1. Experimental Setup .................................................. 8",
        "   5.2. Visual Comparison for k = 3, 5, 7 ................................... 8",
        "6. Discussion ............................................................... 10",
        "7. Conclusion ............................................................... 11",
        "References .................................................................. 11",
    ]
    for item in toc_items:
        story.append(Paragraph(item.replace(" ", "&nbsp;"), styles["toc"]))
    story.append(PageBreak())

    # ---------------- 1. Introduction ----------------
    story.append(Paragraph("1. Introduction", styles["h1"]))
    story.append(Paragraph("1.1. Student Information", styles["h2"]))
    info = [
        [Paragraph("<b>Full name</b>", styles["table_cell"]), Paragraph("Nguyễn Thế Hiển", styles["table_cell"])],
        [Paragraph("<b>Student ID</b>", styles["table_cell"]), Paragraph("22127107", styles["table_cell"])],
        [Paragraph("<b>Class</b>", styles["table_cell"]), Paragraph("22CLC08", styles["table_cell"])],
        [Paragraph("<b>Course</b>", styles["table_cell"]), Paragraph("MTH00051 — Applied Mathematics and Statistics", styles["table_cell"])],
    ]
    t = Table(info, colWidths=[4.2 * cm, 11.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.6, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f3f3")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("1.2. Motivation", styles["h2"]))
    story.append(
        Paragraph(
            "A color digital image is commonly stored as an array of pixels in the RGB "
            "model. Each channel is encoded by one byte, so a single pixel belongs to a "
            "discrete cube {0, 1, ..., 255}<super>3</super> containing up to "
            "256<super>3</super> ~ 1.68 x 10<super>7</super> possible colors. In natural "
            "photographs the number of distinct colors is typically far smaller than this "
            "upper bound, yet still large enough to inflate storage cost and bandwidth "
            "usage. Color compression (also called color quantization) seeks a compact "
            "palette of <font face='Body'>k</font> representative colors such that "
            "the reconstructed image remains visually faithful to the original.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "From a statistical learning perspective, the task is an unsupervised "
            "clustering problem: similar colors should be grouped, and each group should "
            "be summarized by a prototype. K-Means provides a transparent and "
            "computationally tractable solution, making it an instructive bridge between "
            "applied mathematics and practical computing.",
            styles["body"],
        )
    )

    # ---------------- 2. Problem Formulation ----------------
    story.append(Paragraph("2. Problem Formulation", styles["h1"]))
    story.append(
        Paragraph(
            "Let an RGB image of height <font face='Body'>H</font> and width "
            "<font face='Body'>W</font> be represented by the set of pixel vectors",
            styles["body_noindent"],
        )
    )
    story.append(
        Paragraph(
            "X = { x<sub>i</sub> in R<super>3</super> | i = 1, ..., N }, N = H . W.",
            styles["formula"],
        )
    )
    story.append(
        Paragraph(
            "Given a positive integer <font face='Body'>k</font>, the goal is to "
            "compute centroids C = { c<sub>1</sub>, ..., c<sub>k</sub> } subset R<super>3</super> "
            "and an assignment function l : {1, ..., N} -> {1, ..., k} that minimize the "
            "within-cluster sum of squares (WCSS)",
            styles["body_noindent"],
        )
    )
    story.append(
        Paragraph(
            "J(C, l) = sum<sub>i=1</sub><super>N</super> || x<sub>i</sub> - c<sub>l(i)</sub> ||<super>2</super><sub>2</sub>.",
            styles["formula"],
        )
    )
    story.append(
        Paragraph(
            "After optimization, the compressed image is obtained by the reconstruction "
            "x̂<sub>i</sub> = c<sub>l(i)</sub>. Consequently, the image uses at most "
            "<font face='Body'>k</font> colors. The reconstruction quality may be "
            "quantified by the mean squared error (MSE)",
            styles["body_noindent"],
        )
    )
    story.append(
        Paragraph(
            "MSE = (1/N) sum<sub>i=1</sub><super>N</super> || x<sub>i</sub> - x̂<sub>i</sub> ||<super>2</super><sub>2</sub>,",
            styles["formula"],
        )
    )
    story.append(
        Paragraph(
            "which coincides with J(C, l)/N. Lower MSE indicates a closer approximation "
            "in RGB Euclidean geometry; perceptual quality, however, also depends on "
            "human vision and is therefore assessed visually in Section 5.",
            styles["body"],
        )
    )

    # ---------------- 3. Theory ----------------
    story.append(Paragraph("3. Theoretical Background", styles["h1"]))
    story.append(Paragraph("3.1. K-Means as an Optimization Procedure", styles["h2"]))
    story.append(
        Paragraph(
            "Exact minimization of J is NP-hard in general. The classical Lloyd iteration "
            "alternates two conditional updates that are each optimal given the other:",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Assignment step.</b> For fixed centroids, every pixel is assigned to the "
            "nearest centroid under the Euclidean metric:",
            styles["body_noindent"],
        )
    )
    story.append(
        Paragraph(
            "l(i) = arg min<sub>jin{1,...,k}</sub> || x<sub>i</sub> - c<sub>j</sub> ||<super>2</super><sub>2</sub>.",
            styles["formula"],
        )
    )
    story.append(
        Paragraph(
            "<b>Update step.</b> For a fixed assignment, each centroid is replaced by the "
            "sample mean of its members, which is the unique minimizer of the quadratic "
            "loss on that cluster:",
            styles["body_noindent"],
        )
    )
    story.append(
        Paragraph(
            "c<sub>j</sub> <- (1/|S<sub>j</sub>|) sum<sub>iinS<sub>j</sub></sub> x<sub>i</sub>, "
            "S<sub>j</sub> = { i | l(i) = j },",
            styles["formula"],
        )
    )
    story.append(
        Paragraph(
            "provided S<sub>j</sub> is nonempty. If a cluster becomes empty, the "
            "implementation retains the previous centroid to preserve numerical stability. "
            "The iteration continues until the centroids stabilize (within a prescribed "
            "tolerance) or a maximum iteration budget is reached. Because each step does "
            "not increase J, the sequence of objective values is monotonically "
            "non-increasing and converges to a local minimum.",
            styles["body"],
        )
    )

    story.append(Paragraph("3.2. Centroid Initialization Strategies", styles["h2"]))
    story.append(
        Paragraph(
            "K-Means is sensitive to the initial configuration of centroids. This project "
            "implements two initialization schemes required by the assignment:",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>random.</b> Each centroid coordinate is sampled independently and "
            "uniformly from [0, 255]. This explores the full RGB cube and may place "
            "prototypes far from the empirical color support of the image, occasionally "
            "producing empty clusters in early iterations.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>in_pixels.</b> Centroids are sampled uniformly without replacement from "
            "the observed pixels. The initial palette therefore lies inside the convex "
            "hull of the data, which typically yields a more favorable starting value of "
            "J and more stable early assignments.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Neither scheme guarantees a global optimum. In practice, comparing both "
            "initializations for the same <font face='Body'>k</font> provides "
            "insight into the variability of local solutions.",
            styles["body"],
        )
    )

    # ---------------- 4. Implementation ----------------
    story.append(Paragraph("4. Implementation", styles["h1"]))
    story.append(Paragraph("4.1. Software Environment and Libraries", styles["h2"]))
    story.append(
        Paragraph(
            "The program is developed in a Jupyter Notebook environment using only the "
            "libraries permitted by the course specification:",
            styles["body"],
        )
    )
    lib_data = [
        [
            Paragraph("<b>Library</b>", styles["table_header"]),
            Paragraph("<b>Role in the project</b>", styles["table_header"]),
        ],
        [
            Paragraph("NumPy", styles["table_cell"]),
            Paragraph(
                "Vectorized matrix computation for distance evaluation, centroid updates, and array reshaping.",
                styles["table_cell"],
            ),
        ],
        [
            Paragraph("Pillow (PIL)", styles["table_cell"]),
            Paragraph(
                "Image input/output, RGB conversion, and export to png/jpg/pdf.",
                styles["table_cell"],
            ),
        ],
        [
            Paragraph("Matplotlib", styles["table_cell"]),
            Paragraph(
                "Visualization of original and reconstructed images.",
                styles["table_cell"],
            ),
        ],
    ]
    lib_table = Table(lib_data, colWidths=[3.5 * cm, 12.2 * cm])
    lib_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(lib_table)
    story.append(Spacer(1, 0.15 * cm))
    story.append(
        Paragraph(
            "Pre-built clustering routines (for example, "
            "<font face='Courier'>sklearn.cluster.KMeans</font>) are deliberately "
            "excluded from the submission, in accordance with the project constraints.",
            styles["body"],
        )
    )

    story.append(Paragraph("4.2. Functional Design", styles["h2"]))
    story.append(
        Paragraph(
            "The implementation is organized into small, reusable functions with explicit "
            "docstrings. The principal components are summarized below.",
            styles["body"],
        )
    )

    funcs = [
        ("<b>read_img(img_path)</b>",
         "Opens an image file, converts it to the RGB color space, and returns a "
         "floating-point NumPy array of shape (H, W, 3). Explicit RGB conversion "
         "avoids channel inconsistencies arising from RGBA or palette-based images."),
        ("<b>show_img(img_2d)</b>",
         "Displays an image with Matplotlib and suppresses coordinate axes to focus "
         "on visual content."),
        ("<b>save_img(img_2d, img_path)</b>",
         "Clips intensities to [0, 255], casts to 8-bit integers, and writes the image "
         "to disk."),
        ("<b>convert_img_to_1d(img_2d)</b>",
         "Reshapes the image into an (N, 3) design matrix so that each row is a pixel "
         "feature vector suitable for clustering."),
        ("<b>kmeans(img_1d, k_clusters, max_iter, init_centroids)</b>",
         "Executes Lloyd iteration with the selected initialization. Distances are "
         "computed via squared Euclidean norms; convergence is declared when centroid "
         "coordinates change by less than 10<super>-4</super> in absolute value."),
        ("<b>generate_2d_img(img_2d_shape, centroids, labels)</b>",
         "Maps every pixel to its centroid color and restores the original spatial "
         "shape (H, W, 3)."),
        ("<b>reconstruction_error(img_1d, centroids, labels)</b>",
         "Returns the MSE between original pixels and their reconstructed colors, "
         "providing a quantitative complement to visual inspection."),
    ]
    for title, desc in funcs:
        story.append(Paragraph(title, styles["h3"]))
        story.append(Paragraph(desc, styles["body_noindent"]))

    story.append(Paragraph("4.3. Main Program Workflow", styles["h2"]))
    story.append(
        Paragraph(
            "The interactive <font face='Courier'>main</font> procedure satisfies the "
            "course interface requirements. At each execution the user provides:",
            styles["body"],
        )
    )
    bullets = [
        "the input image path;",
        "the number of clusters <font face='Body'>k</font>;",
        "the maximum number of iterations;",
        "the centroid initialization mode (<font face='Body'>random</font>, "
        "<font face='Body'>in_pixels</font>, or both);",
        "the output format chosen from {png, jpg, pdf};",
        "the base filename used for saving reconstructed images.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(b, styles["body_noindent"]), leftIndent=10) for b in bullets],
            bulletType="bullet",
            start="•",
        )
    )
    story.append(Spacer(1, 0.1 * cm))
    story.append(
        Paragraph(
            "The pipeline then reads and flattens the image, runs K-Means for each "
            "requested initialization, displays the reconstructed result, reports the "
            "MSE, and exports the file in the selected format. Supporting unit-style "
            "checks are collected in <font face='Courier'>test_functions</font>.",
            styles["body"],
        )
    )

    # ---------------- 5. Experiments ----------------
    story.append(Paragraph("5. Experimental Results", styles["h1"]))
    story.append(Paragraph("5.1. Experimental Setup", styles["h2"]))
    story.append(
        Paragraph(
            "Experiments are conducted on a natural beach photograph containing smooth "
            "illumination gradients (sky and water) together with a high-contrast "
            "silhouette. Such content is informative for color quantization: coarse "
            "palettes tend to posterize the sky, while larger palettes restore "
            "intermediate tones. Unless otherwise stated, both initialization strategies "
            "are executed for <font face='Body'>k</font> in {3, 5, 7} with a "
            "sufficient iteration budget to reach practical convergence.",
            styles["body"],
        )
    )
    story.append(fig(assets["original"], 9.5 * cm, "Figure 1. Original test image prior to color compression.", styles))

    story.append(Paragraph("5.2. Visual Comparison for k = 3, 5, 7", styles["h2"]))
    story.append(
        Paragraph(
            "Figure 2 presents reconstructions for <font face='Body'>k</font> = 3. "
            "With only three palette colors, both initializations reduce the scene to a "
            "silhouette, a mid-tone band, and a sky tone. Fine reflections on the water "
            "are largely suppressed, yet the semantic layout of the photograph remains "
            "recognizable. The two methods produce closely related visual outcomes, "
            "suggesting that the dominant modes of the color distribution are stable.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k3_in"],
            "Figure 2a. Reconstruction with in_pixels initialization, k = 3.",
            assets["k3_rand"],
            "Figure 2b. Reconstruction with random initialization, k = 3.",
            styles,
        )
    )

    story.append(
        Paragraph(
            "For <font face='Body'>k</font> = 5 (Figure 3), additional centroids "
            "capture transitional hues near the horizon and richer water reflections. "
            "Differences between initialization schemes become more noticeable: random "
            "initialization may allocate a centroid to a less frequent region of RGB "
            "space, slightly altering the tonal balance relative to in_pixels.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k5_in"],
            "Figure 3a. Reconstruction with in_pixels initialization, k = 5.",
            assets["k5_rand"],
            "Figure 3b. Reconstruction with random initialization, k = 5.",
            styles,
        )
    )

    story.append(
        Paragraph(
            "When <font face='Body'>k</font> = 7 (Figure 4), the reconstructions "
            "approach the original more closely. Gradients in the sky and specular "
            "highlights on wet sand reappear as distinct palette entries. Residual "
            "discrepancies between the two initializations illustrate that K-Means may "
            "converge to distinct local minima even for moderate <font face='Body'>k</font>.",
            styles["body"],
        )
    )
    story.append(
        two_figs(
            assets["k7_in"],
            "Figure 4a. Reconstruction with in_pixels initialization, k = 7.",
            assets["k7_rand"],
            "Figure 4b. Reconstruction with random initialization, k = 7.",
            styles,
        )
    )

    # Qualitative summary table
    story.append(Paragraph("5.3. Qualitative Summary", styles["h2"]))
    summary = [
        [
            Paragraph("<b>k</b>", styles["table_header"]),
            Paragraph("<b>Visual fidelity</b>", styles["table_header"]),
            Paragraph("<b>Observed effect of initialization</b>", styles["table_header"]),
        ],
        [
            Paragraph("3", styles["table_cell"]),
            Paragraph("Strong posterization; content preserved at a coarse level.", styles["table_cell"]),
            Paragraph("Minor differences; dominant colors are consistently recovered.", styles["table_cell"]),
        ],
        [
            Paragraph("5", styles["table_cell"]),
            Paragraph("Improved mid-tones and horizon detail.", styles["table_cell"]),
            Paragraph("Noticeable palette shifts between random and in_pixels.", styles["table_cell"]),
        ],
        [
            Paragraph("7", styles["table_cell"]),
            Paragraph("Closer to the original; smoother apparent gradients.", styles["table_cell"]),
            Paragraph("Local minima remain visible but less disruptive perceptually.", styles["table_cell"]),
        ],
    ]
    st = Table(summary, colWidths=[1.5 * cm, 7.0 * cm, 7.2 * cm])
    st.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(st)

    # ---------------- 6. Discussion ----------------
    story.append(Paragraph("6. Discussion", styles["h1"]))
    story.append(
        Paragraph(
            "The experiments confirm the classical bias–complexity trade-off of prototype "
            "methods. Small <font face='Body'>k</font> yields aggressive "
            "compression and a piecewise-constant appearance; large "
            "<font face='Body'>k</font> reduces MSE and restores chromatic "
            "nuance at the expense of a larger palette. In mathematical terms, the "
            "feasible set of reconstructions expands with <font face='Body'>k</font>, "
            "so the minimal attainable value of J is monotonically non-increasing in "
            "<font face='Body'>k</font>.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Regarding initialization, claims that one scheme is universally “faster” or "
            "“better” are not justified without measuring iteration counts and objective "
            "values over repeated trials. The evidence available here supports a more "
            "cautious statement: <font face='Body'>in_pixels</font> places "
            "centroids on the data manifold and therefore tends to avoid pathological "
            "empty-cluster configurations, whereas <font face='Body'>random</font> "
            "initialization explores a broader region of parameter space and can discover "
            "alternative local minima. For images with highly concentrated color "
            "histograms, the two strategies often agree; for images with multiple chromatic "
            "modes, divergence is more likely as <font face='Body'>k</font> grows.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Several limitations should be acknowledged. First, Euclidean distance in RGB "
            "is only an approximate proxy for perceptual dissimilarity; distances in "
            "CIELAB would align more closely with human judgment. Second, full pairwise "
            "distance tensors have memory cost O(Nk), which may be mitigated by chunked "
            "distance computation for very large images. Third, a single photograph does "
            "not exhaust the diversity of natural scenes; a broader benchmark would "
            "strengthen statistical conclusions.",
            styles["body"],
        )
    )

    # ---------------- 7. Conclusion ----------------
    story.append(Paragraph("7. Conclusion", styles["h1"]))
    story.append(
        Paragraph(
            "This practical exercise demonstrates that K-Means clustering provides an "
            "elegant and effective mechanism for color compression. By casting pixels as "
            "points in R<super>3</super> and minimizing a quadratic distortion criterion, "
            "one obtains a reduced palette that retains the essential visual narrative of "
            "an image. The implemented system fulfills the project requirements: a "
            "from-scratch K-Means routine with both prescribed initializations, an "
            "interactive main program supporting png/jpg/pdf export, and a systematic "
            "qualitative evaluation for multiple values of <font face='Body'>k</font>.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "Future extensions include K-Means++ initialization, multi-run selection of "
            "the best local minimum, and quantitative reporting of MSE/PSNR across a "
            "curated image set. Such enhancements would further connect the algorithmic "
            "prototype developed here with contemporary practice in statistical image "
            "analysis.",
            styles["body"],
        )
    )

    # ---------------- References ----------------
    story.append(Paragraph("References", styles["h1"]))
    refs = [
        "[1] MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. "
        "<font face='Body'>Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics "
        "and Probability</font>, 1, 281–297. (Foundational formulation of K-Means-type clustering.)",
        "[2] Lloyd, S. (1982). Least squares quantization in PCM. "
        "<font face='Body'>IEEE Transactions on Information Theory</font>, 28(2), 129–137. "
        "(Classical alternating minimization procedure used in this report.)",
        "[3] Wikipedia contributors. (n.d.). <font face='Body'>K-means clustering</font>. "
        "Wikipedia. https://en.wikipedia.org/wiki/K-means_clustering "
        "(Accessed for algorithmic overview and terminology.)",
        "[4] Harris, C. R., et al. (2020). Array programming with NumPy. "
        "<font face='Body'>Nature</font>, 585, 357–362. https://numpy.org/doc/ "
        "(Numerical backbone of the implementation.)",
        "[5] Clark, A., and contributors. (n.d.). <font face='Body'>Pillow (PIL Fork) Documentation</font>. "
        "https://pillow.readthedocs.io/en/stable/ (Image reading, writing, and format conversion.)",
        "[6] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. "
        "<font face='Body'>Computing in Science &amp; Engineering</font>, 9(3), 90–95. "
        "https://matplotlib.org/stable/ (Visualization of experimental results.)",
    ]
    for r in refs:
        story.append(Paragraph(r, styles["ref"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
