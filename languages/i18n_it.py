# i18n_it.py
# ----------
# Italian messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Assistente Gentoo"),

    # — Wizard step titles —
    "step_select_disk":   _("Passo 1 – Seleziona disco"),
    "step_efi":           _("Passo 2 – Usare EFI?"),
    "step_partitions":    _("Passo 3 – Seleziona partizioni"),
    "step_stage3":        _("Passo 4 – Scarica Stage 3 o entra nel sistema"),
    "step_enter_chroot":  _("Passo 5 – Entra in chroot"),
    "step_root_passwd":   _("Passo 6 – Imposta password root"),
    "step_pkg_helper":    _("Passo 7 – Gestore pacchetti"),
    "step_install_opts":  _("Passo 8 – Opzioni d'installazione"),
    "step_exit":          _("Passo 9 – Completa l'installazione"),

    # — Button labels —
    "btn_select":          _("Seleziona"),
    "btn_yes":             _("Sì"),
    "btn_no":              _("No"),
    "btn_back":            _("◀ Indietro"),
    "btn_next":            _("Avanti ▶"),
    "btn_install":         _("Installa ▶"),
    "btn_parted":          _("Partiziona disco"),
    "btn_download_stage3": _("Scarica Stage 3 ▶"),
    "btn_enter_chroot":    _("Entra nel sistema ▶"),
    "btn_packages":        _("Pacchetti ▶"),
    "btn_terminal":        _("Terminale ▶"),
    "btn_root_passwd":     _("Imposta password root ▶"),
    "btn_exit":            _("Esci"),
    "extracting_text":     _("estrazione…"),

    # — Informational texts —
    "info_choose_option": _("Scegli una delle opzioni seguenti:"),
    "info_stage3": _(
        "Si aprirà una nuova finestra di terminale con il browser links.\n"
        "Seleziona il profilo desktop Stage 3 o il file OpenRC e scaricalo.\n"
        "Dopo la chiusura del terminale l'estrazione inizierà automaticamente."
    ),
    "info_root_passwd": _(
        "Clicca il pulsante e un nuovo terminale eseguirà passwd\n"
        "all'interno del chroot /mnt/gentoo.\n"
        "Dopo la chiusura del terminale potrai continuare."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Nessun emulatore di terminale trovato.\n"
        "Installa xterm, gnome-terminal o konsole."
    ),
    "err_no_stage3":      _("Stage 3 non trovato in /mnt/gentoo."),
    "err_stage3":         _("Scarica ed estrai prima Stage 3."),
    "err_field_required1": _("Il campo 'User' non può essere vuoto!"),
    "err_field_required2": _("Il campo 'jobs' non può essere vuoto!"),
    "err_field_integer":  _("Il campo 'jobs' deve essere un numero intero!"),

    "pkg_sync_text":      _("Installare Python 3 e eix e sincronizzare l'albero di Portage?"),
    "pkg_sync_info": _(
        "Questa è un'operazione una tantum; nelle esecuzioni successive l'interfaccia grafica dei pacchetti si avvierà immediatamente."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Installazione completata!"),
    "install_done_info": _(
        "Puoi chiudere l'installer o eseguire azioni aggiuntive\n"
        "nel sistema installato."
    ),
    "btn_close": _("Chiudi"),

    # — Field labels —
    "label_root": _("Radice (/):"),
    "label_efi":  _("EFI (/boot):"),

    # — Step —
    "step_export_vars": "Esporta variabili d'ambiente",
    "step_config_makeconf_initial": "Configurazione iniziale di make.conf",
    "step_generate_locales": "Genera locali",
    "step_eselect_locale": "Imposta locale tramite eselect",
    "step_sync_portage": "Sincronizza Portage",
    "step_update_world": "Aggiorna sistema (world)",
    "step_config_makeconf_final": "Configurazione finale di make.conf",
    "step_extra_cflags": "Imposta EXTRA_CFLAGS",
    "step_install_kernel": "Installa kernel",
    "step_microcode": "Configura microcode",
    "step_link_linux": "Link simbolico al kernel",
    "step_genkernel": "Compila kernel (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Installa eselect-repository",
    "step_eselect": "Aggiungi overlays con eselect",
    "step_sync_overlays": "Sincronizza overlays",
    "step_update_world2": "Aggiorna sistema (di nuovo)",
    "step_install_programs": "Installa programmi",
    "step_useradd": "Aggiungi utente",
    "step_autostart_x": "Avvio automatico di X",
    "step_set_desktop_env": "Configura ambiente desktop",
    "step_set_desktop_env_xterm": "Configura ambiente desktop (Xterm)",
    "step_sudoers": "Configura sudoers",
    "step_history": "Configura cronologia comandi",
    "step_dbus": "Aggiungi dbus all'avvio automatico",
    "step_networkmanager": "Aggiungi NetworkManager all'avvio automatico",
    "step_autologin": "Configura accesso automatico",
    "step_set_user_passwd": "Imposta password utente",
    "step_install_grub_uefi": "Installa GRUB (UEFI)",
    "step_install_grub_bios": "Installa GRUB (BIOS)",
    "env_none": "Nessuno (solo XTerm)",
        "x_desktop": _("Ambienti grafici:"),
    "step_grub_time": _("Nascondi GRUB"),
    "step_history_chown": _("Imposta i permessi"),
    # — Final extra hint —
    "install_done_hint": _(
        "Ora puoi rivedere la configurazione del sistema.\n"
        "Sul computer di destinazione, controlla il file /etc/portage/make.conf\n"
        "e regola MAKEOPTS per la tua CPU e altre opzioni."
    ),
    "err_no_unmounted_partitions": _(
        "Non ci sono partizioni SMONTATE sul disco selezionato.\n"
        "Smontala o scegli un altro disco."
    ),
    "err_partition_mounted": _("Quella partizione è montata – scegli un'altra."),
    "suffix_mounted": _("(montata)"),
    "info_set_password": _(
        "Apparirà una finestra di terminale per impostare la password dell'utente.\n"
        "Suggerimento: usa una password forte e univoca!"
    ),
    "btn_set_password": _("Imposta la password utente"),
    "missing_package": _("Pacchetto {pkg} non trovato."),
    "install_prompt": _("Vuoi installare il pacchetto {pkg}?"),
    "install_failed": _("Installazione del pacchetto {pkg} non riuscita."),
}
