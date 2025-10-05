# Purity Suite

Purity Suite is a collection of tools for intelligence and forensics, orchestrated via a simple suite layer.

## Repository structure

- `suite/` – Orchestration layer and configuration
  - `suite/config/ecosystem_config.json` – Defines available tools and their entry commands
  - `suite/cache/` – Runtime cache (ignored by git)
- `intelligence/` – Intelligence-oriented tools
  - `pure-geo/` (Python; requirements.txt)
  - `purity-quest/` (Python; requirements.txt)
  - `pure-face/` (Python; explore to see specifics)
- `forensics/` – Forensics tools
  - `pure-data/`
  - `pure-usb/`
  - `pure-pics/`
- `docs/` – Documentation and additional READMEs

## Prerequisites (Kali/Debian)

- Git
- Python 3.x with venv

Install system packages:

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
```

## Setup (recommended): virtual environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install Python dependencies used by included tools:

```bash
# Intelligence tools
python -m pip install -r intelligence/pure-geo/requirements.txt
python -m pip install -r intelligence/purity-quest/requirements.txt
```

Note: Additional components may have their own requirements or setup scripts. Check their READMEs under each subfolder (for example, `intelligence/purity-quest/README.md`, `intelligence/pure-geo/README.md`).

## Running tools via the suite

The suite defines tool paths and commands in:

- `suite/config/ecosystem_config.json`

Examples (run from repo root after activating the venv when needed):

```bash
# Purity Quest
python intelligence/purity-quest/purity_quest.py

# Pure Geo (shell launcher)
bash intelligence/pure-geo/launch_pure_geo.sh

# Pure Face (if Python entrypoint exists)
python intelligence/pure-face/pure_face.py
```

Adjust commands as needed per each tool’s README and the `ecosystem_config.json` mapping.

## Development

- Create a new virtual environment for development (`.venv/` is git-ignored).
- Add new tool entries to `suite/config/ecosystem_config.json` following the existing structure.

## Contributing

Please open issues and pull requests describing changes. Ensure any new tool documents its own dependencies and provides a simple entrypoint.

## License

Specify your license here (e.g., MIT, Apache-2.0).