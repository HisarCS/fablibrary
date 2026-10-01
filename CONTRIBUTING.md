# Contributing (for lab assistants)

1. **Ran a test?** Open *Issues → New issue → Test result* and fill in the form: measured value, photo, decision.
2. **Need to change files?** Create a branch: `git checkout -b ws/slot-3.15`
3. Change the parameter in the generator script and run `python projects/welcome-space/generators/build.py`.
4. Add a line to `CHANGELOG.md` (what changed, which issue).
5. Open a Pull Request and reference the issue (`Closes #12`). Once approved it merges into `main` and the site updates automatically.

## Version tags
`v1-proto1`, `v1-proto2`, `v1.0-pilot`, `v1.0-final`. Every set that goes to the machines gets a tag.

## File rules
- Use Releases or Git LFS for large files (Bambu `.3mf` projects, high-resolution photos).
- No student faces, names or class information in photos.
