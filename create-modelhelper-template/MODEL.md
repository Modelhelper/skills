# Sample model

`--demo` renders against sample tables built into the `mh` binary, no database needed: `customer`, `order`, `orderItem`, `product`. Use it to see exactly what a template receives.

```bash
mh code generate -t go-db-repo --demo -s order --screen
```

Add `--code-only` to print only the code (no statistics or slogan), e.g. to pipe it to `gofmt -e`.

## What `order` looks like to a template (`model: entity`)

Source (`order.yaml`): schema `dbo`, columns `Id` (int, identity, primary), `OrderId` (varchar), `CustomerId` (int, references `customer`), `TotalAmount` (decimal, nullable); `orderItem` references `order`.

| Expression | Value |
|------------|-------|
| `.Name`, `.Schema` | `order`, `dbo` |
| `.Name \| singular \| pascal` | `Order` |
| `.PrimaryKeys` | `Id` |
| `.NonPrimaryColumns` | `OrderId, CustomerId, TotalAmount` |
| `.Columns` | all four; `.IsLast` is true on the last |
| `{{ .DataType \| datatype }}` | language type for the column (`int`, `string`, ...) |
| `.Children` | `orderItem` (tables that reference this one) |

Notes:
- Demo columns are sorted by name, not by the YAML order.
- Demo uses mssql, so `sql-*` blocks resolve from `db/mssql`. Check postgres by reading `db/postgres` output by eye or against a real postgres source.
- Types without a mapping in the language definitions (`languages.definitions` in the config, e.g. `decimal` for go) pass through unchanged. If the generated type looks wrong, fix the definition, not the template.
