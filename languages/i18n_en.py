"""
i18n_en.py
----------
English messages for Gentoo Helper.
"""

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Gentoo Helper"),

    # — Wizard step titles —
    "step_select_disk":   _("Step 1 – Select disk"),
    "step_efi":           _("Step 2 – Use EFI?"),
    "step_partitions":    _("Step 3 – Select partitions"),
    "step_stage3":        _("Step 4 – Download Stage 3 or enter system"),
    "step_enter_chroot":  _("Step 5 – Enter chroot"),
    "step_root_passwd":   _("Step 6 – Set root password"),
    "step_pkg_helper":    _("Step 7 – Package manager"),
    "step_install_opts":  _("Step 8 – Installation options"),
    "step_exit":          _("Step 9 – Finish installation"),

    # — Button labels —
    "btn_select":          _("Select"),
    "btn_yes":             _("Yes"),
    "btn_no":              _("No"),
    "btn_back":            _("◀ Back"),
    "btn_next":            _("Next ▶"),
    "btn_install":         _("Install ▶"),
    "btn_parted":          _("Partition disk"),
    "btn_download_stage3": _("Download Stage 3 ▶"),
    "btn_enter_chroot":    _("Enter system ▶"),
    "btn_packages":        _("Packages ▶"),
    "btn_terminal":        _("Terminal ▶"),
    "btn_root_passwd":     _("Set root password ▶"),
    "btn_exit":            _("Exit"),
    "extracting_text":     _("extracting…"),

    # — Informational texts —
    "info_choose_option": _("Choose one of the options below:"),
    "info_stage3": _(
        "A new terminal window will open the links browser.\n"
        "Select the stage3 desktop profile | openrc file and download it.\n"
        "After closing the terminal, automatic extraction will start."
    ),
    "info_root_passwd": _(
        "Click the button and a new terminal will run passwd\n"
        "inside the /mnt/gentoo chroot.\n"
        "After closing the terminal you will proceed further."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "No terminal emulator found.\n"
        "Install xterm, gnome-terminal or konsole."
    ),
    "err_no_stage3":      _("Stage 3 not found in /mnt/gentoo."),
    "err_stage3":         _("First download and extract Stage 3."),
    "err_field_required1": _("The 'User' field cannot be empty!"),
    "err_field_required2": _("The 'jobs' field cannot be empty!"),
    "err_field_integer":  _("The 'jobs' field must be an integer!"),

    "pkg_sync_text":      _("Install Python 3 and eix and sync the Portage tree?"),
    "pkg_sync_info": _(
        "This is a one-time operation; on subsequent runs the package GUI will start immediately."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Installation completed!"),
    "install_done_info": _(
        "You can close the installer or perform additional actions\n"
        "in the installed system."
    ),
    "btn_close": _("Close"),

    # — Field labels —
    "label_root": _("Root (/):"),
    "label_efi":  _("EFI (/boot):"),

    # — Step —
    "step_export_vars": "Export environment variables",
    "step_config_makeconf_initial": "Initial make.conf configuration",
    "step_generate_locales": "Generate locales",
    "step_eselect_locale": "Set locale via eselect",
    "step_sync_portage": "Sync Portage",
    "step_update_world": "Update system (world)",
    "step_config_makeconf_final": "Final make.conf configuration",
    "step_extra_cflags": "Set EXTRA_CFLAGS",
    "step_install_kernel": "Install kernel",
    "step_microcode": "Configure microcode",
    "step_link_linux": "Symlink to kernel",
    "step_genkernel": "Build kernel (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Install eselect-repository",
    "step_eselect": "Add overlays via eselect",
    "step_sync_overlays": "Sync overlays",
    "step_update_world2": "Update system (again)",
    "step_install_programs": "Install programs",
    "step_useradd": "Add user",
    "step_autostart_x": "Autostart X",
    "step_set_desktop_env": "Configure desktop environment",
    "step_set_desktop_env_xterm": "Configure desktop environment (Xterm)",
    "step_sudoers": "Configure sudoers",
    "step_history": "Configure command history",
    "step_dbus": "Add dbus to autostart",
    "step_networkmanager": "Add NetworkManager to autostart",
    "step_autologin": "Configure autologin",
    "step_set_user_passwd": "Set user password",
    "step_install_grub_uefi": "Install GRUB (UEFI)",
    "step_install_grub_bios": "Install GRUB (BIOS)",
    "env_none": "None (XTerm only)",
    "x_desktop": _("Desktop environments:"),
    "step_grub_time": _("Hide GRUB"),
    "step_history_chown": _("Set permissions"),
    "install_done_hint": _(
    "You can now review the system configuration.\n"
    "On your target hardware, check the /etc/portage/make.conf file\n"
    "and adjust MAKEOPTS for your CPU and other options."
    ),
    "err_no_unmounted_partitions": _(
        "There are no UNMOUNTED partitions on the selected disk.\n"
        "Unmount it or choose another disk."
    ),
    "err_partition_mounted": _("That partition is mounted – choose another."),
    "suffix_mounted": _("(mounted)"),
    "info_set_password": _(
        "A terminal window will appear to set the user's password.\n"
        "Tip: Use a strong, unique password!"
    ),
    "btn_set_password": _("Set user password"),
    "tooltip_partition_help": _("How to partition the disk – details"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " • 300–400 MB FAT32 — flags: boot, esp\n"
        " • rest of disk ext4 — root filesystem /\n\n"
        "BIOS / MBR (Legacy):\n"
        " • 3 MB (unformatted) — flag: bios_grub, grub_bios\n"
        " • rest of disk ext4 — root filesystem /"
    ),

}
