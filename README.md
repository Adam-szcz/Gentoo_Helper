# Gentoo Helper

An interactive **GTK-based installer GUI** that walks you through a full Gentoo Linux installation—disk partitioning, Stage 3 extraction, chroot setup, kernel build, user creation, boot loader, and optional desktop packages.

> **Status**: beta.  Tested on amd64 with both SystemRescue and the official Gentoo Live‑GUI images.

---

## Table of contents

1. [Why Gentoo Helper?](#why-gentoohelper)
2. [Prerequisites](#prerequisites)
3. [Quick start (live‑USB)](#quick-start-live-usb)
4. [Full installation guide](#full-installation-guide)
5. [Frequently asked questions](#frequently-asked-questions)
6. [Contributing & translation](#contributing--translation)
7. [License](#license)

---

## Why Gentoo Helper?

Manually installing Gentoo is powerful but verbose.  Gentoo Helper aims to provide a *guided, reproducible* path that still leaves the resulting system 100 % Gentoo—no custom binary repos, no wrappers—just a time‑saving wizard.

---

## Prerequisites

| Requirement  | Package (Gentoo)       | Notes                                             |
| ------------ | ---------------------- | ------------------------------------------------- |
| GTK bindings | `dev-python/pygobject` | GUI library                                       |
| Partitioner  | `gparted`              | Optional, launched by wizard                      |
| Text browser | `links`                | Stage 3 download                                  |
| Python 3.11+ | system package         | Wizard engine                                     |
| **Optional** | `genkernel`            | Builds a generic kernel *if* you choose that path |

> **Why genkernel?**  Many newcomers prefer a fast, working kernel before diving into *make menuconfig*.  Gentoo Helper offers both: **Genkernel** for “get me booting now”, or manual kernel configuration for advanced users.

---

## Quick start (live‑USB)

```bash
# 1. Boot any Gentoo‑based live medium with X11.
#    Verify the network works and your clock is correct.

# 2. Fetch the installer
git clone https://github.com/youruser/gentoo-helper.git
cd gentoo-helper

# 3. (optional) Create a virtual env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4. Run the wizard
python3 wizard.py
```

The wizard will: choose a disk, open GParted, download Stage 3, chroot, let you pick a kernel method, create **root** and an ordinary user, install the boot loader and extra packages.

---

## Full installation guide

1. **Select target disk** – lists `/dev/sdX`, `/dev/nvmeXn1`, etc.
2. **Partition**

   * BIOS: 1 × `boot` (ext2), 1 × `swap`, 1 × `root` (ext4/btrfs).
   * UEFI: add a 512 MiB FAT32 EFI partition.
3. **Pick partitions** – point the wizard at your `root` and (if UEFI) `boot`.
4. **Download Stage 3** – wizard opens `links` to choose the latest snapshot.
5. **Enter chroot** – mounts `proc`, `sys`, `dev`, `run` and copies DNS.
6. **Set passwords & users**

   * You *must* enter a **root password**.
   * You *may* create a normal user **<your_username>** (see note below).
7. **Kernel build (current beta)** – the wizard calls `genkernel all` with safe defaults.

   *Manual kernel compilation via `make menuconfig` is **not implemented yet** but is planned for a future release.*

8. **Configure extra packages** – desktop environment, GPU drivers, Steam…
9. **Install boot loader** – GRUB (BIOS/UEFI) or systemd‑boot.
10. **Finish** – unmount, reboot, and enjoy your fresh Gentoo!

---

## Frequently asked questions

### “What is **<your_username> / yourname** in the docs?”

It is a **placeholder** for the *Linux user account you create inside the new Gentoo system*, *not* your GitHub login.  Replace it everywhere with the actual username you typed in step 6 above.  Example:

```bash
useradd -m -G wheel,audio,video yourname   # becomes
useradd -m -G wheel,audio,video adam
```

Home directory ⇒ `/home/adam`.

### “I can’t log in after the first reboot”

1. Use `root` + the password you set in the wizard.
2. Log in as `<your_username>` only *after* you have created that user **inside the wizard**.  This account is brand‑new and unrelated to any external services.

### “Do I have to use genkernel?”

For the moment, **yes**.  The current beta only supports the Genkernel path.  Manual kernel compilation via `make menuconfig` will be added in a future version—it’s on the roadmap.

---

## Contributing & translation

I am still learning Gentoo myself, so **any tips, bug reports or pull requests are welcome and greatly appreciated.**

Pull requests are welcome—bug fixes, UI tweaks, new language files.  Translation templates live under `i18n/`; copy `en.po` to your locale (e.g. `de.po`) and submit a PR.

---

## License

Gentoo Helper is released under the **MIT License**.  See [LICENSE](LICENSE) for details.
