# termux-store-db

Community-maintained metadata for Termux native packages, used by
[termux-store](https://github.com/eobarretooo/termux-store).

This repository does not replace Termux package repositories. It adds the
missing human layer: categories, GUI/X11 notes, screenshots, launch commands,
tips, and community compatibility ratings.

## How it works

`termux-store` gets the real package list from `pkg list-all`. It then downloads
`packages/index.json` from this repository and enriches matching packages with
metadata.

No backend server is required. Contributions are regular GitHub pull requests.

## Repository layout

```text
termux-store-db/
  categories/categories.json
  packages/_template.json
  packages/index.json
  packages/vim.json
  schema/package.schema.json
  scripts/generate_index.py
  scripts/validate.py
```

## Package metadata format

Each package is stored as one JSON file in `packages/`.

```json
{
  "name": "vim",
  "termux_package": true,
  "gui": false,
  "x11_required": false,
  "category": "development",
  "short_description": "Powerful terminal text editor",
  "long_description": "Vim is a configurable text editor that runs well inside Termux without X11.",
  "install_command": "pkg install vim",
  "launch_command": "vim",
  "tips": [
    "Run vimtutor to learn the basics."
  ],
  "screenshots": [],
  "community_rating": {
    "works_great": 0,
    "unstable": 0,
    "broken": 0
  },
  "submitted_by": "eobarretooo",
  "last_updated": "2026-05-24"
}
```

## Contributing

1. Copy `packages/_template.json` to `packages/<package-name>.json`.
2. Fill in the fields using the exact package name from Termux.
3. Add optional screenshots under `screenshots/<package-name>/`.
4. Run validation:

```bash
python scripts/validate.py
python scripts/generate_index.py --check
```

## Rules

- Only native Termux packages are accepted.
- Do not add proot-only, root-only, Docker-only, or Android APK entries.
- Keep `short_description` under 80 characters.
- Use categories from `categories/categories.json`.
- Screenshot paths must point to files committed in this repository.

## License

MIT
