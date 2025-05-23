# i18n_pt.py
# ----------
# Portuguese (Brazilian) messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Assistente Gentoo"),

    # — Wizard step titles —
    "step_select_disk":   _("Etapa 1 – Selecionar disco"),
    "step_efi":           _("Etapa 2 – Usar EFI?"),
    "step_partitions":    _("Etapa 3 – Selecionar partições"),
    "step_stage3":        _("Etapa 4 – Baixar o Stage 3 ou entrar no sistema"),
    "step_enter_chroot":  _("Etapa 5 – Entrar no chroot"),
    "step_root_passwd":   _("Etapa 6 – Definir senha root"),
    "step_pkg_helper":    _("Etapa 7 – Gerenciador de pacotes"),
    "step_install_opts":  _("Etapa 8 – Opções de instalação"),
    "step_exit":          _("Etapa 9 – Finalizar instalação"),

    # — Button labels —
    "btn_select":          _("Selecionar"),
    "btn_yes":             _("Sim"),
    "btn_no":              _("Não"),
    "btn_back":            _("◀ Voltar"),
    "btn_next":            _("Próximo ▶"),
    "btn_install":         _("Instalar ▶"),
    "btn_parted":          _("Particionar disco"),
    "btn_download_stage3": _("Baixar Stage 3 ▶"),
    "btn_enter_chroot":    _("Entrar no sistema ▶"),
    "btn_packages":        _("Pacotes ▶"),
    "btn_terminal":        _("Terminal ▶"),
    "btn_root_passwd":     _("Definir senha root ▶"),
    "btn_exit":            _("Sair"),
    "extracting_text":     _("extraindo…"),

    # — Informational texts —
    "info_choose_option": _("Escolha uma das opções abaixo:"),
    "info_stage3": _(
        "Uma nova janela de terminal abrirá o navegador links.\n"
        "Selecione o perfil de desktop Stage 3 ou o arquivo OpenRC e faça o download.\n"
        "Após fechar o terminal, a extração automática começará."
    ),
    "info_root_passwd": _(
        "Clique no botão e um novo terminal executará passwd\n"
        "dentro do chroot /mnt/gentoo.\n"
        "Após fechar o terminal, você poderá continuar."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Nenhum emulador de terminal encontrado.\n"
        "Instale xterm, gnome-terminal ou konsole."
    ),
    "err_no_stage3":      _("Stage 3 não encontrado em /mnt/gentoo."),
    "err_stage3":         _("Baixe e extraia o Stage 3 primeiro."),
    "err_field_required1": _("O campo 'User' não pode estar vazio!"),
    "err_field_required2": _("O campo 'jobs' não pode estar vazio!"),
    "err_field_integer":  _("O campo 'jobs' deve ser um número inteiro!"),

    "pkg_sync_text":      _("Instalar Python 3 e eix e sincronizar a árvore Portage?"),
    "pkg_sync_info": _(
        "Esta é uma operação única; em execuções subsequentes a interface gráfica de pacotes iniciará imediatamente."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Instalação concluída!"),
    "install_done_info": _(
        "Você pode fechar o instalador ou realizar ações adicionais\n"
        "no sistema instalado."
    ),
    "btn_close": _("Fechar"),

    # — Field labels —
    "label_root": _("Raiz (/):"),
    "label_efi":  _("EFI (/boot):"),

    # — Step —
    "step_export_vars": "Exportar variáveis de ambiente",
    "step_config_makeconf_initial": "Configuração inicial do make.conf",
    "step_generate_locales": "Gerar locales",
    "step_eselect_locale": "Definir locale via eselect",
    "step_sync_portage": "Sincronizar Portage",
    "step_update_world": "Atualizar o sistema (world)",
    "step_config_makeconf_final": "Configuração final do make.conf",
    "step_extra_cflags": "Definir EXTRA_CFLAGS",
    "step_install_kernel": "Instalar kernel",
    "step_microcode": "Configurar microcode",
    "step_link_linux": "Link simbólico para o kernel",
    "step_genkernel": "Compilar kernel (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Instalar eselect-repository",
    "step_eselect": "Adicionar overlays via eselect",
    "step_sync_overlays": "Sincronizar overlays",
    "step_update_world2": "Atualizar o sistema (novamente)",
    "step_install_programs": "Instalar programas",
    "step_useradd": "Adicionar usuário",
    "step_autostart_x": "Iniciar X automaticamente",
    "step_set_desktop_env": "Configurar ambiente de desktop",
    "step_set_desktop_env_xterm": "Configurar ambiente de desktop (Xterm)",
    "step_sudoers": "Configurar sudoers",
    "step_history": "Configurar histórico de comandos",
    "step_dbus": "Adicionar dbus à inicialização automática",
    "step_networkmanager": "Adicionar NetworkManager à inicialização automática",
    "step_autologin": "Configurar login automático",
    "step_set_user_passwd": "Definir senha do usuário",
    "step_install_grub_uefi": "Instalar GRUB (UEFI)",
    "step_install_grub_bios": "Instalar GRUB (BIOS)",
    "env_none": "Nenhum (somente XTerm)",
        "x_desktop": _("Ambientes gráficos:"),
    "step_grub_time": _("Ocultar o GRUB"),
    "step_history_chown": _("Definir permissões"),
    # — Final extra hint —
    "install_done_hint": _(
        "Agora você pode revisar a configuração do sistema.\n"
        "No hardware de destino, verifique o arquivo /etc/portage/make.conf\n"
        "e ajuste o MAKEOPTS para seu processador e outras opções."
    ),
    "err_no_unmounted_partitions": _(
        "Não há partições DESMONTADAS no disco selecionado.\n"
        "Desmonte-a ou escolha outro disco."
    ),
    "err_partition_mounted": _("Essa partição está montada – escolha outra."),
    "suffix_mounted": _("(montada)"),
    "info_set_password": _(
        "Uma janela de terminal aparecerá para definir a senha do usuário.\n"
        "Dica: Use uma senha forte e única!"
    ),
    "btn_set_password": _("Definir senha do usuário"),
    "tooltip_partition_help": _("Como particionar o disco – detalhes"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " • 300–400 MB FAT32 — flags: boot, esp\n"
        " • restante do disco ext4 — sistema de arquivos /\n\n"
        "BIOS / MBR (Legado):\n"
        " • 3 MB (não formatado) — flag: bios_grub, grub_bios\n"
        " • restante do disco ext4 — sistema de arquivos /"
    ),

}
