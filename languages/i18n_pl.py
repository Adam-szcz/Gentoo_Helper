"""
i18n.py
-------
All user-facing messages for Gentoo Helper.
Currently in Polish; ready for future localization.
"""

def _(s):
    # placeholder for gettext.gettext
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Gentoo Helper"),

    # — Wizard step titles —
    "step_select_disk":   _("Krok 1 - Wybierz dysk"),
    "step_efi":           _("Krok 2 - Czy system ma używać EFI?"),
    "step_partitions":    _("Krok 3 - Wybierz partycje"),
    "step_stage3":        _("Krok 4 - Pobierz Stage3 albo wejdź do systemu"),
    "step_enter_chroot":  _("Krok 5 - Wejdź do chroot"),
    "step_root_passwd":   _("Krok 6 - Ustaw hasło roota"),
    "step_pkg_helper":    _("Krok 7 - Menedżer pakietów"),
    "step_install_opts":  _("Krok 8 - Opcje instalacji"),
    "step_exit":          _("Krok 9 - Zakończ instalację"),

    # — Button labels —
    "btn_select":         _("Wybierz"),
    "btn_yes":            _("Tak"),
    "btn_no":             _("Nie"),
    "btn_back":           _("◀ Wstecz"),
    "btn_next":           _("Dalej ▶"),
    "btn_install":        _("Instaluj ▶"),
    "btn_parted":         _("Spartycjonuj dysk"),
    "btn_download_stage3":_("Pobierz Stage 3 ▶"),
    "btn_enter_chroot":   _("Wejdź do systemu ▶"),
    "btn_packages":       _("Pakiety ▶"),
    "btn_terminal":       _("Terminal ▶"),
    "btn_root_passwd":    _("Ustaw hasło roota ▶"),
    "btn_exit":           _("Zakończ"),
    "extracting_text":    _("rozpakowuję..."),
    # — Informational texts —
    "info_choose_option": _("Wybierz jedną z opcji poniżej:"),
    "info_stage3": _(
        "W nowym oknie terminala otworzy się przeglądarka links.\n"
        "Wskaż plik stage3 desktop profile | openrc i pobierz go.\n"
        "Po zamknięciu terminala rozpocznie się automatyczne rozpakowanie."
    ),
    "info_root_passwd": _(
        "Kliknij przycisk, a w nowym terminalu zostanie uruchomione\n"
        "passwd w chroocie /mnt/gentoo.\n"
        "Po zamknięciu terminala przejdziesz dalej."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Brak emulatora terminala.\n"
        "Zainstaluj xterm, gnome-terminal lub konsole."
    ),
    "err_no_stage3":      _("Nie znalazłem stage3 w /mnt/gentoo."),
    "err_stage3":         _("Najpierw pobierz i rozpakuj Stage3."),
    "err_field_required1": _("Pole „User” nie może być puste!"),
    "err_field_required2": _("Pole „jobs” nie może być puste!"),
    "err_field_integer":  _("Pole „jobs” musi być liczbą całkowitą!"),

    "pkg_sync_text":      _("Zainstalować Python3 i eix oraz zsynchronizować drzewo Portage?"),
    "pkg_sync_info": _(
        "To operacja jednorazowa; przy kolejnych uruchomieniach od razu\n"
        "uruchomi się GUI menedżera pakietów."
    ),
    # ── Instalacja zakończona ──────────────────────────
    "install_done_title": _("✓ Instalacja zakończona!"),
    "install_done_info": _(
        "Możesz zamknąć instalator lub wykonać dodatkowe czynności\n"
        "w zainstalowanym systemie."
    ),
    "btn_close": _("Zamknij"),
    # — Field labels —
    "label_root":         _("Root (/):"),
    "label_efi":          _("EFI (/boot):"),

    # — Step —
    "step_export_vars": _("Eksport zmiennych środowiskowych"),
    "step_config_makeconf_initial": _("Konfiguracja pliku make.conf (wstępna)"),
    "step_generate_locales": _("Generowanie locale"),
    "step_eselect_locale": _("Ustawienie locale przez eselect"),
    "step_sync_portage": _("Synchronizacja Portage"),
    "step_update_world": _("Aktualizacja systemu (world)"),
    "step_config_makeconf_final": _("Konfiguracja pliku make.conf (ostateczna)"),
    "step_extra_cflags": _("Ustawienie EXTRA_CFLAGS"),
    "step_install_kernel": _("Instalacja kernela"),
    "step_microcode": _("Konfiguracja microcode"),
    "step_link_linux": _("Link symboliczny do kernela"),
    "step_genkernel": _("Budowanie kernela (genkernel)"),
    "step_env_update": _("Env-update"),
    "step_repo": _("Instalacja eselect-repository"),
    "step_eselect": _("Dodanie overlayów przez eselect"),
    "step_sync_overlays": _("Synchronizacja overlayów"),
    "step_update_world2": _("Aktualizacja systemu (ponownie)"),
    "step_install_programs": _("Instalacja programów"),
    "step_useradd": _("Dodanie użytkownika"),
    "step_autostart_x": _("Automatyczny start X"),
    "step_set_desktop_env": _("Konfiguracja środowiska graficznego"),
    "step_set_desktop_env_xterm": _("Konfiguracja środowiska graficznego (Xterm)"),
    "step_sudoers": _("Konfiguracja sudoers"),
    "step_history": _("Konfiguracja historii poleceń"),
    "step_dbus": _("Dodanie dbus do autostartu"),
    "step_networkmanager": _("Dodanie NetworkManager do autostartu"),
    "step_autologin": _("Konfiguracja autologowania"),
    "step_set_user_passwd": _("Ustawienie hasła użytkownika"),
    "step_install_grub_uefi": _("Instalacja GRUB (UEFI)"),
    "step_install_grub_bios": _("Instalacja GRUB (BIOS)"),
    "env_none": _("Brak (tylko XTerm)"),
    "x_desktop": _("Środowiski graficzne:"),
    "step_grub_time": _("Schowanie gruba"),
    "step_history_chown": _("Nadanie uprawnień"),
        # — Final extra hint —
    "install_done_hint": _(
        "Teraz możesz zapoznać się z konfiguracją systemu.\n"
        "Na docelowym sprzęcie zajrzyj do pliku /etc/portage/make.conf\n"
        "i dostosuj MAKEOPTS do swojego procesora oraz inne opcje."
    ),
    "err_no_unmounted_partitions": _(
        "Na wybranym dysku nie ma NIEZAMONTOWANEJ partycji.\n"
        "Odmontuj ją lub wybierz inny dysk."
    ),
    "err_partition_mounted": _("Ta partycja jest zamontowana – wybierz inną."),
    "suffix_mounted": _("(zamontowana)"),
    "info_set_password": _(
        "Pojawi się okno terminala, aby ustawić hasło użytkownika.\n"
        "Wskazówka: użyj silnego, unikalnego hasła!"
    ),
    "btn_set_password": _("Ustaw hasło użytkownika"),
    "tooltip_partition_help": _("Jak podzielić dysk – szczegóły"),
    "info_partition_help": _(
                "  UEFI (GPT):\n"
                "  • 300 – 400 MB FAT32      –  flagi:  boot, esp\n"
                "  • reszta  ext4                   –  system plików /\n\n"
                "  BIOS / MBR (Legacy):\n"
                "  • 3 MB  (nieformatowana)  –  flaga: bios_grub, grub_bios\n"
                "  • reszta  ext4                   –  system plików /"
    ), 
    "missing_package": _("Nie znaleziono pakietu {pkg}."),
    "install_prompt": _("Czy chcesz zainstalować pakiet {pkg}?"),
    "install_failed": _("Instalacja pakietu {pkg} nie powiodła się."),                              
}
