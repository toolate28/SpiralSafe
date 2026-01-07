# SIGNOFF CHECKLIST — SpiralSafe docs reorg

Use this checklist before merging the docs reorg PR. Add checkboxes and sign off on each item.

Pre-merge verification
- [ ] All moved files are present under docs/ and readable
- [ ] Pointer files exist at the repository root for moved filenames
- [ ] .gitattributes includes LFS tracking for binary/zip files (if used)
- [ ] Link-check run: npx markdown-link-check "docs/**/*.md" (no unresolved broken links)
- [ ] pre-commit hooks run locally: pre-commit run --all-files (fix issues or document exceptions)
- [ ] CI workflows run successfully for the PR (GitHub Actions)
- [ ] No secrets or sensitive data introduced in moved docs (scan with trufflehog or repo scanner)
- [ ] Owners assigned in docs/ops/OWNERS.md or CODEOWNERS updated to include docs area

Release & operational notes
- [ ] If binary assets are LFS-tracked, ensure LFS is enabled for the organization and instructions added to docs/ops/LFS.md
- [ ] If any scripts or workflows reference old paths, update them and run CI smoke tests
- [ ] Create or update ADRs in docs/DECISIONS.md for any architectural merges or canonicalizations performed during reorg

Sign-off
- [ ] Author verification: ____________________  (name, date)
- [ ] Docs owner verification: ____________________  (name, date)
- [ ] Security review (if applicable): ____________________  (name, date)
- [ ] Final approver & merge: ____________________  (name, date)
