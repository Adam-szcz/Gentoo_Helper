# Gentoo Helper

An interactive GTK-based installer GUI for Gentoo Linux.
Guides you step-by-step through partitioning, Stage3 download & extraction, chroot setup, package manager, and full system installation.

---

## Features

- **Disk Selection & Partitioning**
  Scan and choose target disk, launch GParted for manual partitioning.
- **EFI / BIOS Detection**
  Optionally configure UEFI (`/boot`) or legacy BIOS.
- **Partition Picker**
  Select root (`/`) and EFI (`/boot`) partitions from the chosen disk.
- **Stage3 Download & Extraction**
  Opens Links browser to fetch a Stage3 archive, then auto-extracts it under `/mnt/gentoo`.
- **Chroot Entry & Root Password**
  Bind-mounts `/proc`, `/sys`, `/dev`, `/run`, copies DNS, then runs `passwd` in chroot.
- **Package Manager GUI**
  Syncs Portage, installs Python3 & eix once, then launches a simple GUI helper under chroot.
- **Installation Options**
  Configure new user, CPU flags (`march`/`mtune`), cores, GPU drivers, and extra packages before final install.
- **Automated Installation Script**
  Background thread runs a data-driven sequence of commands (make.conf, world update, kernel, grub, user setup, etc.) with live log output.

---

## Prerequisites
| Live environment | Packages | Komenda (Gentoo) |
|------------------|----------|------------------|
| **GTK bindings** | `dev-python/pygobject` | `sudo emerge -av pygobject` |
| **Partitioner**  | `gparted` | `sudo emerge -av gparted` |
| **Text browser** | `links`   | `sudo emerge -av links` |
| **Python deps**  | `pip`, `venv` <sup>†</sup> | `pip install -r requirements.txt` |

<sup>†</sup> Projekt działa także w systemowym Pythonie; wirtualne środowisko jest opcjonalne, ale zalecane.

---

## Installation 🚀
```bash
# 1. Pobierz repozytorium
git clone https://github.com/youruser/gentoo-helper.git
cd gentoo-helper

# 2. (opcjonalnie) utwórz venv
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Uruchom kreator
python3 wizard.py
---

## Supported languages

- Polish (pl)
- English (en)
- Other languages (German, French, Spanish, etc.) – in progress!
  *See `i18n` directory and help us translate!*

---

## Quick Start

1. Boot into a Gentoo live environment with X11 and GTK.
2. Clone & run this tool.
3. Follow the guided wizard – disk, partitions, Stage3, chroot, user & packages, install.

---

## Contributing

Contributions and translations are very welcome!
Please open a pull request or issue if you have suggestions, improvements, or want to add a new language.

---

## License

MIT License
See `LICENSE` file for details.

---

## Screenshots

*(You can add screenshots here to show how the wizard looks!)*

---

## Notes

- You can open a terminal at any time during the installation for manual commands.
- After install, review your `/etc/portage/make.conf`, especially `MAKEOPTS` and language settings.
- For additional tips, see the wiki or Issues section.

---

MIT License – see [LICENSE](LICENSE) for details.

## Opis po polsku

Gentoo Helper to graficzny kreator instalacji Gentoo Linux w środowisku GTK.
Przeprowadza krok po kroku przez partycjonowanie, pobieranie Stage3, chroot, konfigurację i pełną instalację systemu.

**Polskie tłumaczenie i wsparcie – zapraszamy do współpracy!**

---
# Gentoo Helper Installer

A graphical installer and package manager GUI for Gentoo Linux.
Supports full step-by-step installation (disk, EFI, Stage3, users, kernel, packages) and interactive package management in a running system.

## Features
- Guided disk partitioning and EFI/BIOS support
- Automatic download and extraction of Stage3
- Chroot environment setup
- User and kernel configuration
- Easy graphical package selection (GParted, Firefox, Steam, etc.)
- Multi-language interface

## Usage
- Run `wizard.py` for the full graphical installer.
- Run `main.py` to launch the package manager GUI in an existing Gentoo system.

## Post-installation Tips
After installation, review `/etc/portage/make.conf` and tune settings for your hardware.

## Languages
Polish, English, German, French, Spanish, Italian, Portuguese, Russian, Chinese, Japanese.

## License
MIT License (add LICENSE file if not present).

## Support
Please use GitHub Issues for questions and bug reports.

