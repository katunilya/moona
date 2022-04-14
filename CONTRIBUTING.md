# Contribution Guidelines

- No direct pushes to `main` (restricted by GitHub);
- Branch-per-issue;
- Name branches according to GitHub: `<issue_number>-<issue_title>`;
- Docstrings are mandatory (google style);
- Remember to use linters and formatters to keep code consistent;
  - `flake8` with extensions (black compatible);
  - `black` for formatting;
  - `isort` for sorting imports (black compatible mode);
- Tests are mandatory (via `pytest`);

Most of this rules are secured by GitHub Settings of the repository. Just keep code simple and
declarative enough.
