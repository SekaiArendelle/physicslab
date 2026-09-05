# AGENTS.md — Developer Guide for `physicslab`

This file is the entry point for AI coding agents. It contains the development workflow, build/test commands, and coding conventions.

## Mandatory rules

- **Do NOT run git write operations without explicit human instruction.** An agent must not run `git add`, `git commit`, `git push`, open a **Pull Request**, open an **Issue**, or perform any other write operation to the repository or remote unless the human explicitly asks for it.
- After changing code, run formatting and tests (commands below).

## Development environment

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) for dependency management and building

Install dependencies (creates `.venv` automatically):

```sh
uv sync
```

## Quick commands (run from repository root)

### Run tests

```sh
uv run coverage run -m unittest tests -v
```

### View coverage report

```sh
uv run coverage report
```

### Build package

```sh
uv build
```

Outputs `.tar.gz` and `.whl` to `dist/`.

### Code formatting

```sh
uv format
```

### Build docs

```sh
uv run mkdocs build
```

Outputs static site to `site/`.

### Preview docs

```sh
uv run mkdocs serve
```

Opens a local server at `http://127.0.0.1:8000`.

### Run a single test module

```sh
uv run python -m unittest tests.test_celestial_experiment -v
```

### Run a single test case

```sh
uv run python -m unittest tests.test_celestial_experiment.TestCelestialExperiment.test_merge -v
```

## Workflow

1. **Locate** – Read the relevant module under `physicslab/` to understand what to modify.
2. **Code** – Follow the [Coding conventions](#coding-conventions) below.
3. **Test** – Run the full test suite, or the specific test module you changed.
4. **Review** – After a substantive code change, verify correctness manually.
5. **Submit** – Do NOT run any git write operations without explicit human instruction.

## Coding conventions

- Follow existing code style in the file you are editing.
- Use type hints where the surrounding code already uses them.
- Keep changes focused and minimal.
- Preserve backward compatibility unless the change intentionally updates behavior.
- Add or update tests when behavior changes.
- Do not introduce new external dependencies without discussion.
- Do not commit secrets, keys, or credentials.

### Comments and docstrings

- All comments must be in English.
- Describe problems objectively; do not use profanity or emotional language in comments.
- Single-line docstrings must end with a period: `"""Description."""`.
- Multi-line docstrings must have a blank line after the opening `"""` and before the closing `"""`:

```python
def foo(bar: int) -> str:
    """Do something with *bar*.

    Args:
        bar: The input value.

    Returns:
        A formatted string.

    """
```
