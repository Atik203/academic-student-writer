# Contributing

Thank you for helping improve Academic Student Writer. Contributions should make research writing more accurate, clear, and useful while preserving research integrity and author ownership.

## Before you start

- For a substantial change, open an issue first to discuss its scope.
- For a small correction, documentation fix, or clear bug, a pull request is welcome.
- Check for an existing issue or pull request that covers the same change.
- Do not include unpublished manuscripts, private participant data, credentials, or other sensitive material in issues, examples, or commits.

## Contribution principles

- Never add fabricated results, citations, evaluation claims, or unsupported detector claims.
- Do not add instructions for hiding AI involvement, bypassing detectors, or evading disclosure rules.
- Keep guidance evidence-based and distinguish established requirements from suggestions.
- Preserve the skill's plain-Markdown portability. Optional Python scripts should use only the standard library and support Python 3.8 or newer unless a change is discussed first.
- Keep examples synthetic or use material that is authorized for public release.
- Update the relevant integration notes, examples, or evaluation cases when behavior or instructions change.

## Pull requests

1. Explain the problem and the intended change.
2. Keep the change focused and update related documentation.
3. For script changes, run `bash evals/run_selftest.sh` and describe the result. For documentation-only changes, state that in the pull request.
4. Review the diff for private data, unsupported claims, broken links, and accidental changes to numbers or citations.
5. Do not bump the version or claim model/runtime evaluation unless that work was actually completed.

By submitting a contribution, you agree that it is provided under the repository's [MIT License](LICENSE).
