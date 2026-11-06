# Documentation Notes — PocketSmartAI Project Report

## 1. Overview & Inspection Summary
This document records the inspection, analysis, design decisions, and verification steps performed to produce the formal academic project documentation for **PocketSmartAI**.

- **Source Code Inspected**: `C:\Users\DELL\Desktop\PocketSmartAI` (and corresponding archive `PocketSmartAI.zip`).
- **Reference Style Document Inspected**: `C:\Users\DELL\Documents\LegalEase_Project_Presentation_Document.docx` (utilized strictly for academic formatting, heading hierarchy, table conventions, and presentation aesthetics without borrowing any project specifics).
- **Target Audience**: College project submission, project viva-voce examination committee, and technical peer review.

---

## 2. Inspected Source Files & Architectural Components

| Source File | Module / Layer | Primary Architectural Responsibilities |
|---|---|---|
| `app/main.py` | Presentation & Routing | FastAPI application instantiation, Jinja2 template rendering, static asset mounting, authentication cookies (`access_token`), and exception handling. |
| `app/routes.py` | API & Business Endpoints | Route handlers for user authentication (`/login`, `/signup`, `/logout`), lifestyle optimization workflows (`/recommend`, `/optimize`), history tracking (`/history`), and profile configuration. |
| `app/gemini_service.py` | Generative AI & Multimodal Engine | Google GenAI SDK integration (`gemini-2.5-flash`), dynamic prompt construction, multimodal vision analysis (`PIL.Image`), and deterministic fallback recommendation generator. |
| `app/models.py` | Database Persistence (ORM) | SQLAlchemy ORM model declarations (`User`, `RecommendationHistory`, `ExpenseEntry`, `BudgetPreference`). |
| `app/database.py` | Database Engine & Session | SQLite connection engine (`sqlite:///./pocketsmart.db`), scoped sessionmaker, and declarative Base. |
| `app/auth.py` | Cryptography & Security | Argon2id password hashing via Passlib, HMAC-SHA256 JWT encoding/decoding, token expiration enforcement. |
| `templates/*.html` | Frontend Presentation | Responsive HTML5 UI templates (`index.html`, `login.html`, `signup.html`, `history.html`, `dashboard.html`). |
| `static/css/`, `static/js/` | Client Styling & Scripts | CSS styling, asynchronous fetch calls, DOM updates, and client-side form validation. |
| `requirements.txt` | Environment & Dependencies | Pinned package requirements including `fastapi`, `uvicorn`, `google-genai`, `sqlalchemy`, `passlib[argon2]`, `python-jose`, and `jinja2`. |

---

## 3. Mandatory Formatting Settings Applied

- **Paper Size**: A4 (8.27" × 11.69" / 210 mm × 297 mm)
- **Margins**: Exactly 1.0 inch (72 pt) on all four sides (Top, Bottom, Left, Right)
- **Body Font**: Times New Roman, 12 pt, 1.5 line spacing, Justified alignment
- **Heading Hierarchy**:
  - Chapter Headings: Times New Roman, 14 pt, Bold, Centered / Primary Accent
  - Section Headings (Heading 1): Times New Roman, 13 pt, Bold
  - Subsection Headings (Heading 2): Times New Roman, 11.5 pt, Bold / Semi-bold
- **Code Snippets**: Monospace Consolas, 8.5–10 pt, single-spaced in dedicated visual containers
- **Page Numbers**: 
  - Preliminary pages (Certificate, Declaration, Abstract, TOC, List of Figures/Tables): Lowercase Roman numerals (`i`, `ii`, `iii`, `iv`, `v`) centered in footer.
  - Main report chapters (Chapter 1 through Appendices): Arabic numerals (`1`, `2`, `3`, ..., `17`) centered in footer.
- **Header**: Restrained academic running head: *"PocketSmartAI: Multimodal Budget Decision Support System"*.

---

## 4. Verification & Rendering Validation

- **DOCX File**: `C:\Users\DELL\Desktop\PocketSmartAI\PocketSmartAI_Project_Report.docx`
- **PDF File**: `C:\Users\DELL\Desktop\PocketSmartAI\PocketSmartAI_Project_Report.pdf`
- **Verified Page Count**: Exactly **22 pages** (fully compliant with the 20–25 page requirement, precisely within the ideal 22–23 page target).
- **Embedded Visuals**: 9 high-resolution architectural diagrams, data-flow diagrams, and UI screenshots.
- **Structured Tables**: 10 comprehensive academic tables (Requirements FRS/NFR, Tech Stack, Module Responsibilities, Test Cases, Latency Benchmarks, File Catalog).
- **Footers & Pagination Validation**: Verified via `pypdf` extraction and Microsoft Word COM rendering to ensure clean, singular page numbers on every sheet.

---

## 5. Assumptions, Limitations & Unresolved Items

1. **Student & Institutional Metadata**:
   - Institutional markers, candidate names, roll numbers, department heads, and college addresses are populated with standard academic placeholders (e.g., `[CANDIDATE NAME(S)]`, `[REGISTER NUMBER]`, `[COLLEGE / INSTITUTION NAME]`) to allow seamless final personalization by the student prior to submission.
2. **Third-Party AI API Constraints**:
   - The multimodal generative features require a valid `GEMINI_API_KEY`. In offline or unauthenticated development environments, the application’s built-in **Deterministic Fallback Engine** (`gemini_service.py`) transparently activates, providing reliable algorithmic allocation.
3. **Application Source Code**:
   - All underlying production code in `app/`, `templates/`, `static/`, and `pocketsmart.db` remains 100% untouched and preserved.
