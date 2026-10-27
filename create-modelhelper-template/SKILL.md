---
name: create-modelhelper-template
description: Create or edit Modelhelper CLI code templates (YAML + Go text/template) in the templates repo, either by turning existing code into a template or by writing one from a prompt. Use when the user wants a new modelhelper/mh template, says "make this a template", templatize code, or adds SQL/db templates for mssql or postgres.
---

# Create Modelhelper Template

Assumes only the installed `mh` binary. Template folders are listed in `~/.modelhelper/config.yaml` under `templates.code` (code), `templates.database` (SQL) and `languages.definitions` (type mappings for `datatype`). Edit templates in the first `templates.code` / `templates.database` path, which is normally a git checkout of the templates repo.

Discover before writing:
- `mh code template list --lang go --db mssql` lists names, types, keys and models.
- `mh code template detail <name>` prints one template with its source path; its closest siblings are the best style guide.

## Naming and location (the YAML `name:` field is ignored)

The name is the file path relative to the root, `/` becomes `-`, extension dropped, lowercased.
- `code/go/blocks/db/paged.yaml` -> `go-blocks-db-paged`
- `db/mssql/sql-select-paged.yaml` -> `sql-select-paged`

Database templates are separate: `db/mssql/` and `db/postgres/`, and only the folder matching the source connection's type is loaded. A SQL block referenced from a Go template (`{{ template "sql-select-paged" . }}`) must exist in **both** folders, with the same name, in each dialect's syntax (mssql: `@name`, `[brackets]`, `OUTPUT`/`SCOPE_IDENTITY()`; postgres: `$1`, `RETURNING`).

Before inventing a name, list `code/<lang>/` and `db/*/` and reuse the existing naming style.

## File format

```yaml
version: 3
language: go            # go, sql, cs, ts ...
type: block             # block = fragment other templates include; file = generated file
short: One line on what it generates
key: model              # file type only: model | core | repo | router ... (look at siblings)
model: entity           # entity = one table
fileName: "{{ .Name | kebab }}.go"   # file type only
body: |
  ...
```

Use `block` for anything reused (SQL, function bodies, argument lists); compose with `{{ template "go-blocks-..." . }}`. Use `file` for a whole output file.

## Template data and functions

Entity fields (worked example in [MODEL.md](MODEL.md)): `.Name .Schema .Namespace .Columns .PrimaryKeys .NonPrimaryColumns .Children .OwnerName .NameWithoutPrefix .RelatedColumn`. Column: `.Name .DataType .NameWithoutPrefix .IsLast`.
Functions: `plural singular pascal camel snake kebab macro train dot title lower upper words sentence append increment datatype nullable`. `{{ .DataType | datatype }}` maps a SQL type to the language type.

## Workflow: from existing code

1. Read the code and pick one concrete entity as the example.
2. Replace entity-specific names with data: table name -> `{{ .Name | singular | pascal }}`, fields -> `{{ range .Columns }}`, the pk -> `.PrimaryKeys`. Separators: use `{{ if not .IsLast }}, {{ end }}` or `{{ if $index }},{{ end }}`.
3. Split reusable pieces (the SQL, the pk argument list) into `block` templates; check `code/go/blocks/` first.
4. Keep generated code compiling: preserve imports, error wrapping and logging style from the source.

## Workflow: from a prompt

Find the closest existing template in the same language, copy its structure and conventions, then adapt. Ask one question if the entity shape (single table, children, paging) is unclear.

## Validate (always)

1. Render against the built-in sample data, no database needed: `mh code generate -t <template-name> --demo -s order --screen`. A bad `{{ template "x" }}` reference, unknown function or syntax error is reported here. Sample data and what each field holds: [MODEL.md](MODEL.md).
2. For Go output, use `--code-only`, save it and run `gofmt -e` on it.
3. Run it for a second entity with children and nullable columns (`-s orderItem`), and with `--db`-specific SQL for both `mssql` and `postgres` when you added a SQL block.
4. If a database is reachable, repeat with the real source: `mh code generate -t <name> -s Schema.Table --screen`.
5. Optional, needs python3: `python3 <skill dir>/scripts/check-refs.py` from the templates root lists every `{{ template }}` reference that resolves to nothing, across all templates.

Do not commit unless asked.
