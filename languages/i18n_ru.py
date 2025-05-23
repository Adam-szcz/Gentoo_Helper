# i18n_ru.py
# ----------
# Russian messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Помощник Gentoo"),

    # — Wizard step titles —
    "step_select_disk":   _("Шаг 1 – Выбор диска"),
    "step_efi":           _("Шаг 2 – Использовать EFI?"),
    "step_partitions":    _("Шаг 3 – Выбор разделов"),
    "step_stage3":        _("Шаг 4 – Загрузить Stage 3 или войти в систему"),
    "step_enter_chroot":  _("Шаг 5 – Войти в chroot"),
    "step_root_passwd":   _("Шаг 6 – Установить пароль root"),
    "step_pkg_helper":    _("Шаг 7 – Диспетчер пакетов"),
    "step_install_opts":  _("Шаг 8 – Параметры установки"),
    "step_exit":          _("Шаг 9 – Завершить установку"),

    # — Button labels —
    "btn_select":          _("Выбрать"),
    "btn_yes":             _("Да"),
    "btn_no":              _("Нет"),
    "btn_back":            _("◀ Назад"),
    "btn_next":            _("Далее ▶"),
    "btn_install":         _("Установить ▶"),
    "btn_parted":          _("Разметить диск"),
    "btn_download_stage3": _("Скачать Stage 3 ▶"),
    "btn_enter_chroot":    _("Войти в систему ▶"),
    "btn_packages":        _("Пакеты ▶"),
    "btn_terminal":        _("Терминал ▶"),
    "btn_root_passwd":     _("Установить пароль root ▶"),
    "btn_exit":            _("Выход"),
    "extracting_text":     _("распаковка…"),

    # — Informational texts —
    "info_choose_option": _("Выберите один из вариантов ниже:"),
    "info_stage3": _(
        "В новом окне терминала откроется браузер links.\n"
        "Выберите профиль рабочего стола stage3 или файл OpenRC и скачайте его.\n"
        "После закрытия терминала начнётся автоматическая распаковка."
    ),
    "info_root_passwd": _(
        "Нажмите кнопку, и в новом терминале будет выполнена команда passwd\n"
        "внутри chroot /mnt/gentoo.\n"
        "После закрытия терминала вы сможете продолжить."
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "Эмулятор терминала не найден.\n"
        "Установите xterm, gnome-terminal или konsole."
    ),
    "err_no_stage3":      _("Stage 3 не найден в /mnt/gentoo."),
    "err_stage3":         _("Сначала скачайте и распакуйте Stage 3."),
    "err_field_required1": _("Поле «User» не может быть пустым!"),
    "err_field_required2": _("Поле «jobs» не может быть пустым!"),
    "err_field_integer":  _("Поле «jobs» должно быть целым числом!"),

    "pkg_sync_text":      _("Установить Python 3 и eix и синхронизировать дерево Portage?"),
    "pkg_sync_info": _(
        "Это операция, выполняемая один раз; при последующих запусках графический интерфейс пакетов запустится сразу же."
    ),

    # — Installation finished —
    "install_done_title": _("✓ Установка завершена!"),
    "install_done_info": _(
        "Вы можете закрыть установщик или выполнить дополнительные действия\n"
        "в установленной системе."
    ),
    "btn_close": _("Закрыть"),

    # — Field labels —
    "label_root": _("Корень (/):"),
    "label_efi":  _("EFI (/boot):"),

    # — Step —
    "step_export_vars": "Экспортировать переменные окружения",
    "step_config_makeconf_initial": "Первоначальная настройка make.conf",
    "step_generate_locales": "Генерация локалей",
    "step_eselect_locale": "Установить локаль через eselect",
    "step_sync_portage": "Синхронизировать Portage",
    "step_update_world": "Обновить систему (world)",
    "step_config_makeconf_final": "Финальная настройка make.conf",
    "step_extra_cflags": "Установить EXTRA_CFLAGS",
    "step_install_kernel": "Установить ядро",
    "step_microcode": "Настроить микрокод",
    "step_link_linux": "Символическая ссылка на ядро",
    "step_genkernel": "Собрать ядро (genkernel)",
    "step_env_update": "Env-update",
    "step_repo": "Установить eselect-repository",
    "step_eselect": "Добавить overlays через eselect",
    "step_sync_overlays": "Синхронизировать overlays",
    "step_update_world2": "Обновить систему (ещё раз)",
    "step_install_programs": "Установить программы",
    "step_useradd": "Добавить пользователя",
    "step_autostart_x": "Автоматически запускать X",
    "step_set_desktop_env": "Настроить графическую среду",
    "step_set_desktop_env_xterm": "Настроить графическую среду (Xterm)",
    "step_sudoers": "Настроить sudoers",
    "step_history": "Настроить историю команд",
    "step_dbus": "Добавить dbus в автозагрузку",
    "step_networkmanager": "Добавить NetworkManager в автозагрузку",
    "step_autologin": "Настроить автологин",
    "step_set_user_passwd": "Установить пароль пользователя",
    "step_install_grub_uefi": "Установить GRUB (UEFI)",
    "step_install_grub_bios": "Установить GRUB (BIOS)",
    "env_none": "Нет (только XTerm)",
        "x_desktop": _("Графические окружения:"),
    "step_grub_time": _("Скрыть GRUB"),
    "step_history_chown": _("Установить права доступа"),
    # — Final extra hint —
    "install_done_hint": _(
        "Теперь вы можете ознакомиться с конфигурацией системы.\n"
        "На целевом устройстве откройте файл /etc/portage/make.conf\n"
        "и настройте MAKEOPTS для вашего процессора и других опций."
    ),
    "err_no_unmounted_partitions": _(
        "На выбранном диске нет НЕСМОНТИРОВАННЫХ разделов.\n"
        "Отмонтируйте один из них или выберите другой диск."
    ),
    "err_partition_mounted": _("Этот раздел смонтирован – выберите другой."),
    "suffix_mounted": _("(смонтирован)"),
    "info_set_password": _(
        "Откроется окно терминала для установки пароля пользователя.\n"
        "Совет: используйте сложный и уникальный пароль!"
    ),
    "btn_set_password": _("Установить пароль пользователя"),
    "tooltip_partition_help": _("Как разметить диск – подробности"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " • 300–400 MB FAT32 — флаги: boot, esp\n"
        " • остальное ext4 — корневая файловая система /\n\n"
        "BIOS / MBR (Legacy):\n"
        " • 3 MB (неформатированный) — флаг: bios_grub, grub_bios\n"
        " • остальное ext4 — корневая файловая система /"
    ),
}
