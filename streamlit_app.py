import os
import re
import json
from pathlib import Path
import streamlit as st

from assignment.main import run as run_crew


RESULTS_DIR = Path(__file__).parent / "results"
# Structured outputs (JSON text saved in .md files)
NEWS_JSON = RESULTS_DIR / "news.md"
SUMMARIES_JSON = RESULTS_DIR / "summaries.md"
# HTML artifacts
DRAFT_HTML = RESULTS_DIR / "draft.html"
FINAL_HTML = RESULTS_DIR / "newsletter.html"

# Canonical topic order for controlled sidebar
CANONICAL_TOPICS = [
    "Research & Prevention",
    "Early Detection and Diagnosis",
    "Drug Discovery and Development",
    "Treatment Methods",
    "Precision Oncology",
]


def read_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def read_html_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def read_json_file(path: Path):
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8").strip()
        # Some models might wrap JSON in triple backticks; strip them
        if text.startswith("```"):
            text = text.strip("`\n ")
        return json.loads(text)
    except Exception:
        return None


def apply_theme(html: str) -> str:
    """Inject a colorful CSS theme into the newsletter HTML."""
    theme_css = (
        """
        <style>
        :root {
          --primary: #16a34a; /* green */
          --accent: #06b6d4;  /* cyan */
          --bg: #f8fafc;      /* slate-50 */
          --text: #111827;    /* gray-900 */
          --muted: #6b7280;   /* gray-500 */
          --card: #ffffff;
        }
        html, body { background: var(--bg); color: var(--text); }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Arial, sans-serif; line-height: 1.65; }
        .newsletter, main, article, section, .container {
          max-width: 900px; margin: 24px auto; background: var(--card);
          border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px;
          box-shadow: 0 10px 30px rgba(2, 6, 23, 0.08);
        }
        h1 { margin: 0 0 16px 0; color: #fff; padding: 14px 18px; border-radius: 12px;
             background: linear-gradient(90deg, var(--primary), var(--accent));
             box-shadow: 0 6px 16px rgba(22,163,74,0.25); }
        /* Improve contrast for headings in summary view */
        h2 { color: #0f172a; border-left: 6px solid var(--primary); padding-left: 12px; }
        h3 { color: #0f172a; }
        p { color: var(--text); }
        small, .muted { color: var(--muted); }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
        blockquote { background: #f0fdf4; border-left: 5px solid var(--primary); padding: 10px 14px; border-radius: 10px; }
        ul { padding-left: 22px; }
        li { margin: 6px 0; }
        hr { border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }
        table { width: 100%; border-collapse: collapse; border: 1px solid #e5e7eb; }
        th { background: #ecfeff; }
        th, td { border: 1px solid #e5e7eb; padding: 8px 10px; text-align: left; }
        code { background: #f1f5f9; padding: 2px 6px; border-radius: 6px; }
        </style>
        """
    )

    if "<head" in html.lower():
        # Insert right after <head>
        lower = html.lower()
        idx = lower.find("<head")
        close_idx = lower.find(">", idx)
        if close_idx != -1:
            return html[: close_idx + 1] + theme_css + html[close_idx + 1 :]
    # If no <head>, prepend theme
    return theme_css + html


def style_summary_html(html: str) -> str:
    """Wrap provided HTML with inline styles to increase font sizes and readability.
    This affects only the embedded component, not the whole app.
    """
    summary_css = (
        """
        <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Arial, sans-serif; }
        h1 { font-size: 32px; }
        h2 { font-size: 28px; color: #0f172a; }
        h3 { font-size: 24px; color: #0f172a; }
        p, li { font-size: 20px; line-height: 1.75; }
        ul { padding-left: 22px; }
        </style>
        """
    )
    return summary_css + (html or "")


st.set_page_config(page_title="AI Agent News", layout="wide")
st.title("AI Agent News - Crew Runner")

