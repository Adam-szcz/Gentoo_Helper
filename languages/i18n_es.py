"""
i18n_es.py
----------
Mensajes en español para Gentoo Helper.
"""

def _(s):
    return s

MESSAGES = {
    # — Aplicación —
    "app_title": _("Gentoo Helper"),

    # — Títulos de pasos —
    "step_select_disk":   _("Paso 1 – Seleccionar disco"),
    "step_efi":           _("Paso 2 – ¿Usar EFI?"),
    "step_partitions":    _("Paso 3 – Seleccionar particiones"),
    "step_stage3":        _("Paso 4 – Descargar Stage 3 o entrar al sistema"),
    "step_enter_chroot":  _("Paso 5 – Entrar al chroot"),
    "step_root_passwd":   _("Paso 6 – Definir contraseña de root"),
    "step_pkg_helper":    _("Paso 7 – Gestor de paquetes"),
    "step_install_opts":  _("Paso 8 – Opciones de instalación"),
    "step_exit":          _("Paso 9 – Finalizar la instalación"),

    # — Botones —
    "btn_select":          _("Seleccionar"),
    "btn_yes":             _("Sí"),
    "btn_no":              _("No"),
    "btn_back":            _("◀ Atrás"),
    "btn_next":            _("Siguiente ▶"),
    "btn_install":         _("Instalar ▶"),
    "btn_parted":          _("Particionar disco"),
    "btn_download_stage3": _("Descargar Stage 3 ▶"),
    "btn_enter_chroot":    _("Entrar al sistema ▶"),
    "btn_packages":        _("Paquetes ▶"),
    "btn_terminal":        _("Terminal ▶"),
    "btn_root_passwd":     _("Definir contraseña de root ▶"),
    "btn_exit":            _("Salir"),
    "extracting_text":     _("extrayendo…"),

    # — Textos informativos —
    "info_choose_option": _("Elige una de las siguientes opciones:"),
    "info_stage3": _(
        "En una nueva ventana de terminal se abrirá el navegador links.\n"
        "Elige el archivo stage3 perfil desktop | openrc y descárgalo.\n"
        "Tras cerrar la terminal comenzará la extracción automática."
    ),
    "info_root_passwd": _(
        "Haz clic en el botón y en una nueva terminal se ejecutará\n"
        "passwd dentro del chroot /mnt/gentoo.\n"
        "Después de cerrar la terminal seguirás al siguiente paso."
    ),

    # — Errores y diálogos —
    "err_no_terminal": _(
        "No se encontró ningún emulador de terminal.\n"
        "Instala xterm, gnome-terminal o konsole."
    ),
    "err_no_stage3":      _("No se encontró Stage 3 en /mnt/gentoo."),
    "err_stage3":         _("Primero descarga y extrae Stage 3."),
    "err_field_required1": _("¡El campo 'User' no puede estar vacío!"),
    "err_field_required2": _("¡El campo 'jobs' no puede estar vacío!"),
    "err_field_integer":  _("¡El campo 'jobs' debe ser un número entero!"),

    "pkg_sync_text":      _("¿Instalar Python 3 y eix y sincronizar el árbol de Portage?"),
    "pkg_sync_info": _(
        "Esta operación se realiza una sola vez; en futuras ejecuciones se abrirá directamente la GUI del gestor de paquetes."
    ),

    # — Instalación finalizada —
    "install_done_title": _("✓ ¡Instalación completada!"),
    "install_done_info": _(
        "Puedes cerrar el instalador o realizar acciones adicionales\n"
        "en el sistema instalado."
    ),
    "btn_close": _("Cerrar"),

    # — Etiquetas de campos —
    "label_root": _("Raíz (/):"),
    "label_efi":  _("EFI (/boot):"),
    # — Paso —
    "step_export_vars": "Exportar variables de entorno",
    "step_config_makeconf_initial": "Configuración inicial de make.conf",
    "step_generate_locales": "Generar locales",
    "step_eselect_locale": "Configurar el locale con eselect",
    "step_sync_portage": "Sincronizar Portage",
    "step_update_world": "Actualizar el sistema (world)",
    "step_config_makeconf_final": "Configuración final de make.conf",
    "step_extra_cflags": "Establecer EXTRA_CFLAGS",
    "step_install_kernel": "Instalar el kernel",
    "step_microcode": "Configurar microcódigo",
    "step_link_linux": "Enlace simbólico al kernel",
    "step_genkernel": "Compilar kernel (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Instalar eselect-repository",
    "step_eselect": "Agregar overlays con eselect",
    "step_sync_overlays": "Sincronizar overlays",
    "step_update_world2": "Actualizar el sistema (otra vez)",
    "step_install_programs": "Instalar programas",
    "step_useradd": "Agregar usuario",
    "step_autostart_x": "Autoiniciar X",
    "step_set_desktop_env": "Configurar entorno de escritorio",
    "step_set_desktop_env_xterm": "Configurar entorno de escritorio (Xterm)",
    "step_sudoers": "Configurar sudoers",
    "step_history": "Configurar historial de comandos",
    "step_dbus": "Agregar dbus al inicio automático",
    "step_networkmanager": "Agregar NetworkManager al inicio automático",
    "step_autologin": "Configurar inicio de sesión automático",
    "step_set_user_passwd": "Establecer contraseña del usuario",
    "step_install_grub_uefi": "Instalar GRUB (UEFI)",
    "step_install_grub_bios": "Instalar GRUB (BIOS)",
    "env_none": "Ninguno (solo XTerm)",
    "x_desktop": _("Entornos gráficos:"),
    "step_grub_time": _("Ocultar GRUB"),
    "step_history_chown": _("Asignar permisos"),
    "install_done_hint": _(
    "Ahora puedes revisar la configuración del sistema.\n"
    "En el hardware de destino, revisa el archivo /etc/portage/make.conf\n"
    "y ajusta MAKEOPTS para tu CPU y otras opciones."
    ),
    "err_no_unmounted_partitions": _(
        "No hay particiones DESMONTADAS en el disco seleccionado.\n"
        "Desmóntala o elige otro disco."
    ),
    "err_partition_mounted": _("Esa partición está montada – elige otra."),
    "suffix_mounted": _("(montada)"),
    "info_set_password": _(
        "Se abrirá una ventana de terminal para establecer la contraseña del usuario.\n"
        "Consejo: ¡Usa una contraseña fuerte y única!"
    ),
    "btn_set_password": _("Establecer contraseña de usuario"),
    "tooltip_partition_help": _("Cómo particionar el disco – detalles"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " • 300–400 MB FAT32 — flags: boot, esp\n"
        " • resto del disco ext4 — sistema de archivos /\n\n"
        "BIOS / MBR (Legacy):\n"
        " • 3 MB (sin formatear) — flag: bios_grub, grub_bios\n"
        " • resto del disco ext4 — sistema de archivos /"
    ),
    "missing_package": _("Paquete {pkg} no encontrado."),
    "install_prompt": _("¿Desea instalar el paquete {pkg}?"),
    "install_failed": _("La instalación del paquete {pkg} ha fallado."),
}
