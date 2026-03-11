# LLM Authority Bias Experiment

**Do LLMs evaluate arguments through social hierarchy heuristics?**

3×2×2 factorial design: Status × Expertise × Argument Type

## Repo Structure

```
authority-bias-llm/
├── notebooks/
│   ├── 01_run_experiment.ipynb   ← Runs API calls, saves data to Drive
│   └── 02_analysis.ipynb         ← Loads data from Drive, runs all analyses
├── src/
│   ├── prompts.py                ← Prompt template
│   ├── models.py                 ← API wrappers (Gemini, GPT, Claude)
│   ├── parsing.py                ← Response extraction (rating, weaknesses)
│   └── config.py                 ← Paths and settings
├── data/
│   └── .gitkeep                  ← Data lives on Google Drive, not in repo
├── .gitignore
└── README.md
```

## Setup

1. **Clone into Colab** — each notebook starts with:
   ```python
   !git clone https://github.com/YOUR_USERNAME/authority-bias-llm.git
   %cd authority-bias-llm
   ```

2. **Add API keys** via Colab Secrets (🔑 icon in sidebar):
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `ANTHROPIC_API_KEY`

3. **Data files** (`arguments.csv`, `authority.csv`) should be in your Google Drive at:
   ```
   /My Drive/PhD/2PhD 1Paper/data/
   ```

## Workflow

1. Open `01_run_experiment.ipynb` in Colab → run experiment → data saved to Drive
2. Open `02_analysis.ipynb` in Colab → loads data from Drive → figures + tables saved to Drive

## Design

| Factor         | Levels                |
|----------------|-----------------------|
| Status         | low / medium / high   |
| Expertise      | relevant / irrelevant |
| Argument type  | descriptive / normative |

12 treatment cells. Each model evaluated independently with stateless API calls.
