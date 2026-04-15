# COPI Development and Release Pipeline

This document describes the full lifecycle of a COPI ontology update: from editing a class in the COPIeditor tool, through the automated GitHub Actions pipeline, to the final deployment at the official IRI.

---

## Architecture overview

Two separate repositories are involved:

| Repository | Purpose |
|---|---|
| [`INF-UFRGS-Ontologies/COPI`](https://github.com/INF-UFRGS-Ontologies/COPI) | Ontology source, release artefacts, static HTML docs |
| [`n0santos/COPIeditor`](https://github.com/n0santos/COPIeditor) | Web tool for term aggregation, LLM-assisted axiomatization, and OWL export |

The COPIeditor tool is deployed locally (Docker) and communicates with the COPI repo via the GitHub API. It never modifies ontology files directly — it submits pull requests.

---

## Step 1 — Edit classes in COPIeditor

COPIeditor aggregates terms from industrial standards (ISO 15926-4, ISO 14224, CFIHOS, DEXPI, POSC Caesar RDL, SLB Glossary) and provides a workbench for ontology axiomatization.

1. Start the tool locally:
   ```bash
   docker compose up -d
   ```
   Then open `http://localhost:8765`.

2. Navigate to **Enrich** to find the equipment cluster you want to work on.

3. Use the LLM-assisted workbench to define:
   - The **identity-giving function** (subtype of `DesignedFunction`)
   - The **genus** (most specific known superclass)
   - **Necessary parts** (`hasComponentPartAtAllTimes` restrictions)
   - **Process participation signature** (typed input/output participants)

4. Choose an **axiom mode**:
   - `equivalent` — for functional basis (e.g., control valve, separator): the DesignedFunction is necessary and sufficient, enabling automatic reasoner classification.
   - `necessary` — for constructive basis (e.g., ball valve, reciprocating compressor): structural differentia are necessary conditions only; OWA makes equivalence unsafe.
   - `mixed` — when both apply (e.g., centrifugal pump).

5. Set the status to **Validated** once the axiomatization is reviewed.

---

## Step 2 — Export a PR from COPIeditor

Once one or more classes are validated, use the **Export → GitHub PR** feature in COPIeditor:

1. Go to **Enrich → Export → GitHub**.
2. Provide a GitHub personal access token with `repo` scope for `INF-UFRGS-Ontologies/COPI`.
3. Optionally write a commit message.
4. Click **Submit**.

The tool will:
- Generate updated OWL axioms for the validated classes and patch them into `src/ontology/copi-edit.owl`
- Regenerate static HTML documentation pages under `docs/classes/`
- Create a new branch `enrichment/YYYYMMDD-HHMMSS` in the COPI repo
- Open a pull request targeting `main`

The PR includes both the ontology edit file and the updated HTML docs so reviewers can inspect both.

---

## Step 3 — Review and merge the PR

Once the PR is open on `INF-UFRGS-Ontologies/COPI`:

1. The **ODK QC workflow** (`qc.yml`) runs automatically and validates the ontology with a reasoner (HermiT). Check that it passes before merging.
2. Review the OWL diff in `src/ontology/copi-edit.owl` and the HTML preview in `docs/classes/`.
3. Merge the PR when QC passes.

---

## Step 4 — Automated release pipeline (GitHub Actions)

Merging to `main` triggers `.github/workflows/deploy.yml`, which has two sequential jobs.

### Job 1 — `generate` (runs on `ubuntu-latest` + ODK container)

Uses the [Ontology Development Kit](https://github.com/INCATools/ontology-development-kit) Docker image (`obolibrary/odkfull:v1.6`) to produce release artefacts:

```bash
cd src/ontology
make prepare_release IMP=false PAT=false MIR=false COMP=false
```

Flags used:
- `IMP=false` — skip re-downloading imports (uses committed mirrors under `src/ontology/mirror/`)
- `PAT=false` — skip SPARQL pattern processing
- `MIR=false` — skip mirror refresh
- `COMP=false` — skip component regeneration

ODK writes the following artefacts directly to the **repository root** (configured via `RELEASEDIR=../..` in the Makefile):

| File | Description |
|---|---|
| `copi.owl` / `copi.ttl` | Primary release (full, imports merged) |
| `copi-base.owl` / `copi-base.ttl` | Base (no imports merged) |
| `copi-full.owl` / `copi-full.ttl` | Full (explicit imports merged) |
| `copi-simple.owl` / `copi-simple.ttl` | Simplified (inferred hierarchy only) |

The job then commits these artefacts back to `main` with `[skip ci]` (to avoid re-triggering the workflow) and creates a **GitHub Release** tagged `vYYYY-MM-DD` with all 8 files attached as downloadable assets.

### Job 2 — `deploy` (runs on `arc-runner`, after `generate`)

Transfers files to the UFRGS ontologies web server (`REDACTED`) via SFTP under the `ontokg` user. Four uploads happen:

| Source | Destination on server | Resolves to |
|---|---|---|
| `docs/` | `public_html/copi/docs/` | `https://www.inf.ufrgs.br/ontologies/copi/docs/` |
| `copi-*.owl/ttl` | `public_html/copi/` | `https://www.inf.ufrgs.br/ontologies/copi/copi-base.owl` etc. |
| `copi.owl`, `copi.ttl` | `public_html/` | `https://www.inf.ufrgs.br/ontologies/copi.owl` |
| All artefacts | `public_html/copi/releases/YYYY-MM-DD/` | `https://www.inf.ufrgs.br/ontologies/copi/releases/2026-04-15/copi.owl` |

---

## IRI strategy

COPI follows the standard OWL versioning pattern:

- **`owl:ontologyIRI`** — `https://www.inf.ufrgs.br/ontologies/copi.owl`  
  Always resolves to the **latest** release. Use this for general imports.

- **`owl:versionIRI`** — `https://www.inf.ufrgs.br/ontologies/copi/releases/YYYY-MM-DD/copi.owl`  
  Resolves to a **frozen snapshot** of that specific release. Use this in publications, datasets, and any context where reproducibility of reasoning is required.

This pattern is aligned with OBO Foundry principles and is used by BFO, IAO, and RO.

---

## Infrastructure requirements

### GitHub secrets

The following secrets must be configured in `INF-UFRGS-Ontologies/COPI` → Settings → Secrets:

| Secret | Description |
|---|---|
| `GITHUB_TOKEN` | Automatically provided by GitHub Actions (no setup needed) |
| `FTP` | Password for `ontokg@REDACTED` (UFRGS SFTP server) |

### Self-hosted runner

The `deploy` job requires an `arc-runner` self-hosted runner registered to the `INF-UFRGS-Ontologies` organization. The `generate` job runs on GitHub-hosted `ubuntu-latest` and does not require a self-hosted runner.

To register a new runner, follow the [Actions Runner Controller (ARC)](https://github.com/actions/actions-runner-controller) documentation and add it to the organization.

### Server directory structure

The following directories must exist on the UFRGS server before the first deploy. They are not created automatically by the SFTP action:

```
/home/www/ontologies/public_html/
├── copi/
│   ├── docs/
│   │   └── classes/
│   └── releases/       ← created per-deploy by the workflow
```

Run once to initialise:
```bash
ssh ontokg@REDACTED
mkdir -p /home/www/ontologies/public_html/copi/docs/classes
```

The `releases/` subdirectories are created automatically by the workflow on each deploy.

---

## Dependency versions

| Component | Version |
|---|---|
| ODK | `obolibrary/odkfull:v1.6` |
| BFO import | `bfo-2020` (mirror: `purl.obolibrary.org/obo/bfo/2020/bfo-core.ttl`) |
| IOF-Core import | `202601` (mirror: `spec.industrialontologies.org/ontology/202601/core/Core/`) |
| SFTP action | `Dylan700/sftp-upload-action@latest` |

To update an import mirror, edit the `mirror_from` URL in `src/ontology/copi-odk.yaml` and replace the file in `src/ontology/mirror/`.

---

## Troubleshooting

**`generate` job fails with "No rule to make target 'imports/X_import.owl'`"**  
An import listed in `IMPORTS` inside the Makefile does not have a corresponding mirror or target. Check that `src/ontology/copi-odk.yaml` and the Makefile `IMPORTS` variable are in sync.

**`generate` job fails with `cp: cannot stat 'src/ontology/copi.owl'`**  
ODK writes artefacts to the repo root (via `RELEASEDIR=../..`), not to `src/ontology/`. Remove any `cp` steps that assume the old path.

**`deploy` job never starts**  
The `arc-runner` is not registered or is offline. The `generate` job runs independently on GitHub-hosted runners and will still complete.

**SFTP upload fails with "no such file or directory"**  
The target directory does not exist on the server. The SFTP action does not create parent directories. SSH into the server and create the path manually (see above).

**GitHub Release creation fails with "already exists"**  
Two workflow runs on the same calendar day will try to create the same `vYYYY-MM-DD` tag. The step handles this gracefully with `|| echo "... skipping."` — no action needed.
