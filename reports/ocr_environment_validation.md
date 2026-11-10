# Milestone 2B.5A — OCR Environment and Test Failure Investigation

## 1. Verified Environment

The VS Code/Pylance workspace interpreter is the project virtual environment:

`/Users/tusharpandey/Documents/CS2_PolicyLens/.venv/bin/python`

| Environment | Python | PyMuPDF distribution version | `pymupdf.__version__` | Notes |
|---|---:|---:|---:|---|
| Project `.venv` (VS Code selected) | 3.15.2 | 1.28.2 | 1.28.2 | Intended project interpreter |
| Anaconda selected by bare `python` in the shell | 3.14.6 | 2.1 | 2.1 | Not the project interpreter |

In the project `.venv`, `pytesseract` and Pillow are not installed. They are
listed in `requirements.txt`, but the current OCR module invokes the Tesseract
CLI directly and uses PyMuPDF to render pages; it does not import either
package. Python-package presence does not install the Tesseract executable or
its trained language data.

The operating system is macOS on Apple Silicon (Darwin ARM64). No `tesseract`
executable was found on `PATH`, and the OCR module's own preflight reports:

> Tesseract executable not found: tesseract.

Accordingly, the Tesseract version is unavailable, and the presence of `eng`
and `hin` language packs cannot be verified. No software or system configuration
was installed or changed.

## 2. Failing Table Test Investigation

The existing test [test_detects_tables_and_preserves_structured_cells](../tests/test_extract.py)
creates a PDF cell containing `Loan Policy One` and asserts that the structured
table cell preserves those spaces. The source PDF's native text extraction
returns `Loan Policy One` in both tested environments.

A focused reproduction using the same generated PDF observed:

| Interpreter | PyMuPDF | `page.get_text("text")` | `page.find_tables().tables[0].extract()[1][0]` |
|---|---:|---|---|
| Project `.venv` | 1.28.2 | `Loan Policy One` | `Loan Policy One` |
| Anaconda shell `python` | 2.1 | `Loan Policy One` | `LoanPolicyOne` |

The extraction code takes the value returned by `table.extract()` and applies
`.strip()`; it does not remove internal spaces. The change is therefore in the
PyMuPDF table-extraction result observed with version 2.1, not in this project's
table post-processing or the source PDF. In that environment, the structured
table value is genuinely incomplete because word boundaries are lost, even
though the ordinary text layer still contains the spaces.

The test expectation is valid for the project-selected and tested environment.
It was not changed. The test itself already provides regression coverage for
the cell's word boundaries. To keep dependency resolution from selecting the
observed incompatible major version, `requirements.txt` now constrains PyMuPDF
to `>=1.24.0,<2.0`. This is based on the verified passing 1.28.2 and failing
2.1 behavior; it is not a claim that every PyMuPDF 1.x release was tested.
No production extraction code was modified.

The earlier `21 passed, 1 failed` result came from running bare `python`, which
resolved to Anaconda rather than the VS Code-selected `.venv`. Using the
project interpreter explicitly resolves the discrepancy.

## 3. OCR Setup Requirements for This Mac

Homebrew is present at `/opt/homebrew/bin/brew`, but neither Tesseract package
is installed. Homebrew's current `tesseract` formula includes `eng` and `osd`;
the separate `tesseract-lang` formula supplies additional languages, including
Hindi.

Install the system OCR engine and language data explicitly:

```bash
brew install tesseract
brew install tesseract-lang
```

Then verify the actual executable and languages before running OCR:

```bash
command -v tesseract
tesseract --version
tesseract --list-langs
```

The language listing must include both `eng` and `hin`. If Homebrew's binary
is not on the shell `PATH`, configure the executable path in the project's
`.env` (Apple Silicon's default prefix is shown):

```text
TESSERACT_CMD=/opt/homebrew/bin/tesseract
```

The path can be checked with `brew --prefix tesseract`. Only after the
executable and both language codes are confirmed should the project run:

```bash
.venv/bin/python -m src.ocr
```

No Python-only install command can satisfy these system prerequisites.

## 4. Code and Test Changes

- Updated `requirements.txt` from `PyMuPDF>=1.24.0` to
  `PyMuPDF>=1.24.0,<2.0`, because version 2.1 demonstrably drops spaces from
  table-cell extraction.
- Updated `README.md` with the separate Homebrew installation for Hindi
  language data and explicit `.venv` test/OCR commands.
- Did not alter the existing table test or production extraction code.
- Did not run corpus OCR or modify PDFs, manifest metadata, or processed JSONL
  files.

## 5. Verification Results

All commands below use the project interpreter:

| Verification | Result |
|---|---|
| Targeted table test: `.venv/bin/python -m pytest tests/test_extract.py::test_detects_tables_and_preserves_structured_cells -q` | **1 passed** |
| Full suite: `.venv/bin/python -m pytest tests/ -q` | **22 passed** |
| Compilation: `.venv/bin/python -m compileall -q src tests` | **Passed** |
| OCR engine preflight | **Blocked: executable not found** |
| `eng`/`hin` language verification | **Not possible until Tesseract is installed** |
| Corpus OCR | **Not run** |

The passing test run emits upstream PyMuPDF/Python deprecation warnings; there
are no test failures in the project `.venv`.

## 6. Readiness Assessment

The Python project environment is the intended `.venv`, and its targeted and
complete test suites pass. The previous table-test failure was caused by using
the separate Anaconda interpreter with PyMuPDF 2.1. The dependency range now
excludes that observed table-spacing regression.

**The project is not yet ready for actual OCR execution.** Tesseract itself is
absent, and neither required language pack can currently be verified. Install
Tesseract and its language data using the commands above, confirm `eng` and
`hin` with `tesseract --list-langs`, then rerun the engine preflight before
processing the corpus.
