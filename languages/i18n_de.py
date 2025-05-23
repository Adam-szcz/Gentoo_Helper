# i18n_de.py
# ----------
# German messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Gentoo-Assistent"),

    # — Wizard step titles —
    "step_select_disk":   _("Schritt 1 – Laufwerk auswählen"),
    "step_efi":           _("Schritt 2 – EFI verwenden?"),
    "step_partitions":    _("Schritt 3 – Partitionen auswählen"),
    "step_stage3":        _("Schritt 4 – Stage 3 herunterladen oder ins System wechseln"),
    "step_enter_chroot":  _("Schritt 5 – Chroot betreten"),
    "step_root_passwd":   _("Schritt 6 – Root-Passwort festlegen"),
    "step_pkg_helper":    _("Schritt 7 – Paketmanager"),
    "step_install_opts":  _("Schritt 8 – Installationsoptionen"),
    "step_exit":          _("Schritt 9 – Installation abschließen"),

    # — Button labels —
    "btn_select":          _("Auswählen"),
    "btn_yes":             _("Ja"),
    "btn_no":              _("Nein"),
    "btn_back":            _("◀ Zurück"),
    "btn_next":            _("Weiter ▶"),
    "btn_install":         _("Installieren ▶"),
    "btn_parted":          _("Laufwerk partitionieren"),
    "btn_download_stage3": _("Stage 3 herunterladen ▶"),
    "btn_enter_chroot":    _("Ins System eintreten ▶"),
    "btn_packages":        _("Pakete ▶"),
    "btn_terminal":        _("Terminal ▶"),
    "btn_root_passwd":     _("Root-Passwort festlegen ▶"),
    "btn_exit":            _("Beenden"),
    "extracting_text":     _("wird entpackt…"),

    # — Informational texts —
    "info_choose_option": _("Wählen Sie eine der folgenden Optionen:"),
    "info_stage3": _(
        "Ein neues Terminal-Fenster öffnet den Links-Browser.\n"
        "Wählen Sie das Stage 3-Desktop-Profil oder die OpenRC-Datei aus und laden Sie es herunter.\n"
        "Nach dem Schließen des Terminals beginnt die automatische Extraktion."
    ),
    "info_root_passwd": _(
        "Klicken Sie auf die Schaltfläche, und ein neues Terminal führt passwd\n"
        "im Chroot /mnt/gentoo aus.\n"
        "Nach dem Schließen des Terminals geht es weiter."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Kein Terminal-Emulator gefunden.\n"
        "Installieren Sie xterm, gnome-terminal oder konsole."
    ),
    "err_no_stage3":      _("Stage 3 wurde nicht in /mnt/gentoo gefunden."),
    "err_stage3":         _("Laden Sie zuerst Stage 3 herunter und entpacken Sie es."),
    "err_field_required1": _("Das Feld „User“ darf nicht leer sein!"),
    "err_field_required2": _("Das Feld „jobs“ darf nicht leer sein!"),
    "err_field_integer":  _("Das Feld „jobs“ muss eine Ganzzahl sein!"),

    "pkg_sync_text":      _("Python 3 und eix installieren und den Portage-Baum synchronisieren?"),
    "pkg_sync_info": _(
        "Dies ist eine einmalige Operation; bei nachfolgenden Durchläufen startet die Paket-GUI sofort."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Installation abgeschlossen!"),
    "install_done_info": _(
        "Sie können das Installationsprogramm schließen oder\n"
        "weitere Aktionen im installierten System durchführen."
    ),
    "btn_close": _("Schließen"),

    # — Field labels —
    "label_root": _("Root (/):"),
    "label_efi":  _("EFI (/boot):"),

    # — Schritt —
    "step_export_vars": "Umgebungsvariablen exportieren",
    "step_config_makeconf_initial": "Erste Konfiguration von make.conf",
    "step_generate_locales": "Locales generieren",
    "step_eselect_locale": "Locale mit eselect festlegen",
    "step_sync_portage": "Portage synchronisieren",
    "step_update_world": "System aktualisieren (world)",
    "step_config_makeconf_final": "Endgültige Konfiguration von make.conf",
    "step_extra_cflags": "EXTRA_CFLAGS setzen",
    "step_install_kernel": "Kernel installieren",
    "step_microcode": "Microcode konfigurieren",
    "step_link_linux": "Symlink zum Kernel",
    "step_genkernel": "Kernel kompilieren (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "eselect-repository installieren",
    "step_eselect": "Overlays mit eselect hinzufügen",
    "step_sync_overlays": "Overlays synchronisieren",
    "step_update_world2": "System erneut aktualisieren",
    "step_install_programs": "Programme installieren",
    "step_useradd": "Benutzer hinzufügen",
    "step_autostart_x": "X automatisch starten",
    "step_set_desktop_env": "Desktop-Umgebung konfigurieren",
    "step_set_desktop_env_xterm": "Desktop-Umgebung konfigurieren (Xterm)",
    "step_sudoers": "Sudoers konfigurieren",
    "step_history": "Befehlsverlauf konfigurieren",
    "step_dbus": "Dbus zum Autostart hinzufügen",
    "step_networkmanager": "NetworkManager zum Autostart hinzufügen",
    "step_autologin": "Autologin konfigurieren",
    "step_set_user_passwd": "Benutzerpasswort setzen",
    "step_install_grub_uefi": "GRUB installieren (UEFI)",
    "step_install_grub_bios": "GRUB installieren (BIOS)",
    "env_none": "Kein (nur XTerm)",
    "x_desktop": _("Grafische Umgebungen:"),
    "step_grub_time": _("GRUB verstecken"),
    "step_history_chown": _("Berechtigungen setzen"),
    "install_done_hint": _(
    "Du kannst nun die Systemkonfiguration überprüfen.\n"
    "Auf der Zielhardware schaue in die Datei /etc/portage/make.conf\n"
    "und passe MAKEOPTS für deine CPU und andere Optionen an."
    ),
    "err_no_unmounted_partitions": _(
        "Es gibt keine nicht gemountete Partition auf dem ausgewählten Datenträger.\n"
        "Hänge sie aus oder wähle einen anderen Datenträger."
    ),
    "err_partition_mounted": _("Diese Partition ist eingehängt – wählen Sie eine andere."),
    "suffix_mounted": _("(eingehängt)"),
    "info_set_password": _(
        "Ein Terminalfenster wird geöffnet, um das Benutzerpasswort festzulegen.\n"
        "Tipp: Verwenden Sie ein sicheres, eindeutiges Passwort!"
    ),
    "btn_set_password": _("Benutzerpasswort festlegen"),
    "tooltip_partition_help": _("Datenträger partitionieren – Details"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " • 300–400 MB FAT32 – Flags: boot, esp\n"
        " • Rest ext4 – Dateisystem /\n\n"
        "BIOS / MBR (Legacy):\n"
        " • 3 MB (unformatiert) – Flag: bios_grub, grub_bios\n"
        " • Rest ext4 – Dateisystem /"
    ),
}
