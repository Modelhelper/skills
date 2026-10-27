# skills

Agent skills for working with [Modelhelper](https://github.com/Modelhelper).

| Skill | Use it to |
|-------|-----------|
| [create-modelhelper-template](create-modelhelper-template/SKILL.md) | Turn existing code into a Modelhelper template, or write one from a prompt, and validate it |
| [create-modelhelper-project](create-modelhelper-project/SKILL.md) | Set up a `.modelhelper` folder (config.yaml, locations, namespaces, project-local templates) at a repo root |

## Requirements

The skills run the `mh` CLI, so install it first (needs Go, and `$GOBIN` or `$GOPATH/bin` on your `PATH`):

```bash
go install github.com/Modelhelper/cli/v3/cmd/mh@latest
```

You also need the [Modelhelper templates](https://github.com/Modelhelper/templates). The CLI asks for their location the first time you run `mh`.

## Install

Copy or symlink a skill folder into `~/.claude/skills/` (or a project's `.claude/skills/`):

```bash
ln -s "$PWD/create-modelhelper-template" ~/.claude/skills/create-modelhelper-template
```
