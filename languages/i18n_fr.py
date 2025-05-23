# i18n_fr.py
# ----------
# French messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Assistant Gentoo"),

    # — Wizard step titles —
    "step_select_disk":   _("Étape 1 – Sélectionner le disque"),
    "step_efi":           _("Étape 2 – Utiliser EFI ?"),
    "step_partitions":    _("Étape 3 – Sélectionner les partitions"),
    "step_stage3":        _("Étape 4 – Télécharger Stage 3 ou entrer dans le système"),
    "step_enter_chroot":  _("Étape 5 – Entrer dans le chroot"),
    "step_root_passwd":   _("Étape 6 – Définir le mot de passe root"),
    "step_pkg_helper":    _("Étape 7 – Gestionnaire de paquets"),
    "step_install_opts":  _("Étape 8 – Options d'installation"),
    "step_exit":          _("Étape 9 – Terminer l'installation"),

    # — Button labels —
    "btn_select":          _("Sélectionner"),
    "btn_yes":             _("Oui"),
    "btn_no":              _("Non"),
    "btn_back":            _("◀ Retour"),
    "btn_next":            _("Suivant ▶"),
    "btn_install":         _("Installer ▶"),
    "btn_parted":          _("Partitionner le disque"),
    "btn_download_stage3": _("Télécharger Stage 3 ▶"),
    "btn_enter_chroot":    _("Entrer dans le système ▶"),
    "btn_packages":        _("Paquets ▶"),
    "btn_terminal":        _("Terminal ▶"),
    "btn_root_passwd":     _("Définir le mot de passe root ▶"),
    "btn_exit":            _("Quitter"),
    "extracting_text":     _("extraction…"),

    # — Informational texts —
    "info_choose_option": _("Choisissez une des options ci-dessous :"),
    "info_stage3": _(
        "Une nouvelle fenêtre de terminal s'ouvrira avec le navigateur links.\n"
        "Sélectionnez le profil de bureau Stage 3 ou le fichier OpenRC et téléchargez-le.\n"
        "Après la fermeture du terminal, l'extraction automatique commencera."
    ),
    "info_root_passwd": _(
        "Cliquez sur le bouton et un nouveau terminal exécutera passwd\n"
        "à l'intérieur du chroot /mnt/gentoo.\n"
        "Après la fermeture du terminal, vous pourrez continuer."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Aucun émulateur de terminal trouvé.\n"
        "Installez xterm, gnome-terminal ou konsole."
    ),
    "err_no_stage3":      _("Stage 3 introuvable dans /mnt/gentoo."),
    "err_field_required1": _("Le champ « User » ne peut pas être vide !"),
    "err_field_required2": _("Le champ « jobs » ne peut pas être vide !"),
    "err_field_integer":  _("Le champ « jobs » doit être un entier !"),

    "pkg_sync_text":      _("Installer Python 3 et eix et synchroniser l'arbre Portage ?"),
    "pkg_sync_info": _(
        "C'est une opération unique ; lors des exécutions suivantes, l'interface graphique des paquets démarrera immédiatement."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Installation terminée !"),
    "install_done_info": _(
        "Vous pouvez fermer l'installateur ou effectuer des actions supplémentaires\n"
        "dans le système installé."
    ),
    "btn_close": _("Fermer"),

    # — Field labels —
    "label_root": _("Racine (/):"),
    "label_efi":  _("EFI (/boot) :"),

    # — Step —
    "step_export_vars": "Exporter les variables d'environnement",
    "step_config_makeconf_initial": "Configuration initiale de make.conf",
    "step_generate_locales": "Générer les locales",
    "step_eselect_locale": "Définir la locale via eselect",
    "step_sync_portage": "Synchroniser Portage",
    "step_update_world": "Mettre à jour le système (world)",
    "step_config_makeconf_final": "Configuration finale de make.conf",
    "step_extra_cflags": "Définir EXTRA_CFLAGS",
    "step_install_kernel": "Installer le noyau",
    "step_microcode": "Configurer le microcode",
    "step_link_linux": "Lien symbolique vers le noyau",
    "step_genkernel": "Compiler le noyau (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Installer eselect-repository",
    "step_eselect": "Ajouter des overlays via eselect",
    "step_sync_overlays": "Synchroniser les overlays",
    "step_update_world2": "Mettre à jour le système (encore)",
    "step_install_programs": "Installer des programmes",
    "step_useradd": "Ajouter un utilisateur",
    "step_autostart_x": "Démarrage automatique de X",
    "step_set_desktop_env": "Configurer l'environnement de bureau",
    "step_set_desktop_env_xterm": "Configurer l'environnement de bureau (Xterm)",
    "step_sudoers": "Configurer sudoers",
    "step_history": "Configurer l'historique des commandes",
    "step_dbus": "Ajouter dbus au démarrage automatique",
    "step_networkmanager": "Ajouter NetworkManager au démarrage automatique",
    "step_autologin": "Configurer l'ouverture automatique de session",
    "step_set_user_passwd": "Définir le mot de passe de l'utilisateur",
    "step_install_grub_uefi": "Installer GRUB (UEFI)",
    "step_install_grub_bios": "Installer GRUB (BIOS)",
    "env_none": "Aucun (XTerm seulement)",
        "x_desktop": _("Environnements de bureau :"),
    "step_grub_time": _("Masquer GRUB"),
    "step_history_chown": _("Définir les autorisations"),
    "x_desktop": _("Environnements de bureau :"),
    "step_grub_time": _("Masquer GRUB"),
    "step_history_chown": _("Définir les autorisations"),
    # — Final extra hint —
    "install_done_hint": _(
        "Vous pouvez maintenant consulter la configuration du système.\n"
        "Sur le matériel cible, vérifiez le fichier /etc/portage/make.conf\n"
        "et ajustez MAKEOPTS pour votre processeur et d'autres options."
    ),
     "err_no_unmounted_partitions": _(
        "Il n'y a AUCUNE partition DÉMONTÉE sur le disque sélectionné.\n"
        "Démontez-la ou choisissez un autre disque."
    ),
    "err_partition_mounted": _("Cette partition est montée – choisissez une autre."),
    "suffix_mounted": _("(montée)"),
    "info_set_password": _(
        "Une fenêtre de terminal s'ouvrira pour définir le mot de passe de l'utilisateur.\n"
        "Astuce : utilisez un mot de passe fort et unique !"
    ),
    "btn_set_password": _("Définir le mot de passe de l'utilisateur"),

}