# Subtle colorful theming
st.markdown(
    """
    <style>
      .app-banner {
        background: linear-gradient(90deg, #22c55e 0%, #06b6d4 100%);
        padding: 10px 16px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin-bottom: 12px;
      }
      .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        padding: 10px;
      }
    </style>
    <div class="app-banner">Final AI Newsletter</div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Controls")
    run_clicked = st.button("Run Crew")
    st.markdown("---")
    st.caption("This will execute the CrewAI pipeline and refresh outputs.")

if run_clicked:
    try:
        run_crew()
        st.success("Crew run completed.")
    except Exception as e:
        st.error(f"Crew run failed: {e}")

col = st.container()

with col:
    # Try to render structured summaries first
    summaries_json = read_json_file(SUMMARIES_JSON)
    fetch_json = read_json_file(NEWS_JSON)

    # Load final HTML and parse sections for richer summaries
    final_html_raw = read_html_file(FINAL_HTML)

    def extract_sections(html: str):
        sections = []  # list of (title, inner_html)
        for match in re.finditer(r"<h2[^>]*>(.*?)</h2>([\s\S]*?)(?=<h2[^>]*>|$)", html or "", re.IGNORECASE):
            title = re.sub(r"<.*?>", "", match.group(1)).strip()
            body = match.group(2).strip()
            sections.append((title or "Section", body))
        return sections

    html_sections = extract_sections(final_html_raw)
    section_titles = [t for t, _ in html_sections]

    # Robustly detect overview: match headings containing 'overview' or 'summary'.
    def is_overview_title(title: str) -> bool:
        norm = re.sub(r"[^a-z]", "", (title or "").lower())
        return norm in ("overview", "summary", "executivesummary") or "overview" in norm

    overview_pair = next(((t, b) for (t, b) in html_sections if is_overview_title(t)), None)
    if overview_pair is None and html_sections:
        overview_pair = html_sections[0]

    overview_title = overview_pair[0] if overview_pair else None
    overview_html = overview_pair[1] if overview_pair else None

    # Build topic list and mapping
    overview_text = (summaries_json.get("overview") if isinstance(summaries_json, dict) else None) or ""
    topics = (summaries_json.get("topics") if isinstance(summaries_json, dict) else None) or []
    json_topic_titles = [t.get("topic") for t in topics if isinstance(t, dict) and t.get("topic")] if topics else []
    # Prefer HTML section titles (excluding Overview) for sidebar
    # Build a controlled list of topics following the canonical order
    excluded_title = (overview_title or "").lower()
    available = set([t for t in section_titles if t and t.lower() != excluded_title]) | set(json_topic_titles)
    topic_titles = [t for t in CANONICAL_TOPICS if t in available]

    # Sidebar subtopic controls (same panel as Controls)
    with st.sidebar:
        st.subheader("Subtopics")
        if topic_titles:
            st.radio("Select a topic", topic_titles, key="selected_topic", label_visibility="collapsed")
        else:
            st.info("Run the crew to populate subtopics.")

    # Show main summary at the top (prefer richer HTML Overview)
    st.subheader("Main Summary")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if overview_html:
        st.components.v1.html(style_summary_html(overview_html), height=620, scrolling=True)
    elif overview_text:
        st.write(overview_text)
    else:
        st.info("Run the crew to populate the overview summary.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Selected topic summary (pull selection from sidebar)
    selected = st.session_state.get("selected_topic")
    if not selected and topic_titles:
        st.session_state["selected_topic"] = topic_titles[0]
        selected = topic_titles[0]

    if selected:
        # Selected topic summary on top
        t = next((x for x in topics if x.get("topic") == selected), None)
        if t:
            summary_text = t.get("summary") or ""
            bullets = t.get("bullets") or []
            st.subheader(f"Summary: {selected}")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # Prefer HTML section content for the selected topic
            html_body = next((body for (title, body) in html_sections if title == selected), None)
            if html_body:
                st.components.v1.html(style_summary_html(html_body), height=700, scrolling=True)
            elif summary_text:
                st.markdown(f"<div style='font-size:20px; line-height:1.75'>{summary_text}</div>", unsafe_allow_html=True)
            if bullets:
                st.markdown("\n".join([f"- {b}" for b in bullets]))
            st.markdown('</div>', unsafe_allow_html=True)

            # Links for this topic at the bottom of the summary
            topic_to_items = {}
            if fetch_json and isinstance(fetch_json, dict):
                for ft in fetch_json.get("topics", []):
                    name = ft.get("topic")
                    if name:
                        topic_to_items[name] = ft.get("items", [])
            items = topic_to_items.get(selected, [])
            if items:
                st.markdown("**Further reading**")
                for it in items:
                    title = it.get("title") or it.get("url")
                    url = it.get("url")
                    if url:
                        st.markdown(f"- [{title}]({url})")

    # Always show final themed newsletter preview and download
    st.subheader("Final Newsletter (preview)")
    final_html = read_html_file(FINAL_HTML)
    if not final_html:
        st.info("No final newsletter yet. Click 'Run Crew' to generate.")
    else:
        themed_html = apply_theme(final_html)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.components.v1.html(themed_html, height=650, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            label="Download newsletter.html",
            data=themed_html,
            file_name="newsletter.html",
            mime="text/html",
        )


