# Contributing

Thanks for improving the Termux package metadata database.

## Add a package

```bash
cp packages/_template.json packages/<package-name>.json
```

Edit the new file and keep the `name` field equal to the real Termux package
name used with `pkg install`.

## Validate locally

```bash
python scripts/validate.py
python scripts/generate_index.py --check
```

If `pkg` is available, validation also checks whether each package exists in
Termux. Outside Termux, that check is skipped.

## Screenshots

Place screenshots under `screenshots/<package-name>/` and reference them with
relative paths, for example:

```json
"screenshots": ["screenshots/mpv/01.png"]
```

Screenshots should be real captures from Termux or Termux X11.
