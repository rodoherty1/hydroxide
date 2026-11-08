# hydroxide fork (patched Sailfish OS build)

Fork of DanteCpp/hydroxide (Proton Mail bridge with CAPTCHA support), used to build an unofficial `harbour-hydroxide` RPM for aarch64 Sailfish OS.

## Constraints
- Source is pinned by full SHA in `.github/workflows/build-arm64.yml` (`SOURCE_COMMIT`): branch `fix-captcha-stdin`, which adds a stdin fix on DanteCpp/hydroxide@60a7c7e8. Changing it needs a new RPM version.
- Build in CI only: Go from go.mod, `CGO_ENABLED=0`, `GOOS=linux GOARCH=arm64`, `-trimpath`, stripped.
- This branch holds build, packaging and docs only. Do not use it as a PR source.

## Device work
- Read-only by default; ask before any write to a device.
- Root steps are run by the device owner.
- Never read, print or log config/auth files, bridge passwords or CAPTCHA tokens.
- Save the original packages and their checksums before any install.

## Docs
`docs/patching-workflow.md` describes the repeatable process; `docs/plan-template.md` is a checklist to copy for a new exercise.
