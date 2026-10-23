# NextTime preflight

Recorded 2026-10-23 for the initial local foundation. Project code and tests target Python 3.12; the audit-only system interpreter is not a substitute project runtime.

## Available and exercised

| Capability | Recorded version/state |
| --- | --- |
| Project interpreter | Source-built CPython 3.12.12 with zlib and SQLite support |
| Package manager | uv 0.9.5; `uv.lock` is frozen for normal bootstrap |
| Quality tools | Ruff 0.13.2; mypy 1.18.2; pytest 9.0.3; pytest-cov 6.3.0 |
| Runtime dependencies | None for the current domain package |
| Audit-only runner | System CPython 3.11.2 with OpenSSL 3.0.20, used to audit the installed 3.12 site-packages |

The source-built 3.12 interpreter lacks `_ssl`, `_bz2`, `_lzma`, and `_ctypes`. Tests, builds, and fixture execution pass, but its own `pip-audit` cannot make TLS requests. The recorded audit therefore used the separate SSL-capable runner against `.venv/lib/python3.12/site-packages`. Normal development should use a complete Python 3.12 installation so `make test-security` is self-contained.

## Blocked or not implemented

- Actual Bee/Apple Watch hardware, Developer Mode, and documented CLI/MCP ingestion.
- macOS/Xcode/SwiftUI iOS application, notifications, and on-device Speech validation.
- AWS credentials and deployed Bee bridge, Polly, Transcribe, Bedrock, storage, and database.
- Transcript lifecycle/deletion workers, authentic participant data, and accent/device evaluation.
- User research, learning outcomes, deployment, and release evidence.

## First local checks

```bash
python3.12 --version
uv --version
make bootstrap
make lint typecheck test-unit test-contract test-security build
make dev
```

Do not bypass the audit because a local interpreter lacks SSL. Use a complete 3.12 runtime or an explicitly recorded SSL-capable audit runner against the locked environment.
