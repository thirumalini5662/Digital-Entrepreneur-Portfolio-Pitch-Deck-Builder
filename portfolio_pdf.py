from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.units import mm
from io import BytesIO


def create_portfolio_pdf(
    profile,
    startup,
    portfolio,
    ai_content=""
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#14233C"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontSize=14,
        leading=20,
        textColor=colors.HexColor("#456789"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#2D64B4"),
        spaceBefore=10,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#232323"),
        spaceAfter=10
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#666666")
    )

    story = []


    # ========================================================
    # COVER
    # ========================================================

    story.append(Spacer(1, 55 * mm))

    story.append(
        Paragraph(
            "DIGITAL ENTREPRENEUR",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "Portfolio",
            title_style
        )
    )

    story.append(
        Paragraph(
            startup.get(
                "startup_name",
                "Startup Name"
            ),
            subtitle_style
        )
    )

    story.append(
        Spacer(1, 10 * mm)
    )

    story.append(
        Paragraph(
            startup.get(
                "industry",
                "Industry"
            ),
            subtitle_style
        )
    )

    story.append(
        Spacer(1, 35 * mm)
    )

    story.append(
        Paragraph(
            profile.get(
                "name",
                "Entrepreneur"
            ),
            subtitle_style
        )
    )

    story.append(PageBreak())


    # ========================================================
    # ENTREPRENEUR PROFILE
    # ========================================================

    story.append(
        Paragraph(
            "1. Entrepreneur Profile",
            heading_style
        )
    )

    profile_data = [
        [
            Paragraph("<b>Name</b>", body_style),
            Paragraph(
                profile.get("name", ""),
                body_style
            )
        ],
        [
            Paragraph("<b>Role</b>", body_style),
            Paragraph(
                profile.get("role", ""),
                body_style
            )
        ],
        [
            Paragraph("<b>Email</b>", body_style),
            Paragraph(
                profile.get("email", ""),
                body_style
            )
        ],
        [
            Paragraph("<b>Phone</b>", body_style),
            Paragraph(
                profile.get("phone", ""),
                body_style
            )
        ],
        [
            Paragraph("<b>LinkedIn</b>", body_style),
            Paragraph(
                profile.get("linkedin", ""),
                body_style
            )
        ],
        [
            Paragraph("<b>Skills</b>", body_style),
            Paragraph(
                profile.get("skills", ""),
                body_style
            )
        ]
    ]

    table = Table(
        profile_data,
        colWidths=[45 * mm, 125 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#E1EEFA")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#CCCCCC")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(table)

    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph(
            "<b>Professional Bio</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            profile.get(
                "bio",
                "Professional bio not provided."
            ),
            body_style
        )
    )

    story.append(PageBreak())


    # ========================================================
    # STARTUP OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "2. Startup Overview",
            heading_style
        )
    )

    startup_items = [
        (
            "Startup Name",
            startup.get("startup_name", "")
        ),
        (
            "Industry",
            startup.get("industry", "")
        ),
        (
            "Problem",
            startup.get("problem", "")
        ),
        (
            "Solution",
            startup.get("solution", "")
        ),
        (
            "Target Market",
            startup.get("target_market", "")
        ),
        (
            "Competitive Advantage",
            startup.get("competitive_advantage", "")
        )
    ]

    for label, value in startup_items:

        story.append(
            Paragraph(
                f"<b>{label}</b>",
                heading_style
            )
        )

        story.append(
            Paragraph(
                value or "Not provided.",
                body_style
            )
        )


    # ========================================================
    # BUSINESS MODEL
    # ========================================================

    story.append(
        Paragraph(
            "3. Business Model & Market Opportunity",
            heading_style
        )
    )

    business_items = [
        (
            "Revenue Model",
            startup.get("revenue_model", "")
        ),
        (
            "Market Size",
            startup.get("market_size", "")
        ),
        (
            "Expected Growth Rate",
            startup.get("growth_rate", "")
        ),
        (
            "Current Revenue",
            startup.get("current_revenue", "")
        ),
        (
            "Funding Stage",
            startup.get("funding_stage", "")
        )
    ]

    for label, value in business_items:

        story.append(
            Paragraph(
                f"<b>{label}</b>",
                heading_style
            )
        )

        story.append(
            Paragraph(
                value or "Not provided.",
                body_style
            )
        )

    story.append(PageBreak())


    # ========================================================
    # PORTFOLIO
    # ========================================================

    story.append(
        Paragraph(
            "4. Portfolio & Case Study",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "project_name",
                "Project"
            ),
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "project_description",
                "No project description provided."
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Project Result</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "project_result",
                "No result provided."
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Major Achievements</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "achievements",
                "No achievements provided."
            ),
            body_style
        )


    )


    # ========================================================
    # CLIENTS & TESTIMONIALS
    # ========================================================

    story.append(
        Paragraph(
            "5. Clients, Users & Testimonials",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "<b>Clients / Users</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "clients",
                "No clients or users provided."
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Testimonials</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "testimonials",
                "No testimonials provided."
            ),
            body_style
        )
    )

    story.append(PageBreak())


    # ========================================================
    # ROADMAP
    # ========================================================

    story.append(
        Paragraph(
            "6. Future Roadmap",
            heading_style
        )
    )

    story.append(
        Paragraph(
            portfolio.get(
                "roadmap",
                "Future roadmap not provided."
            ),
            body_style
        )
    )


    # ========================================================
    # AI CONTENT
    # ========================================================

    if ai_content:

        story.append(
            Paragraph(
                "7. AI-Assisted Content",
                heading_style
            )
        )

        story.append(
            Paragraph(
                ai_content,
                body_style
            )
        )


    # ========================================================
    # FINAL
    # ========================================================

    story.append(
        Spacer(1, 25 * mm)
    )

    story.append(
        Paragraph(
            "Thank You",
            title_style
        )
    )

    story.append(
        Paragraph(
            startup.get(
                "startup_name",
                "Startup"
            ),
            subtitle_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer