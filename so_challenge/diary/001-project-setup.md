---

# 📝 7. Diary Entry

## `diary/001-project-setup.md`

```markdown
# 001 — Project Setup

**Date**: 2026-03-30  
**Tool**: ChatGPT  
**Model**: GPT-5.3  
**Iterations**: 1

## Prompt

**2026-03-30 00:00**

Create a Python project called so-challenge using uv (from Astral)
for dependency management. The project should separate data
collection (data_fetcher.py) from visualization (plotter.py), with
a separate module for milestone definitions (milestones.py).

Set up pytest for testing with corresponding test files for each
module. Manage all dependencies through pyproject.toml — I'll need
pandas, matplotlib, requests, and pytest.

Include a README.md with a brief project description.

Create a diary/ folder for tracking AI interactions. For every
prompt cycle in this project, save the interaction record to this
folder as a numbered markdown file.

## ✅ Cause

This error usually happens because:

- You are **not inside the project directory (`so-challenge`)**
- OR the `pyproject.toml` file is missing

---

## 🔧 Fix (Step-by-Step)

cd move to particular directory

```

# 002 — Requirements Specification

**Date**: 2026-03-30
**Tool**: ChatGPT
**Model**: GPT-5.3
**Iterations**: 1

## Prompt

**2026-03-30 00:00**

Write a brief requirements specification for this project and save
it to docs/requirements.md.

Include:
- Functional requirements (data source, date range 2008-2024, plot
  type, milestone overlay)
- Non-functional requirements (performance: cache data locally,
  reliability: handle API errors with retries, usability: clear axis
  labels and legend)
- Acceptance criteria for each requirement

Save the diary entry for this interaction and commit everything
together with a meaningful commit message.

# 004 — Data Fetcher Implementation

**Date**: 2026-03-30  
**Tool**: GitHub Copilot  
**Model**: Grok Code Fast 1  
**Iterations**: 1

## Prompt

**2026-03-30 00:00**

Now implement `data_fetcher.py` to pass the tests in
test_data_fetcher.py. The implementation should pass all tests.
Do not modify the tests.

Run the tests to confirm they pass. If they do, save the diary
entry and commit everything with a proper commit message that
describes what was implemented and why.

## ✅ Implementation

Implemented `fetch_so_data` function in `data_fetcher.py`:
- Checks for cached CSV file; loads if exists
- Fetches data from Stack Overflow API with retry logic (up to 3 attempts)
- Processes creation dates to year-month format and aggregates question counts
- Saves aggregated data to cache and returns DataFrame
- Handles empty responses and network errors

All tests pass successfully.

```
