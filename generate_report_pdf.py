import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "PocketSmart_AI_Project_Report_22_Pages.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Don't draw header on Page 1 (Title Cover)
        if self._pageNumber > 1:
            self.drawString(54, 755, "PocketSmart AI | Comprehensive Technical Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
            
        # Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "PocketSmart AI — Generative AI with Google")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")   # Deep navy blue
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_neutral = colors.HexColor("#1F2937")    # Charcoal body text
    card_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_neutral,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'ReportCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        leftIndent=10,
        rightIndent=10,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE PAGE & PROJECT METADATA
    # ==========================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("PocketSmart AI", title_style))
    story.append(Paragraph("Your Smart Budget &amp; Recommendation Assistant", subtitle_style))
    story.append(Paragraph(
        "<b>An Integrated Generative AI Application for Personal Budgeting, Home Planning, Event Budgeting, and Jewelry Recommendations</b>",
        ParagraphStyle('MetaDesc', parent=body_style, alignment=1, fontSize=10, leading=14, spaceAfter=18)
    ))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Project Detail</b>", body_style), Paragraph("<b>Specification / Information</b>", body_style)],
        [Paragraph("<b>Project Name</b>", body_style), Paragraph("PocketSmart AI", body_style)],
        [Paragraph("<b>Domain</b>", body_style), Paragraph("Generative AI, Personal Finance, Rule-Based &amp; Recommendation Systems", body_style)],
        [Paragraph("<b>Technology Track</b>", body_style), Paragraph("Generative AI with Google (Google AI Studio Track)", body_style)],
        [Paragraph("<b>Project Team</b>", body_style), Paragraph("<b>Krithick</b> (Team Lead), <b>Dhatchayini</b>, <b>Dharshini</b>, <b>Harrish Balaji</b>", body_style)],
        [Paragraph("<b>Institution</b>", body_style), Paragraph("KPR College of Arts Science and Research<br/>(Affiliated to Bharathiar University, Coimbatore, Tamil Nadu)", body_style)],
        [Paragraph("<b>Live Application</b>", body_style), Paragraph("https://pocketsmart-ai-ba9w.onrender.com", body_style)],
        [Paragraph("<b>Source Code</b>", body_style), Paragraph("https://github.com/swe1142007-bot/PocketSmart-AI", body_style)],
        [Paragraph("<b>Academic Report Period</b>", body_style), Paragraph("October 2026 | Comprehensive Capstone Report (22-Page Full Standard)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[130, 374])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Executive Overview", h1_style))
    story.append(Paragraph(
        "<b>PocketSmart AI</b> bridges a critical divide in modern consumer software: the disconnect between quantitative arithmetic and qualitative everyday planning. Traditional spreadsheets require manual upkeep without providing contextual reasoning, while standalone Large Language Models (LLMs) frequently hallucinate numerical totals. PocketSmart AI resolves this challenge by strictly isolating deterministic mathematical calculations in Python, while deploying Google Gemini exclusively as an analytical reasoning layer to deliver contextual financial health assessments, lifestyle budget allocations, and external product search directions.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: CERTIFICATE OF ORIGINALITY & DECLARATION
    # ==========================================
    story.append(Paragraph("Certificate of Authenticity", h1_style))
    story.append(Paragraph(
        "This is to certify that the project report entitled <b>\"PocketSmart AI: Your Smart Budget &amp; Recommendation Assistant\"</b> submitted by <b>Krithick (Team Lead), Dhatchayini, Dharshini, and Harrish Balaji</b> in partial fulfillment of the project requirements under the <b>Generative AI with Google</b> track, affiliated with <b>Bharathiar University, Coimbatore</b>, is a bona fide record of original research and engineering work completed by the team.",
        body_style
    ))
    story.append(Paragraph(
        "The algorithmic architectures, system implementations, test assertions, and integration protocols documented in this report represent the independent engineering work of the candidate team, tested and hosted at the official deployment URL.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Candidate Declaration &amp; Responsibilities", h1_style))
    story.append(Paragraph(
        "We hereby declare that this technical project report is our authentic work. All external APIs, foundational open-source libraries, and academic citations have been documented with full compliance and standard attribution.",
        body_style
    ))

    team_data = [
        [Paragraph("<b>Candidate Name</b>", body_style), Paragraph("<b>Assigned Engineering Role</b>", body_style), Paragraph("<b>Key Contributions</b>", body_style)],
        [Paragraph("<b>Krithick</b>", body_style), Paragraph("Team Lead &amp; System Architect", body_style), Paragraph("System design, backend pipeline, Gemini API orchestration, and deployment", body_style)],
        [Paragraph("<b>Dhatchayini</b>", body_style), Paragraph("Algorithmic Engine &amp; Prompt Engineer", body_style), Paragraph("Deterministic arithmetic core, prompt templates, structured output parsing", body_style)],
        [Paragraph("<b>Dharshini</b>", body_style), Paragraph("UI/UX &amp; Frontend Engineer", body_style), Paragraph("Responsive web interface, data entry forms, real-time client validation", body_style)],
        [Paragraph("<b>Harrish Balaji</b>", body_style), Paragraph("Quality Assurance, DevOps &amp; Security", body_style), Paragraph("Test suites, boundary stress tests, Render deployment, cloud secrets &amp; search integrations", body_style)],
    ]
    team_table = Table(team_data, colWidths=[90, 160, 254])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Acknowledgements", h1_style))
    story.append(Paragraph(
        "We express our sincere gratitude to <b>KPR College of Arts Science and Research</b> and <b>Bharathiar University</b> for offering the lab facilities and administrative support necessary for this project. We also thank the Google AI Studio developer community and our faculty mentors whose ongoing reviews helped refine the architecture of PocketSmart AI.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: TABLE OF CONTENTS & LIST OF TABLES
    # ==========================================
    story.append(Paragraph("Table of Contents", h1_style))

    toc_data = [
        [Paragraph("<b>Chapter / Section Heading</b>", body_style), Paragraph("<b>Page</b>", body_style)],
        [Paragraph("Title Page &amp; Project Metadata", body_style), Paragraph("1", body_style)],
        [Paragraph("Certificate of Authenticity, Team Declaration &amp; Acknowledgements", body_style), Paragraph("2", body_style)],
        [Paragraph("Table of Contents &amp; Document Index", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>Chapter 1:</b> Introduction &amp; Domain Overview", body_style), Paragraph("4", body_style)],
        [Paragraph("<b>Chapter 2:</b> Problem Formulation &amp; Industry Gap Analysis", body_style), Paragraph("5", body_style)],
        [Paragraph("<b>Chapter 3:</b> Objectives, Project Scope &amp; Feasibility Study", body_style), Paragraph("6", body_style)],
        [Paragraph("<b>Chapter 4:</b> Requirement Specifications &amp; User Personas", body_style), Paragraph("7", body_style)],
        [Paragraph("<b>Chapter 5:</b> System Architecture &amp; Decoupled Design Principles", body_style), Paragraph("8", body_style)],
        [Paragraph("<b>Chapter 6:</b> Behavioral Modeling &amp; Data Flow Diagrams (DFD)", body_style), Paragraph("9", body_style)],
        [Paragraph("<b>Chapter 7:</b> Mathematical Foundations &amp; Deterministic Algorithms", body_style), Paragraph("10", body_style)],
        [Paragraph("<b>Chapter 8:</b> Module Specification I — Personal Budget Engine", body_style), Paragraph("11", body_style)],
        [Paragraph("<b>Chapter 9:</b> Module Specification II — Event &amp; Celebration Budget Planner", body_style), Paragraph("12", body_style)],
        [Paragraph("<b>Chapter 10:</b> Module Specification III — Home Interior &amp; Space Planner", body_style), Paragraph("13", body_style)],
        [Paragraph("<b>Chapter 11:</b> Module Specification IV — Jewelry Stylist &amp; Multimodal Engine", body_style), Paragraph("14", body_style)],
        [Paragraph("<b>Chapter 12:</b> Generative AI Integration &amp; Prompt Engineering", body_style), Paragraph("15", body_style)],
        [Paragraph("<b>Chapter 13:</b> Data Structures, Payloads &amp; Validation Layers", body_style), Paragraph("16", body_style)],
        [Paragraph("<b>Chapter 14:</b> User Interface &amp; Human-Computer Interaction Design", body_style), Paragraph("17", body_style)],
        [Paragraph("<b>Chapter 15:</b> Application Walkthroughs &amp; Real-World Scenarios", body_style), Paragraph("18", body_style)],
        [Paragraph("<b>Chapter 16:</b> Verification, Automated Test Suite &amp; Security Audits", body_style), Paragraph("19", body_style)],
        [Paragraph("<b>Chapter 17:</b> Cloud Deployment, Containerization &amp; DevOps on Render", body_style), Paragraph("20", body_style)],
        [Paragraph("<b>Chapter 18:</b> Technical Challenges, Risk Mitigation &amp; Future Scope", body_style), Paragraph("21", body_style)],
        [Paragraph("<b>Chapter 19:</b> Conclusion, Compliance References &amp; Appendices", body_style), Paragraph("22", body_style)],
    ]
    toc_table = Table(toc_data, colWidths=[420, 84])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: CHAPTER 1 — INTRODUCTION & DOMAIN OVERVIEW
    # ==========================================
    story.append(Paragraph("Chapter 1: Introduction &amp; Domain Overview", h1_style))
    story.append(Paragraph("1.1 Background and Paradigm Shift", h2_style))
    story.append(Paragraph(
        "Modern consumer budgeting has historically been divided into two separate paradigms: manual spreadsheet accounting and automated aggregator platforms. While spreadsheets require time-consuming manual upkeep and lack qualitative guidance, automated aggregators produce static graphs without contextual reasoning. The advent of Large Language Models (LLMs) offers new possibilities for conversational assistants. However, raw LLMs are inherently non-deterministic and frequently hallucinate basic arithmetic calculations.",
        body_style
    ))
    story.append(Paragraph(
        "<b>PocketSmart AI</b> bridges this gap through a clean <b>Separation of Concerns (SoC)</b>: all mathematical computations are evaluated strictly in Python on the backend, while Google Gemini is deployed exclusively to interpret the resulting figures and provide natural-language context.",
        body_style
    ))

    story.append(Paragraph("1.2 The Multi-Domain Vision", h2_style))
    story.append(Paragraph(
        "Rather than treating financial management as an isolated ledger exercise, PocketSmart AI organizes budgeting around four everyday lifestyle scenarios:",
        body_style
    ))

    module_overview_data = [
        [Paragraph("<b>Module Domain</b>", body_style), Paragraph("<b>Core Analytical Focus</b>", body_style), Paragraph("<b>Key Deliverable</b>", body_style)],
        [Paragraph("<b>1. Personal Finance</b>", body_style), Paragraph("Evaluates monthly income, expenses, and savings targets.", body_style), Paragraph("Deterministic balances, category shares, and savings plans.", body_style)],
        [Paragraph("<b>2. Home Space Planning</b>", body_style), Paragraph("Allocates room renovation budgets by style and priority.", body_style), Paragraph("Tiered furniture breakdowns with price estimates.", body_style)],
        [Paragraph("<b>3. Event &amp; Celebrations</b>", body_style), Paragraph("Distributes event budgets across venue, food, decor, and media.", body_style), Paragraph("Per-guest cost breakdowns with reserve contingency buffers.", body_style)],
        [Paragraph("<b>4. Jewelry Stylist</b>", body_style), Paragraph("Matches jewelry recommendations to budget, metal, and outfits.", body_style), Paragraph("Aesthetic suggestions with optional visual color analysis.", body_style)],
    ]
    mod_table = Table(module_overview_data, colWidths=[120, 204, 180])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 Core Innovation Highlights", h2_style))
    story.append(Paragraph("• <b>Deterministic Math Engine:</b> Guarantees zero arithmetic hallucination by calculating all totals on the backend.", bullet_style))
    story.append(Paragraph("• <b>Contextual AI Reasoning:</b> Uses Google Gemini to turn raw figures into clear, actionable advice.", bullet_style))
    story.append(Paragraph("• <b>Ethical Pricing Transparency:</b> Clearly distinguishes estimated prices from verified market rates, using search links instead of false inventory claims.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: CHAPTER 2 — PROBLEM FORMULATION & GAP ANALYSIS
    # ==========================================
    story.append(Paragraph("Chapter 2: Problem Formulation &amp; Industry Gap Analysis", h1_style))
    story.append(Paragraph("2.1 The Consumer Dilemma", h2_style))
    story.append(Paragraph(
        "Consumers often know their top-line income or spending limits, but struggle to translate those numbers into practical financial choices. Calculating a remaining surplus is straightforward, but deciding how to allocate funds across competing categories often causes friction. For instance, when planning a room renovation or wedding anniversary, consumers must balance multiple interdependent choices without exceeding their budget.",
        body_style
    ))
    story.append(Paragraph(
        "Without structured guidance, consumers face two common pitfalls: <i>numerical isolation</i> (viewing numbers without context) and <i>qualitative paralysis</i> (becoming overwhelmed by endless shopping options and hidden costs).",
        body_style
    ))

    story.append(Paragraph("2.2 Industry Gap &amp; Comparative Analysis", h2_style))
    story.append(Paragraph(
        "Current market tools generally fall into three categories, each with notable limitations:",
        body_style
    ))

    comp_data = [
        [Paragraph("<b>Evaluation Dimension</b>", body_style), Paragraph("<b>Manual Spreadsheets</b>", body_style), Paragraph("<b>Standalone Raw LLMs</b>", body_style), Paragraph("<b>PocketSmart AI Platform</b>", body_style)],
        [Paragraph("<b>Arithmetic Precision</b>", body_style), Paragraph("100% (Formulas)", body_style), Paragraph("Inconsistent (Prone to drift)", body_style), Paragraph("<b>100% Deterministic Server Core</b>", body_style)],
        [Paragraph("<b>Contextual Guidance</b>", body_style), Paragraph("None (Manual)", body_style), Paragraph("High (Natural language)", body_style), Paragraph("<b>High (Google Gemini Engine)</b>", body_style)],
        [Paragraph("<b>Lifestyle Planning</b>", body_style), Paragraph("Rigid templates", body_style), Paragraph("Unstructured text", body_style), Paragraph("<b>4 Dedicated Specialized Modules</b>", body_style)],
        [Paragraph("<b>Data Privacy</b>", body_style), Paragraph("Local files", body_style), Paragraph("Entire prompts exposed", body_style), Paragraph("<b>Sanitized vectors; keys protected</b>", body_style)],
        [Paragraph("<b>Pricing Authenticity</b>", body_style), Paragraph("N/A", body_style), Paragraph("Often fabricates live rates", body_style), Paragraph("<b>Labeled estimates + search links</b>", body_style)],
    ]
    comp_table = Table(comp_data, colWidths=[100, 110, 134, 160])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.3 Summary of Key Challenges Addressed", h2_style))
    story.append(Paragraph("• <b>Arithmetic Drift in LLMs:</b> Prevents math errors by keeping calculations inside Python.", bullet_style))
    story.append(Paragraph("• <b>Generic Advice:</b> Tailors recommendations to user-submitted budgets, priorities, and goals.", bullet_style))
    story.append(Paragraph("• <b>Unrealistic Pricing:</b> Labels all AI-generated prices as estimates and routes users to search queries.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: CHAPTER 3 — OBJECTIVES, SCOPE & FEASIBILITY STUDY
    # ==========================================
    story.append(Paragraph("Chapter 3: Objectives, Project Scope &amp; Feasibility Study", h1_style))
    story.append(Paragraph("3.1 Core Project Objectives", h2_style))
    story.append(Paragraph(
        "PocketSmart AI was developed around a clear set of technical and functional goals:",
        body_style
    ))
    story.append(Paragraph("1. <b>Deterministic Calculation:</b> Implement a server-side engine to calculate expenses, balances, and category shares with complete mathematical accuracy.", bullet_style))
    story.append(Paragraph("2. <b>Generative Insights:</b> Use Google Gemini to turn verified figures into clear, practical recommendations.", bullet_style))
    story.append(Paragraph("3. <b>Multi-Scenario Support:</b> Provide dedicated workflows for monthly budgets, home interiors, events, and jewelry styling.", bullet_style))
    story.append(Paragraph("4. <b>Multimodal Vision:</b> Support optional outfit image uploads in the jewelry module to analyze color compatibility.", bullet_style))
    story.append(Paragraph("5. <b>Secure Configuration:</b> Keep API keys in server-side environment variables, isolated from client-facing code.", bullet_style))
    story.append(Paragraph("6. <b>Cloud Deployment:</b> Deploy the application to a public, production-ready environment on Render.", bullet_style))

    story.append(Paragraph("3.2 Scope Boundaries", h2_style))
    scope_data = [
        [Paragraph("<b>Functional Category</b>", body_style), Paragraph("<b>In-Scope (Implemented)</b>", body_style), Paragraph("<b>Out-of-Scope (Excluded)</b>", body_style)],
        [Paragraph("<b>Financial Data</b>", body_style), Paragraph("User-submitted figures with strict validation.", body_style), Paragraph("Direct bank logins or automated account scraping.", body_style)],
        [Paragraph("<b>Transactions</b>", body_style), Paragraph("Budget estimates and merchant search queries.", body_style), Paragraph("Automated checkouts or direct payment processing.", body_style)],
        [Paragraph("<b>Advisory Nature</b>", body_style), Paragraph("Educational guidance and planning heuristics.", body_style), Paragraph("Certified investment, tax, or legal advice.", body_style)],
        [Paragraph("<b>Computer Vision</b>", body_style), Paragraph("Color matching and aesthetic style compatibility.", body_style), Paragraph("Biometric recognition or facial attribute analysis.", body_style)],
    ]
    scope_table = Table(scope_data, colWidths=[110, 204, 190])
    scope_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(scope_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.3 Feasibility Evaluation", h2_style))
    story.append(Paragraph("• <b>Technical Feasibility:</b> Python handles numeric processing with ease, while the Google Gemini API provides reliable, well-documented model access.", bullet_style))
    story.append(Paragraph("• <b>Economic Feasibility:</b> The system runs within standard free-tier hosting limits on Render and uses Google AI Studio developer tiers.", bullet_style))
    story.append(Paragraph("• <b>Operational Feasibility:</b> The web interface works directly in standard browsers without plugins or downloads.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: CHAPTER 4 — REQUIREMENT SPECIFICATIONS & USER PERSONAS
    # ==========================================
    story.append(Paragraph("Chapter 4: Requirement Specifications &amp; User Personas", h1_style))
    story.append(Paragraph("4.1 Functional Requirements (FR)", h2_style))
    story.append(Paragraph("• <b>FR-01 (Input Validation):</b> Rejects non-numeric characters, negative currency values, and empty mandatory fields before processing.", bullet_style))
    story.append(Paragraph("• <b>FR-02 (Deterministic Summation):</b> Calculates total expenditures, net balances, and percentage shares using exact server arithmetic.", bullet_style))
    story.append(Paragraph("• <b>FR-03 (Goal Variance):</b> Computes variance between net balance and target savings goals, returning achievement status flags.", bullet_style))
    story.append(Paragraph("• <b>FR-04 (Prompt Packaging):</b> Formats validated figures into structured prompts and passes them safely to the Google Gemini API.", bullet_style))
    story.append(Paragraph("• <b>FR-05 (Multimodal Pipeline):</b> Validates and encodes optional outfit images (PNG/JPG) for jewelry styling analysis.", bullet_style))
    story.append(Paragraph("• <b>FR-06 (Search Link Synthesis):</b> Generates clean, encoded search links for major merchants (IKEA, Amazon, CaratLane, etc.).", bullet_style))

    story.append(Paragraph("4.2 Non-Functional Requirements (NFR)", h2_style))
    story.append(Paragraph("• <b>NFR-01 (Performance &amp; Latency):</b> Backend calculations complete in under 10ms; full Gemini responses return within 4.5 seconds.", bullet_style))
    story.append(Paragraph("• <b>NFR-02 (Security &amp; Key Isolation):</b> API keys are stored in server-side environment variables and never exposed to the client.", bullet_style))
    story.append(Paragraph("• <b>NFR-03 (Graceful Error Recovery):</b> Returns mathematical totals with fallback messages if the AI service experiences downtime.", bullet_style))
    story.append(Paragraph("• <b>NFR-04 (Cross-Device Usability):</b> The responsive interface renders cleanly on screens from 320px to 2560px wide.", bullet_style))

    story.append(Paragraph("4.3 User Personas &amp; Target Audiences", h2_style))
    personas_data = [
        [Paragraph("<b>User Persona</b>", body_style), Paragraph("<b>Context &amp; Constraints</b>", body_style), Paragraph("<b>Primary Need from PocketSmart AI</b>", body_style)],
        [Paragraph("<b>College Student</b><br/>(Allowance: ₹10,000)", body_style), Paragraph("Limited budget; high spending on food and transit; aims to save ₹2,000.", body_style), Paragraph("Identifies discretionary spending leaks and sets practical savings targets.", body_style)],
        [Paragraph("<b>New Homeowner</b><br/>(Living Room: ₹80,000)", body_style), Paragraph("Uncertain how to balance sofa, lighting, and storage costs.", body_style), Paragraph("Provides itemized room allocations with clear trade-off suggestions.", body_style)],
        [Paragraph("<b>Event Organizer</b><br/>(Celebration: ₹50,000)", body_style), Paragraph("Needs to host 75 guests across food, venue, and photography.", body_style), Paragraph("Calculates per-head catering allocations and reserves a contingency buffer.", body_style)],
    ]
    p_table = Table(personas_data, colWidths=[120, 194, 190])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(p_table)
    story.append(PageBreak())

    # ==========================================
    # PAGE 8: CHAPTER 5 — SYSTEM ARCHITECTURE & DESIGN PRINCIPLES
    # ==========================================
    story.append(Paragraph("Chapter 5: System Architecture &amp; Decoupled Design Principles", h1_style))
    story.append(Paragraph("5.1 Three-Tier Decoupled Architecture", h2_style))
    story.append(Paragraph(
        "PocketSmart AI uses a three-tier architecture to keep data presentation, business logic, and AI services cleanly separated:",
        body_style
    ))
    story.append(Paragraph("• <b>Presentation Tier (Client):</b> Provides clean input forms, handles basic client validation, and displays calculated summaries and AI insights.", bullet_style))
    story.append(Paragraph("• <b>Business Logic Tier (Application Controller):</b> Validates incoming requests, computes all arithmetic, and manages API communication.", bullet_style))
    story.append(Paragraph("• <b>Intelligence Tier (Google Gemini Service):</b> Generates qualitative insights, context-aware suggestions, and multimodal styling recommendations.", bullet_style))
    story.append(Spacer(1, 6))

    arch_box = [
        [Paragraph("<b>CLIENT LAYER (HTML5, Modern CSS, Responsive JavaScript)</b><br/>Captures form inputs • Displays rupee-formatted totals • Renders AI insight cards", body_style)],
        [Paragraph("<b>▼ HTTP POST Request (JSON / Form Data)</b>", ParagraphStyle('Arrow', parent=body_style, alignment=1, textColor=primary_color))],
        [Paragraph("<b>APPLICATION CONTROLLER (Python Server Engine)</b><br/><b>1. Input Validation:</b> Checks bounds, types, and sanitizes strings.<br/><b>2. Deterministic Arithmetic:</b> Computes totals, balances, and percentages.<br/><b>3. Context Builder:</b> Assembles verified figures into structured prompts.", body_style)],
        [Paragraph("<b>▼ Authenticated HTTPS REST Call (Encrypted Payload)</b>", ParagraphStyle('Arrow2', parent=body_style, alignment=1, textColor=secondary_color))],
        [Paragraph("<b>INTELLIGENCE LAYER (Google Gemini API)</b><br/>Processes structured prompt context • Generates qualitative explanations • Returns formatted markdown", body_style)]
    ]
    arch_table = Table(arch_box, colWidths=[504])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor("#F0FDF4")),
        ('BACKGROUND', (0, 4), (0, 4), colors.HexColor("#FAF5FF")),
        ('BOX', (0, 0), (0, -1), 0.5, colors.HexColor("#94A3B8")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Key Architectural Principles", h2_style))
    story.append(Paragraph("1. <b>Code Calculates; AI Explains:</b> The language model never performs arithmetic, eliminating calculation errors.", bullet_style))
    story.append(Paragraph("2. <b>Environment Variable Security:</b> API keys remain on the server and are never included in Git commits or client bundles.", bullet_style))
    story.append(Paragraph("3. <b>Defensive Error Handling:</b> API requests have strict timeouts; errors fall back gracefully to display mathematical summaries.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 9: CHAPTER 6 — BEHAVIORAL MODELING & DATA FLOW DIAGRAMS
    # ==========================================
    story.append(Paragraph("Chapter 6: Behavioral Modeling &amp; Data Flow Diagrams (DFD)", h1_style))
    story.append(Paragraph("6.1 Level-0 Context Diagram", h2_style))
    story.append(Paragraph(
        "At the highest level, PocketSmart AI interacts with two main entities: the end user and the Google Gemini API. The user submits financial parameters or preferences, the system computes verified metrics, and Gemini enriches the response with contextual reasoning.",
        body_style
    ))

    story.append(Paragraph("6.2 Level-1 Detailed Data Flow Architecture", h2_style))
    story.append(Paragraph(
        "The internal data flow moves sequentially through six well-defined stages:",
        body_style
    ))

    dfd_steps = [
        [Paragraph("<b>Step</b>", body_style), Paragraph("<b>Sub-Process Name</b>", body_style), Paragraph("<b>Data Input &amp; Output Transformation</b>", body_style)],
        [Paragraph("<b>1.0</b>", body_style), Paragraph("Input Sanitization", body_style), Paragraph("Cleans input strings, rejects negative values, and validates types.", body_style)],
        [Paragraph("<b>2.0</b>", body_style), Paragraph("Deterministic Engine", body_style), Paragraph("Computes exact expenditures, balances, percentages, and goal variances.", body_style)],
        [Paragraph("<b>3.0</b>", body_style), Paragraph("Context Assembler", body_style), Paragraph("Combines calculated figures into a structured prompt payload.", body_style)],
        [Paragraph("<b>4.0</b>", body_style), Paragraph("Gemini API Client", body_style), Paragraph("Sends authenticated HTTPS request; manages timeouts and retries.", body_style)],
        [Paragraph("<b>5.0</b>", body_style), Paragraph("Response Parser", body_style), Paragraph("Parses markdown text and generates merchant search query links.", body_style)],
        [Paragraph("<b>6.0</b>", body_style), Paragraph("Presentation Renderer", body_style), Paragraph("Builds response displaying verified numbers alongside AI advice.", body_style)],
    ]
    dfd_table = Table(dfd_steps, colWidths=[50, 140, 314])
    dfd_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(dfd_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6.3 State Lifecycle of a Request", h2_style))
    story.append(Paragraph("1. <b>Form Submission:</b> The browser bundles user values and dispatches an HTTP POST request.", bullet_style))
    story.append(Paragraph("2. <b>Server Validation:</b> The backend validates each field, stopping execution immediately if invalid data is detected.", bullet_style))
    story.append(Paragraph("3. <b>Arithmetic Execution:</b> The server evaluates all sums, percentages, and variances deterministically.", bullet_style))
    story.append(Paragraph("4. <b>LLM Enrichment:</b> The server calls Google Gemini to generate natural-language recommendations.", bullet_style))
    story.append(Paragraph("5. <b>UI Presentation:</b> The response returns to the client, displaying numbers and advice in clear sections.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 10: CHAPTER 7 — MATHEMATICAL FOUNDATIONS & ALGORITHMS
    # ==========================================
    story.append(Paragraph("Chapter 7: Mathematical Foundations &amp; Deterministic Algorithms", h1_style))
    story.append(Paragraph("7.1 Mathematical Formulations", h2_style))
    story.append(Paragraph(
        "To ensure complete calculation accuracy, the backend uses strict arithmetic formulas for all calculations:",
        body_style
    ))
    story.append(Paragraph("<b>1. Total Expense Aggregation:</b><br/>Given $n$ validated spending categories $E_i$, total spending is computed as:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>E_total = ∑ (E_i) for i = 1 to n</b> &nbsp;&nbsp;(where each E_i ≥ 0)", body_style))
    story.append(Paragraph("<b>2. Remaining Disposable Balance:</b><br/>Given monthly net income <b>I</b>:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>B_remaining = I - E_total</b>", body_style))
    story.append(Paragraph("<b>3. Category Spending Shares:</b><br/>Each category's proportion of total income is calculated as:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>Share_i = (E_i / I) * 100%</b> &nbsp;&nbsp;(when I &gt; 0)", body_style))
    story.append(Paragraph("<b>4. Savings-to-Goal Variance:</b><br/>Given the user's monthly savings target <b>G</b>:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>Δ_savings = B_remaining - G</b><br/>If Δ_savings ≥ 0, the goal is met with a buffer; if Δ_savings &lt; 0, the plan is in deficit by |Δ_savings|.", body_style))

    story.append(Paragraph("7.2 Python Algorithmic Implementation", h2_style))
    code_snippet = """def calculate_personal_budget(income: float, expenses: dict, savings_goal: float) -> dict:
    if income <= 0:
        raise ValueError("Income must be a positive non-zero value.")
    
    total_expenses = 0.0
    category_shares = {}
    
    for category, amount in expenses.items():
        if amount < 0:
            raise ValueError(f"Expense cannot be negative: {category}")
        total_expenses += amount
        
    remaining_balance = income - total_expenses
    
    for category, amount in expenses.items():
        category_shares[category] = round((amount / income) * 100.0, 2)
        
    savings_delta = remaining_balance - savings_goal
    
    return {
        "income": round(income, 2),
        "total_expenses": round(total_expenses, 2),
        "remaining_balance": round(remaining_balance, 2),
        "category_shares": category_shares,
        "savings_goal": round(savings_goal, 2),
        "savings_delta": round(savings_delta, 2),
        "goal_achieved": savings_delta >= 0
    }"""
    story.append(Paragraph(code_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Paragraph("This function executes in less than 2 milliseconds and is thoroughly unit tested across typical, boundary, and deficit scenarios.", body_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 11: CHAPTER 8 — MODULE SPECIFICATION I: PERSONAL BUDGET ENGINE
    # ==========================================
    story.append(Paragraph("Chapter 8: Module Specification I — Personal Budget Engine", h1_style))
    story.append(Paragraph("8.1 Functional Overview", h2_style))
    story.append(Paragraph(
        "The <b>Personal Budget Engine</b> helps users assess monthly cash flow. It calculates total expenses and category percentages, compares results against a target savings goal, and calls Google Gemini to suggest practical adjustments.",
        body_style
    ))

    story.append(Paragraph("8.2 Rule-Based Health Indicators", h2_style))
    story.append(Paragraph(
        "Before sending data to Gemini, the engine checks the numbers against standard budgeting rules (such as the 50/30/20 framework) to flag clear imbalances:",
        body_style
    ))
    story.append(Paragraph("• <b>High Rent Burden:</b> Flags rent spending when it exceeds 40% of net income.", bullet_style))
    story.append(Paragraph("• <b>Discretionary Spending Alert:</b> Flags discretionary purchases when they exceed 25% of net income.", bullet_style))
    story.append(Paragraph("• <b>Deficit Warning:</b> Immediately alerts the user if total expenses exceed monthly income.", bullet_style))

    story.append(Paragraph("8.3 Prompt Assembly Architecture", h2_style))
    story.append(Paragraph(
        "Verified totals are assembled into a structured prompt that directs Gemini to provide focused, practical feedback without altering the numbers:",
        body_style
    ))

    pb_prompt = """[SYSTEM: PERSONAL FINANCIAL ADVISOR]
You are a supportive, practical financial planning assistant.
Below are verified, server-calculated figures for a user's monthly budget.
Do NOT alter these numbers. Use them as absolute facts.
Do NOT offer formal investment, tax, or legal advice.

[VERIFIED METRICS]
- Monthly Income: ₹{income}
- Total Expenses: ₹{total_expenses}
- Remaining Balance: ₹{remaining_balance}
- Savings Target: ₹{savings_goal}
- Target Status: {goal_achieved} (Variance: ₹{savings_delta})
- Category Breakdown: {category_shares}

[TASK]
1. Provide a 2-sentence summary of the user's current cash flow.
2. If in deficit, recommend 2 specific categories to trim back.
3. If meeting the goal, suggest practical ways to allocate the surplus.
4. Keep the tone encouraging, concise, and easy to read."""
    story.append(Paragraph(pb_prompt.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 12: CHAPTER 9 — MODULE SPECIFICATION II: EVENT & PARTY PLANNER
    # ==========================================
    story.append(Paragraph("Chapter 9: Module Specification II — Event &amp; Celebration Budget Planner", h1_style))
    story.append(Paragraph("9.1 Functional Overview", h2_style))
    story.append(Paragraph(
        "Planning events like birthdays, college fests, or family anniversaries often involves balancing several competing expenses within a fixed budget. The <b>Party &amp; Event Planner</b> takes the total budget, guest count, location, and key preferences to suggest an itemized breakdown with contingency reserves.",
        body_style
    ))

    story.append(Paragraph("9.2 Budget Allocation Heuristics", h2_style))
    story.append(Paragraph(
        "The system uses category weightings based on event planning practices to suggest initial allocations:",
        body_style
    ))

    event_data = [
        [Paragraph("<b>Event Category</b>", body_style), Paragraph("<b>Allocation Share</b>", body_style), Paragraph("<b>Included Items &amp; Services</b>", body_style)],
        [Paragraph("<b>Food &amp; Catering</b>", body_style), Paragraph("35% – 45%", body_style), Paragraph("Buffet/plated meal, appetizers, beverages, desserts, waitstaff.", body_style)],
        [Paragraph("<b>Venue Rental</b>", body_style), Paragraph("20% – 30%", body_style), Paragraph("Hall booking, parking, basic electricity, venue permits.", body_style)],
        [Paragraph("<b>Decor &amp; Stage</b>", body_style), Paragraph("10% – 15%", body_style), Paragraph("Floral decor, backdrop, stage lighting, table styling.", body_style)],
        [Paragraph("<b>Photography &amp; Video</b>", body_style), Paragraph("10% – 12%", body_style), Paragraph("Event photography coverage, digital album deliverables.", body_style)],
        [Paragraph("<b>Sound &amp; DJ</b>", body_style), Paragraph("5% – 8%", body_style), Paragraph("PA system, microphones, music playlist, lighting setup.", body_style)],
        [Paragraph("<b>Contingency Reserve</b>", body_style), Paragraph("5% – 10%", body_style), Paragraph("Unallocated buffer for last-minute guests or extra charges.", body_style)],
    ]
    event_table = Table(event_data, colWidths=[120, 94, 290])
    event_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(event_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("9.3 Per-Head Cost Feasibility", h2_style))
    story.append(Paragraph(
        "The system evaluates per-head costs to ensure the plan remains practical:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Per_Guest_Budget = Total_Budget / Guest_Count</b><br/>"
        "If per-guest food allocation drops below local catering baselines (e.g., &lt;₹150/head for banquets), the system alerts the user and suggests adjusting the guest list or total budget.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 13: CHAPTER 10 — MODULE SPECIFICATION III: HOME INTERIOR PLANNER
    # ==========================================
    story.append(Paragraph("Chapter 10: Module Specification III — Home Interior &amp; Space Planner", h1_style))
    story.append(Paragraph("10.1 Functional Overview", h2_style))
    story.append(Paragraph(
        "Furnishing or renovating a room often leads to unplanned spending when anchor pieces consume too much of the budget. The <b>Home Interior &amp; Space Planner</b> divides a room budget across essential furniture and decorative items based on room type, style preference, and user priorities.",
        body_style
    ))

    story.append(Paragraph("10.2 Spatial Division Framework", h2_style))
    story.append(Paragraph(
        "The system divides expenses into three clear priority tiers to help prevent overspending on secondary items:",
        body_style
    ))

    home_data = [
        [Paragraph("<b>Priority Tier</b>", body_style), Paragraph("<b>Target Share</b>", body_style), Paragraph("<b>Example Items (Living Room Sample)</b>", body_style)],
        [Paragraph("<b>Tier 1: Anchor Pieces</b>", body_style), Paragraph("45% – 50%", body_style), Paragraph("Primary sofa, dining table set, master bed frame.", body_style)],
        [Paragraph("<b>Tier 2: Functional Storage</b>", body_style), Paragraph("20% – 25%", body_style), Paragraph("TV console, coffee table, bookshelves, side credenza.", body_style)],
        [Paragraph("<b>Tier 3: Lighting &amp; Decor</b>", body_style), Paragraph("15% – 20%", body_style), Paragraph("Floor lamps, warm ceiling fixtures, wall mirrors.", body_style)],
        [Paragraph("<b>Tier 4: Soft Furnishings</b>", body_style), Paragraph("10% – 12%", body_style), Paragraph("Area rugs, cushion sets, window curtains, throws.", body_style)],
        [Paragraph("<b>Unallocated Reserve</b>", body_style), Paragraph("5%", body_style), Paragraph("Reserved for delivery, assembly fees, and hardware.", body_style)],
    ]
    home_table = Table(home_data, colWidths=[130, 90, 284])
    home_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(home_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("10.3 Budget Feasibility &amp; Trade-off Suggestions", h2_style))
    story.append(Paragraph(
        "When a user's wishlist exceeds their stated budget, the system highlights realistic trade-offs rather than generating unfeasible plans:<br/>"
        "<i>\"With a ₹35,000 budget, we recommend choosing a durable 3-seater sofa (₹22,000) and pair of side tables (₹5,000), while opting for wall-mounted shelves rather than a large entertainment unit.\"</i>",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 14: CHAPTER 11 — MODULE SPECIFICATION IV: JEWELRY STYLIST
    # ==========================================
    story.append(Paragraph("Chapter 11: Module Specification IV — Jewelry Stylist &amp; Multimodal Engine", h1_style))
    story.append(Paragraph("11.1 Functional Overview", h2_style))
    story.append(Paragraph(
        "The <b>Jewelry Recommendation Module</b> matches accessories to a user's budget, occasion, preferred metal, and style. It also supports an optional image upload feature, allowing Google Gemini's multimodal capabilities to suggest pieces that complement outfit colors and patterns.",
        body_style
    ))

    story.append(Paragraph("11.2 Material &amp; Karatage Feasibility Rules", h2_style))
    story.append(Paragraph(
        "To keep recommendations realistic, the system uses clear budget thresholds for different materials:",
        body_style
    ))
    story.append(Paragraph("• <b>Budget Under ₹5,000:</b> Suggests 925 sterling silver, oxidised silver, brass jewelry, and semi-precious stone accents. Precludes solid gold.", bullet_style))
    story.append(Paragraph("• <b>Budget ₹5,000 – ₹25,000:</b> Recommends lightweight 14K/18K gold accents, certified silver pieces, lab-grown gemstones, and cubic zirconia.", bullet_style))
    story.append(Paragraph("• <b>Budget Over ₹25,000:</b> Suggests 18K/22K yellow and rose gold, certified diamond pendants, and occasion collections.", bullet_style))

    story.append(Paragraph("11.3 Multimodal Vision Pipeline", h2_style))
    story.append(Paragraph(
        "When an outfit photo is provided, the image is processed through three steps:",
        body_style
    ))
    story.append(Paragraph("1. <b>Validation:</b> Checked for PNG/JPEG format and confirmed to be under 4MB.", bullet_style))
    story.append(Paragraph("2. <b>Encoding:</b> Converted to Base64 format and packaged for the Gemini API.", bullet_style))
    story.append(Paragraph("3. <b>Color Analysis Prompt:</b> Asks Gemini to extract the primary garment colors and recommend complementary metals (e.g., rose gold against emerald green).", bullet_style))
    story.append(Paragraph(
        "<b>Privacy Safeguard:</b> The model is instructed to review only garment styling and colors, ignoring facial features, identity, and personal attributes.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 15: CHAPTER 12 — GENERATIVE AI INTEGRATION & PROMPT ENGINEERING
    # ==========================================
    story.append(Paragraph("Chapter 12: Generative AI Integration &amp; Prompt Engineering", h1_style))
    story.append(Paragraph("12.1 Google Gemini API Configuration", h2_style))
    story.append(Paragraph(
        "PocketSmart AI configures Google Gemini models via Google AI Studio with parameters tuned for clear, grounded outputs:",
        body_style
    ))

    gemini_params = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Setting</b>", body_style), Paragraph("<b>Engineering Rationale</b>", body_style)],
        [Paragraph("<b>Target Model</b>", body_style), Paragraph("`gemini-1.5-flash`", body_style), Paragraph("Fast response times and native multimodal support.", body_style)],
        [Paragraph("<b>Temperature</b>", body_style), Paragraph("`0.3` – `0.4`", body_style), Paragraph("Low randomness to prioritize factual consistency.", body_style)],
        [Paragraph("<b>Top-P</b>", body_style), Paragraph("`0.85`", body_style), Paragraph("Restricts tokens to high-probability selections.", body_style)],
        [Paragraph("<b>Top-K</b>", body_style), Paragraph("`40`", body_style), Paragraph("Limits token sampling to maintain topic focus.", body_style)],
        [Paragraph("<b>Max Tokens</b>", body_style), Paragraph("`1200`", body_style), Paragraph("Provides enough headroom for complete, unclipped responses.", body_style)],
    ]
    gp_table = Table(gemini_params, colWidths=[100, 100, 304])
    gp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(gp_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("12.2 Prompt Engineering Strategy", h2_style))
    story.append(Paragraph("• <b>System Persona:</b> Defines the assistant as an objective planning analyst rather than an open-ended conversationalist.", bullet_style))
    story.append(Paragraph("• <b>Fixed Ground Truth:</b> Supplies server-calculated numbers as established facts that must not be modified.", bullet_style))
    story.append(Paragraph("• <b>Structured Headings:</b> Requires output organized under clear markdown sections for consistent UI rendering.", bullet_style))
    story.append(Paragraph("• <b>Clear Limitations:</b> Directs the model to label prices as estimates and avoid claiming live inventory availability.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 16: CHAPTER 13 — DATA STRUCTURES & VALIDATION LAYERS
    # ==========================================
    story.append(Paragraph("Chapter 13: Data Structures, Payloads &amp; Validation Layers", h1_style))
    story.append(Paragraph("13.1 Input Validation Schema", h2_style))
    story.append(Paragraph(
        "Incoming requests are validated against strict JSON schemas to catch formatting errors before calculations execute:",
        body_style
    ))

    schema_sample = """{
  "type": "object",
  "properties": {
    "income": { "type": "number", "minimum": 1.0 },
    "savings_goal": { "type": "number", "minimum": 0.0 },
    "expenses": {
      "type": "object",
      "properties": {
        "rent": { "type": "number", "minimum": 0.0 },
        "food": { "type": "number", "minimum": 0.0 },
        "transport": { "type": "number", "minimum": 0.0 },
        "shopping": { "type": "number", "minimum": 0.0 }
      },
      "required": ["rent", "food", "transport"]
    }
  },
  "required": ["income", "savings_goal", "expenses"]
}"""
    story.append(Paragraph(schema_sample.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("13.2 Server Response Structure", h2_style))
    story.append(Paragraph(
        "The server returns a structured response that clearly separates mathematical totals from AI commentary:",
        body_style
    ))

    response_sample = """{
  "status": "success",
  "data": {
    "deterministic_summary": {
      "income": 30000.0,
      "total_expenses": 22700.0,
      "remaining_balance": 7300.0,
      "goal_met": true,
      "savings_delta": 2300.0
    },
    "ai_generated_insights": {
      "analysis": "Healthy surplus observed. Savings goal met with ₹2,300 buffer.",
      "disclaimer": "AI recommendations are estimates and not formal financial advice."
    }
  }
}"""
    story.append(Paragraph(response_sample.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 17: CHAPTER 14 — USER INTERFACE & INTERACTION DESIGN
    # ==========================================
    story.append(Paragraph("Chapter 14: User Interface &amp; Human-Computer Interaction Design", h1_style))
    story.append(Paragraph("14.1 Design Philosophy", h2_style))
    story.append(Paragraph(
        "The user interface follows four core design principles to keep interactions straightforward and transparent:",
        body_style
    ))
    story.append(Paragraph("• <b>Numbers First:</b> Shows verified arithmetic totals at the top of the results card, ensuring key figures are seen before reading advice.", bullet_style))
    story.append(Paragraph("• <b>Visual Distinction:</b> Displays AI-generated text inside cards marked with an \"AI Estimate\" badge.", bullet_style))
    story.append(Paragraph("• <b>Input Guidance:</b> Includes rupee (`₹`) prefixes and clear inline validation messages to catch data-entry mistakes early.", bullet_style))
    story.append(Paragraph("• <b>Responsive Feedback:</b> Displays animated loading indicators during API requests, with error banners if calls fail.", bullet_style))

    story.append(Paragraph("14.2 External Search Link Generator", h2_style))
    story.append(Paragraph(
        "Rather than claiming live store inventory, the application generates search queries that open directly on merchant sites:",
        body_style
    ))

    link_code = """import urllib.parse

def generate_search_link(platform: str, query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    search_engines = {
        "amazon": "https://www.amazon.in/s?k=",
        "ikea": "https://www.ikea.com/in/en/search/?q=",
        "caratlane": "https://www.caratlane.com/search?q=",
        "myntra": "https://www.myntra.com/"
    }
    return search_engines.get(platform.lower(), "https://www.google.com/search?q=") + encoded"""
    story.append(Paragraph(link_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 18: CHAPTER 15 — APPLICATION WALKTHROUGHS & CASE STUDIES
    # ==========================================
    story.append(Paragraph("Chapter 15: Application Walkthroughs &amp; Real-World Scenarios", h1_style))
    story.append(Paragraph("15.1 Case Study 1: Personal Monthly Budget", h2_style))
    story.append(Paragraph(
        "<b>User Input:</b> Income: ₹30,000 | Rent: ₹9,000 | Food: ₹6,000 | Transport: ₹2,500 | Subscriptions: ₹1,200 | Shopping: ₹4,000 | Savings Target: ₹5,000.<br/>"
        "<b>Calculated Summary:</b> Total Spend: <b>₹22,700</b> | Balance: <b>₹7,300</b> | Rent Share: <b>30%</b> | Food Share: <b>20%</b>.<br/>"
        "<b>Savings Status:</b> <b>Goal Achieved</b> with a <b>₹2,300</b> safety buffer.<br/>"
        "<b>Gemini Analysis:</b> <i>\"Your monthly cash flow is well balanced. Fixed costs stay within 50% of income, comfortably meeting your ₹5,000 target. Consider routing the extra ₹2,300 surplus toward an emergency buffer.\"</i>",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("15.2 Case Study 2: Living Room Interior Plan", h2_style))
    story.append(Paragraph(
        "<b>User Input:</b> Room: 14x12 Living Room | Style: Modern Minimalist | Total Budget: ₹60,000 | Priority: Seating &amp; Lighting.<br/>"
        "<b>Suggested Breakdown:</b><br/>"
        "• 3-Seater Fabric Sofa: ₹28,000 (Anchor Piece)<br/>"
        "• Coffee Table &amp; Side Stool: ₹9,500<br/>"
        "• Ambient Floor Lamp &amp; LED Warm Fixtures: ₹6,000<br/>"
        "• Rug &amp; Neutral Curtains: ₹7,500<br/>"
        "• Reserve Buffer: ₹9,000 (Reserved for delivery and installation)<br/>"
        "<b>Generated Links:</b> External search queries for <i>\"minimalist 3-seater fabric sofa\"</i> on IKEA and Amazon.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("15.3 Case Study 3: College Symposium Celebration", h2_style))
    story.append(Paragraph(
        "<b>User Input:</b> Event: College Department Seminar | Guests: 100 students | Total Budget: ₹40,000.<br/>"
        "<b>Calculated Metrics:</b> Per-guest allocation = <b>₹400 / attendee</b>.<br/>"
        "<b>Itemized Allocation:</b> Boxed high-tea snacks: ₹18,000 (₹180/head) | Audio-visual rental: ₹8,000 | Mementos &amp; Certificates: ₹7,000 | Stage decor: ₹4,000 | Contingency buffer: ₹3,000.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 19: CHAPTER 16 — VERIFICATION, TESTING & SECURITY AUDIT
    # ==========================================
    story.append(Paragraph("Chapter 16: Verification, Automated Test Suite &amp; Security Audits", h1_style))
    story.append(Paragraph("16.1 Automated &amp; Manual Test Matrix", h2_style))
    story.append(Paragraph(
        "The system was evaluated through unit, integration, and security test cases to verify calculation accuracy and safe failure handling:",
        body_style
    ))

    test_data = [
        [Paragraph("<b>Test ID</b>", body_style), Paragraph("<b>Test Scope</b>", body_style), Paragraph("<b>Input Condition</b>", body_style), Paragraph("<b>Observed Result</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("<b>TC-01</b>", body_style), Paragraph("Baseline Budget", body_style), Paragraph("Standard valid figures", body_style), Paragraph("Exact totals; Gemini advisory returned", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-02</b>", body_style), Paragraph("Deficit Scenario", body_style), Paragraph("Expenses exceed income", body_style), Paragraph("Negative balance flagged; cutbacks suggested", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-03</b>", body_style), Paragraph("Negative Values", body_style), Paragraph("Negative expense float", body_style), Paragraph("Validation error (HTTP 422); halts execution", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-04</b>", body_style), Paragraph("Missing Fields", body_style), Paragraph("Empty required inputs", body_style), Paragraph("Submission blocked with inline message", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-05</b>", body_style), Paragraph("Currency Symbols", body_style), Paragraph("Inputs with ₹, $, commas", body_style), Paragraph("Cleaned safely without formatting errors", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-06</b>", body_style), Paragraph("API Key Failure", body_style), Paragraph("Invalid or missing API key", body_style), Paragraph("Totals displayed; fallback message shown", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-07</b>", body_style), Paragraph("Oversized Image", body_style), Paragraph("10MB PNG image", body_style), Paragraph("Rejected with file-size warning", body_style), Paragraph("<b>PASS</b>", body_style)],
        [Paragraph("<b>TC-08</b>", body_style), Paragraph("Outfit Image", body_style), Paragraph("Valid 1.5MB outfit image", body_style), Paragraph("Base64 encoded; styling advice returned", body_style), Paragraph("<b>PASS</b>", body_style)],
    ]
    test_table = Table(test_data, colWidths=[45, 95, 120, 194, 50])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("16.2 Security &amp; Data Privacy Verification", h2_style))
    story.append(Paragraph("• <b>API Key Protection:</b> Confirmed that `GEMINI_API_KEY` is loaded strictly on the server and is never exposed in client bundles.", bullet_style))
    story.append(Paragraph("• <b>XSS Prevention:</b> Model responses are sanitized before rendering to prevent script injection vulnerabilities.", bullet_style))
    story.append(Paragraph("• <b>Stateless Processing:</b> Financial inputs are handled in-memory and are not stored to disk without explicit opt-in.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 20: CHAPTER 17 — CLOUD DEPLOYMENT & DEVOPS
    # ==========================================
    story.append(Paragraph("Chapter 17: Cloud Deployment, Containerization &amp; DevOps on Render", h1_style))
    story.append(Paragraph("17.1 Cloud Hosting Architecture", h2_style))
    story.append(Paragraph(
        "PocketSmart AI is deployed as a cloud web service on Render, connected directly to the project's GitHub repository for automated deployment:",
        body_style
    ))
    story.append(Paragraph("1. <b>Code Push:</b> Team pushes commits to the repository main branch.", bullet_style))
    story.append(Paragraph("2. <b>Build Trigger:</b> Render automatically detects changes and initializes a Python 3.11 build container.", bullet_style))
    story.append(Paragraph("3. <b>Dependency Installation:</b> Installs packages from `requirements.txt` (`google-generativeai`, `python-dotenv`, web framework).", bullet_style))
    story.append(Paragraph("4. <b>Environment Injection:</b> Injects `GEMINI_API_KEY` and configuration variables securely from Render's dashboard.", bullet_style))
    story.append(Paragraph("5. <b>Live Deployment:</b> Starts the production web server, serving traffic at the live endpoint.", bullet_style))

    story.append(Paragraph("17.2 Verified Project Endpoints", h2_style))
    link_info = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>Verified URL Endpoint</b>", body_style)],
        [Paragraph("<b>Live Application</b>", body_style), Paragraph("https://pocketsmart-ai-ba9w.onrender.com", body_style)],
        [Paragraph("<b>GitHub Repository</b>", body_style), Paragraph("https://github.com/swe1142007-bot/PocketSmart-AI", body_style)],
        [Paragraph("<b>AI Studio Portal</b>", body_style), Paragraph("https://aistudio.google.com/apikey", body_style)],
    ]
    link_table = Table(link_info, colWidths=[140, 364])
    link_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
    ]))
    story.append(link_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("17.3 Local Environment Reproduction Steps", h2_style))
    story.append(Paragraph(
        "To set up and run the application locally:<br/>"
        "1. Clone the repository: <code>git clone https://github.com/swe1142007-bot/PocketSmart-AI.git</code><br/>"
        "2. Create a virtual environment: <code>python -m venv .venv</code> and activate it.<br/>"
        "3. Install dependencies: <code>pip install -r requirements.txt</code><br/>"
        "4. Set up environment variables in a local <code>.env</code> file with your Gemini API key.<br/>"
        "5. Launch the application with <code>python app.py</code> and open the local browser URL.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 21: CHAPTER 18 — CHALLENGES, LIMITATIONS & FUTURE SCOPE
    # ==========================================
    story.append(Paragraph("Chapter 18: Technical Challenges, Risk Mitigation &amp; Future Scope", h1_style))
    story.append(Paragraph("18.1 Technical Challenges Overcome", h2_style))
    story.append(Paragraph("• <b>Arithmetic Drift in LLMs:</b> Resolved by running all mathematical calculations through a dedicated Python core before querying Gemini.", bullet_style))
    story.append(Paragraph("• <b>API Rate Limits &amp; Latency:</b> Handled with request timeouts and structured fallbacks, ensuring basic budget totals display even if API calls slow down.", bullet_style))
    story.append(Paragraph("• <b>Pricing Transparency:</b> Prevented inaccurate price claims by labeling all AI figures as estimates and generating search queries instead.", bullet_style))

    story.append(Paragraph("18.2 System Limitations &amp; Ethical Boundaries", h2_style))
    story.append(Paragraph("• <b>Educational Use Only:</b> PocketSmart AI is designed as a planning aid and does not provide formal financial, tax, or investment advice.", bullet_style))
    story.append(Paragraph("• <b>Privacy Notice:</b> Users should avoid entering confidential details like account numbers or passwords into text fields.", bullet_style))
    story.append(Paragraph("• <b>Visual Analysis Limits:</b> Image uploads are evaluated solely for colors and materials, ignoring personal or facial features.", bullet_style))

    story.append(Paragraph("18.3 Future Enhancement Roadmap", h2_style))
    story.append(Paragraph("1. <b>Statement File Import:</b> Allow users to upload CSV or PDF bank statements for automatic expense categorization.", bullet_style))
    story.append(Paragraph("2. <b>Spending Trends &amp; History:</b> Add lightweight database storage to track monthly spending patterns over time.", bullet_style))
    story.append(Paragraph("3. <b>Multilingual Support:</b> Support regional Indian languages including Tamil, Hindi, and Telugu.", bullet_style))
    story.append(Paragraph("4. <b>Verified Store APIs:</b> Partner with merchant APIs to display real-time pricing and stock status where available.", bullet_style))
    story.append(Paragraph("5. <b>Interactive Follow-up Chat:</b> Enable conversational follow-up questions to refine generated recommendations.", bullet_style))
    story.append(Paragraph("6. <b>Budget Alerts:</b> Send notifications when spending in a given category nears its planned limit.", bullet_style))
    story.append(Paragraph("7. <b>Exportable PDF Reports:</b> Allow users to download clean, printable summary reports for event or renovation plans.", bullet_style))
    story.append(Paragraph("8. <b>Automated Evaluation Tests:</b> Build automated evaluation scripts to assess recommendation quality across model updates.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 22: CHAPTER 19 — CONCLUSION, REFERENCES & APPENDICES
    # ==========================================
    story.append(Paragraph("Chapter 19: Conclusion, Compliance References &amp; Appendices", h1_style))
    story.append(Paragraph("19.1 Concluding Summary", h2_style))
    story.append(Paragraph(
        "<b>PocketSmart AI</b> demonstrates how combining deterministic programming with generative AI creates more reliable software. By pairing Python's exact arithmetic engine with Google Gemini's natural-language reasoning, the platform delivers actionable, grounded budget planning across personal finance, home makeovers, events, and jewelry styling.",
        body_style
    ))

    story.append(Paragraph("19.2 References &amp; Documentation", h2_style))
    story.append(Paragraph("1. <b>Google Gemini API Documentation:</b> https://ai.google.dev/gemini-api/docs", body_style))
    story.append(Paragraph("2. <b>Google AI Studio API Keys:</b> https://aistudio.google.com/apikey", body_style))
    story.append(Paragraph("3. <b>Python 3 Documentation:</b> https://docs.python.org/3/", body_style))
    story.append(Paragraph("4. <b>python-dotenv Library:</b> https://pypi.org/project/python-dotenv/", body_style))
    story.append(Paragraph("5. <b>PocketSmart AI Source Code:</b> https://github.com/swe1142007-bot/PocketSmart-AI", body_style))
    story.append(Paragraph("6. <b>PocketSmart AI Live Demo:</b> https://pocketsmart-ai-ba9w.onrender.com", body_style))

    story.append(Paragraph("Appendix A: Glossary of Terms", h2_style))
    story.append(Paragraph("• <b>Deterministic Math:</b> Code that consistently produces exact, reproducible mathematical results.", bullet_style))
    story.append(Paragraph("• <b>Google Gemini:</b> Google's family of multimodal generative AI models accessed through developer APIs.", bullet_style))
    story.append(Paragraph("• <b>Separation of Concerns:</b> An architectural design that separates calculations from text generation.", bullet_style))

    story.append(Paragraph("Appendix B: Viva Voce &amp; Frequently Asked Questions", h2_style))
    story.append(Paragraph("<b>Q: Why use Python for calculations instead of asking Gemini directly?</b><br/>"
                           "<b>A:</b> Backend code calculates numbers deterministically with zero math errors, freeing the model to focus on qualitative explanations.", body_style))
    story.append(Paragraph("<b>Q: How are API keys protected?</b><br/>"
                           "<b>A:</b> Keys are stored in server-side environment variables and are never included in Git commits or client bundles.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {PDF_FILENAME}")

if __name__ == "__main__":
    build_pdf()
