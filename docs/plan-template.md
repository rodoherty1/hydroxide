# Plan: <what is being fixed>

`[ ]` todo, `[x]` done. Tick a step only after verifying it and note the evidence (checksum, run URL, command output).

## Phase 0 - Baseline (read-only)
- [ ] Installed versions, checksums, service state recorded
- [ ] Original packages saved with checksums (rollback set)
**Gate:** rollback set exists.

## Phase 1 - Provenance and CI build
- [ ] Source of the installed binary identified
- [ ] Candidate fix reviewed
- [ ] Fork, pinned SHA, CI build; checksums recorded; second build matches

## Phase 2 - Package
- [ ] Spec mirrors original file list; version bumped
- [ ] Built package inspected (files, requires, scripts)

## Phase 3 - Install
- [ ] Staged and checksum verified on the device
- [ ] Dry run clean; upgraded in place
- [ ] Version, binary hash and service restart verified
**Rollback:** reinstall the saved original with `--oldpackage`.

## Phase 4 - Verify behaviour
- [ ] Failure scenario retried once; result recorded by step label

## Phase 5 - Release and clean up
- [ ] Pre-release tagged with checksums
- [ ] Staged files removed from the device
- [ ] Repo contains no personal or session details
