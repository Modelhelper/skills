---
name: create-modelhelper-project
description: Create or update the .modelhelper folder (config.yaml plus project-local templates) at the root of a codebase so the Modelhelper CLI generates code into the right folders with the right namespaces. Use when the user wants to set up Modelhelper in a project, add a config.yaml, configure locations or namespaces for generated code, or add project-specific templates that override the global ones.
---

# Create Modelhelper Project

The project file is `.modelhelper/config.yaml` (not `project.yaml`: the CLI's loader looks for `config` in the project folder, verified with `mh project`).

`mh project init` is not implemented in the CLI (the body is commented out), so create the folder by hand.

## Layout

```
<repo root>/            # same level as .git
└── .modelhelper/
    ├── config.yaml    # required: name, language, source, locations, setup
    └── templates/      # optional: project-local templates
        └── go/struct.yaml   # -> template "go-struct"
```

Commit `.modelhelper/` so the team shares it. Keep connection strings and secrets out of it (they belong in the user's `~/.modelhelper` config; reference them by key with `defaultSource`).

## How the CLI uses it

- `config.yaml` is read from `./.modelhelper/config.yaml` in the **current directory**. Run `code generate` from the repo root, or it will not see the project.
- `templates/` is found by searching upward from the cwd. Names come from the path relative to `templates/` with `/` -> `-` (same rule as the global templates), and a project template **replaces** a global one with the same name. Use this to tweak one global template for one repo.
- A template's `key` (set in the template YAML, e.g. `model`, `repo`, `router`) links it to two config.yaml maps: `locations[key]` (output folder) and `setup[key]` (namespace, prefix, postfix, imports, inject).
- Files are written to `locations[key]/<template fileName>` only with `--export-bykey` (add `--overwrite` to replace files). Without it, output goes to `--screen`, `--copy` or `--export-path`.
- Location values are themselves templates, so `core/{{ .Name | snake | singular }}` works.

## config.yaml

```yaml
version: "3.0"
name: flight-api
language: go                  # primary language, matches template `language`
description: One line about the project
defaultSource: flight         # connection key from the user's config
rootNamespace: github.com/acme/flight-api
useFileHeader: false

locations:                    # template key -> folder relative to the repo root
  model: internal/core/models
  repo: internal/ports/repository
  router: internal/ports/api
  controller: internal/ports/api/controllers

setup:                        # template key -> values exposed to the template
  model:
    namespace: models
  repo:
    namespace: repository
    postfix: Repository
    imports:
      - github.com/pkg/errors

options:                      # free-form, available as .Options in templates
  idType: int
```

Optional keys: `ownerName`, `defaultKey`, `header`, `features`, `customFeatures`, `inject`, `custom`.

## Workflow

1. Look at the repo: language, module path (`go.mod`, `*.csproj`, `package.json`), and where models, repositories and handlers already live.
2. List the template keys in use: `mh code template list --lang <language>` (the KEY column; add `--key <key>` to see which templates share one). Only add `locations`/`setup` for keys the user will generate.
3. Write `config.yaml` from the real folder layout, never invented paths.
4. Only add `templates/` files for things that differ from the global set. Use the `create-modelhelper-template` skill to write them.
5. Verify from the repo root: `mh project` must print the project name and language ("No project exists here" means the file name or folder is wrong). Then `mh code generate -t <template> --demo -s order --export-bykey` (sample data, no database; add `--overwrite` only to replace files), then with the real `-s Schema.Table`, and confirm the file lands where expected. Check the "Files exported" count in the stats trailer and the disk. Say which of the demo or real-source runs actually happened.
