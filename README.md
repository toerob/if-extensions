# IF Extensions Registry

This repository is the extension registry for [pif](https://github.com/toerob/pif), the package manager for interactive fiction authoring systems.

## Directory structure

```
registry/
  {system}/
    {namespace}/
      {package-id}/
        package.yaml
        releases/
          v1.0.0.yaml
          v2.0.0.yaml
```

### Systems

| Directory | Authoring system |
|-----------|-----------------|
| `tads3`   | TADS 3          |
| `inform`  | Inform 7        |
| `inform6` | Inform 6        |
| `dialog`  | Dialog          |

### Namespaces

The namespace groups related packages under a single directory. Use a kebab-case slug of the author's name (e.g. `aaron-reed`, `eric-eve`). For packages sourced from the IF Archive with no clear individual publisher, use `if-archive`.

The structure is always exactly three levels deep: `{system}/{namespace}/{id}/`. A fourth level is not supported — `pif` looks for `package.yaml` at the third level and will not find it any deeper. 

### Package ID

The package ID is a unique, lowercase, kebab-case identifier for the extension (e.g. `smarter-parser`, `t3cartographer`). It must be unique within the system — across all namespaces.

---

## `package.yaml` — schema version 1

Describes the extension itself. Written once; rarely changes.

```yaml
schema-version: 1
id: smarter-parser
name: Smarter Parser
author: Aaron Reed
description: Understands a broader range of input than the standard parser.
tags:
  - parser
  - inform
```

| Field            | Required | Description                                      |
|------------------|----------|--------------------------------------------------|
| `schema-version` | yes      | Always `1`                                       |
| `id`             | yes      | Unique identifier (lowercase, kebab-case)        |
| `name`           | yes      | Human-readable display name                      |
| `author`         | yes      | Original author(s) of the extension              |
| `description`    | no       | Short description                                |
| `tags`           | no       | List of searchable tags                          |

---

## `releases/v{version}.yaml` — schema version 1

One file per release. The filename encodes the version.

### Version filename conventions

- Standard semver: `v1.2.3.yaml`
- Inform releases include the Inform branch: `v16-i10.1.yaml` (extension version 16, targeting Inform branch 10.1)
- Snapshot / rolling releases: `vSNAPSHOT.yaml`

### Full schema

```yaml
schema-version: 1
maintainer: Aaron Reed
channel: stable
date: '2024-01-15'
description: Optional per-release description or changelog note.
compatibility:
  inform:
    constraint: '>=10.1'
dependencies:
  - id: conversation-framework
    constraint: '>=6'
source:
  url: https://github.com/i7/extensions/blob/10.1/Aaron%20Reed/Smarter%20Parser-v16.i7x
  format: i7x
  branch: main
build:
  exports:
    - type: lib
      path: t3cartographer/cartographer
  private:
    - type: extension
      path: Smarter Parser-v16.i7x
```

| Field            | Required | Description                                                      |
|------------------|----------|------------------------------------------------------------------|
| `schema-version` | yes      | Always `1`                                                       |
| `maintainer`     | no       | Person maintaining this registry entry (may differ from author) |
| `channel`        | no       | `stable` or `beta`. Defaults to `stable` if absent              |
| `date`           | no       | Release date in `YYYY-MM-DD` format                             |
| `description`    | no       | Per-release notes or changelog                                   |
| `compatibility`  | no       | Version constraints per system (see below)                      |
| `dependencies`   | no       | List of required extensions (see below)                         |
| `source`         | yes      | Where to download the extension (see below)                     |
| `build`          | no       | Install instructions for the package manager (see below)        |

### `source`

```yaml
source:
  url: https://github.com/owner/repo.git
  format: git
  branch: main
```

| Field    | Required | Description                              |
|----------|----------|------------------------------------------|
| `url`    | yes      | Download URL                             |
| `format` | yes      | One of the formats listed below          |
| `branch` | no       | Git branch (only relevant for `git` format) |

#### Source formats

| Format  | Description                            |
|---------|----------------------------------------|
| `git`   | Git repository (cloned/pulled)         |
| `zip`   | ZIP archive                            |
| `h`     | Single Inform 6 `.h` header file       |
| `t`     | Single TADS 3 `.t` source file         |
| `i7x`   | Inform 7 single-file extension         |
| `i7xd`  | Inform 7 directory extension           |
| `dg`    | Single Dialog `.dg` file               |

For GitHub blob URLs (`/blob/`), pif automatically rewrites them to `raw.githubusercontent.com` for download.

### `compatibility`

Constrains which version of the authoring system this release targets. Currently used for Inform 7 branch targeting.

```yaml
compatibility:
  inform:
    constraint: '>=10.1'
```

Constraint syntax follows npm-style semver ranges: `>=10.1`, `>=9.3 <10`, `>=11.0`.

### `dependencies`

Lists other extensions required by this one. Not yet installed automatically by pif — listed as a notice during install.

```yaml
dependencies:
  - id: conversation-framework
    constraint: '>=6'
  - id: epistemology   # tracks what characters know/have seen; an Inform 7 extension by Eric Eve
```

| Field        | Required | Description                                    |
|--------------|----------|------------------------------------------------|
| `id`         | yes      | Package ID of the dependency                   |
| `constraint` | no       | Version constraint (semver range)              |

### `build`

Tells pif how to wire up the extension after installation.

```yaml
build:
  exports:
    - type: lib
      path: t3cartographer/cartographer
    - type: source
      path: src/main.t
    - type: define
      value: USE_HTML
  private:
    - type: extension
      path: Smarter Parser-v16.i7x
```

**`exports`** — flags added to a TADS 3 `.t3m` makefile when pif detects one in the project:

| `type`    | Makefile flag generated      |
|-----------|------------------------------|
| `lib`     | `-lib {path}`                |
| `source`  | `-source {path}`             |
| `define`  | `-D {value}`                 |

**`private`** — metadata for the package manager's own use (e.g. the installed filename for Inform extensions). Not added to makefiles.

---

## Example: minimal TADS 3 entry

`registry/tads3/tomas-oberg/t3cartographer/package.yaml`:
```yaml
schema-version: 1
id: t3cartographer
name: t3cartographer
author: Tomas Öberg
description: Generates a map from TADS 3 source code (SVG, HTML, DOT, ASCII).
tags:
  - mapping
  - tads3
```

`registry/tads3/tomas-oberg/t3cartographer/releases/v0.7.0.yaml`:
```yaml
schema-version: 1
maintainer: Tomas Öberg
date: '2022-08-14'
source:
  url: https://github.com/toerob/t3cartographer/archive/refs/tags/v0.7-beta.1.zip
  format: zip
build:
  exports:
    - type: lib
      path: t3cartographer/cartographer
```

## Example: Inform 7 entry with branch targeting

`registry/inform/aaron-reed/smarter-parser/releases/v16-i10.1.yaml`:
```yaml
schema-version: 1
maintainer: Aaron Reed
channel: stable
compatibility:
  inform:
    constraint: '>=10.1'
source:
  url: https://github.com/i7/extensions/blob/10.1/Aaron%20Reed/Smarter%20Parser-v16.i7x
  format: i7x
build:
  private:
    - type: extension
      path: Smarter Parser-v16.i7x
```
