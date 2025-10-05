# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI_NEWS is a CrewAI-based multi-agent system that generates AI/cancer research newsletters. Four agents collaborate sequentially to fetch news, summarize content, draft HTML, and finalize a newsletter. The output is viewable via a Streamlit web interface.

## Development Commands

### Setup
```bash
# Install uv (if not already installed)
pip install uv

# Install dependencies
uv sync

# Set required API key
export SERPER_API_KEY="your_key_here"
```

### Running the Project
```bash
# Run the CrewAI pipeline (generates newsletter in results/)
uv run python -m assignment.main

# Launch Streamlit UI (preview and download newsletter)
uv run streamlit run streamlit_app.py

# Alternative using crewai CLI
crewai run
```

## Architecture

### Agent-Task Pipeline
Sequential process with strict data contracts:

1. **research_assistant** → `fetch_ai_news` task
   - Uses SerperDevTool for web search
   - Outputs: `results/news.md` (FetchResult JSON)
   - Must find ≥5 items per topic

2. **editor_assistant** → `summarize_ai_news` task
   - Input: FetchResult from previous task
   - Outputs: `results/summaries.md` (SummariesOutput JSON)
   - Must include ≥5 links per topic

3. **chief_editor** → `draft_html_newsletter` task
   - Outputs: `results/draft.html`

4. **judge_editor** → `finalize_html_newsletter` task
   - Outputs: `results/newsletter.html`

### Data Contracts (Pydantic)

Defined in `src/assignment/schemas.py`:

- **TopicName**: Literal type constraining topics to 5 canonical values:
  - "Research & Prevention"
  - "Early Detection and Diagnosis"
  - "Drug Discovery and Development"
  - "Treatment Methods"
  - "Precision Oncology"

- **NewsItem**: title, url, publish_date (optional), snippet (optional)
- **FetchResult**: List of TopicItems, each containing topic name and list of NewsItems
- **SummariesOutput**: overview string + list of TopicSummary
- **TopicSummary**: topic name, summary text, bullets list

### Configuration Files

- `src/assignment/config/agents.yaml` - Agent definitions (role, goal, backstory)
- `src/assignment/config/tasks.yaml` - Task definitions (description, expected output)
- `knowledge/user_preference.txt` - User preferences loaded by agents

### Streamlit UI Flow

`streamlit_app.py` provides:
- **Sidebar**: Run crew button, subtopic radio selector (canonical order)
- **Main area**:
  - Main Summary (prefers HTML overview from newsletter.html)
  - Selected topic summary with links
  - Final newsletter preview with themed CSS
  - Download button for newsletter.html

UI extracts sections from final HTML using h2 headings and applies custom theming.

## Key Implementation Details

- All tasks use `output_pydantic` for structured outputs (FetchResult, SummariesOutput)
- Task context is wired via `context=[self.fetch_ai_news()]` in crew.py
- Agents are created with `@agent` decorator, tasks with `@task` decorator
- Process type: `Process.sequential` (defined in crew.py)
- URL fields must be `str` type (not HttpUrl) to avoid JSON serialization errors
- Optional fields use `Optional[str]` syntax (not PEP 604 unions) for Pydantic compatibility

## Common Issues

- **JSON serialization error**: Ensure schemas.py uses `str` for URLs, not HttpUrl
- **Pydantic union errors**: Use `Optional[str]` instead of `str | None`
- **Short overview in app**: Newsletter HTML must include h2 heading like "Overview" or "Executive Summary"
- **Missing topic links**: Verify tasks.yaml requires ≥5 items per topic and ≥5 links in summaries
