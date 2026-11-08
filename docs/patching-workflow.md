# Troubleshooting and patching a packaged program

A repeatable process for fixing a program on a device by building a patched package, based on this repo's history. Each step produces evidence; do not tick a step without it.

## 1. Baseline (read-only)
- Record installed package versions, binary checksums, service state and whether any user data exists.
- Save the original packages and their SHA-256 sums. This is the rollback set; do it before any install.
- Reproduce the failure and note the exact error text.

## 2. Provenance
- Identify what source the installed binary was built from (`go version -m`, strings, package metadata).
- Find the upstream fix or fork. Read its diff before trusting it; prefer small, readable changes.

## 3. Reproducible CI build
- Fork, pin the source by full SHA, build with fixed flags (static, `-trimpath`, stripped).
- Publish a checksum and build info. Build twice and compare hashes.
- Keep packaging files separate from the pinned source.

## 4. Package
- Mirror the original package's file list, bump the version, and make upgrade restart the service.
- Inspect the built package before install: files, requires, scripts, payload format.

## 5. Stage and install
- Copy to a scratch directory in the user's home (never a system path) and verify the checksum on the device.
- Dry run first (`rpm -U --test`), then upgrade in place. Keep the previous package for rollback.
- Verify package version, binary hash and service start time after the upgrade.

## 6. Test the real behaviour
- Change one thing at a time. Do not repeat credentialed actions in a loop; accounts can be rate limited.
- Report which step failed (use labelled errors), never URLs, tokens or passwords.
- When a client fails, test the service with a protocol-level script first (here: one IMAP LOGIN with a stdlib socket client) to separate service from client problems.
- Check form fields: host and port are separate fields.

## 7. Release and clean up
- Tag a pre-release with the package and checksums once it works on the device.
- Remove staged files from the device, including anything holding secrets.
- Keep session notes and personal details out of the public repo.

## Gotchas seen
- A GUI that starts a CLI login without a controlling terminal fails reading the password (`/dev/tty` error).
- Two readers on one stdin race for input; share one reader.
- Minimal devices often lack `nc`, `ss` and `/dev/tcp`; use the Python or Perl already installed.
