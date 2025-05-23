# i18n_zh.py
# ----------
# Chinese (Simplified) messages for Gentoo Helper.

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Gentoo 辅助程序"),

    # — Wizard step titles —
    "step_select_disk":   _("第1步 – 选择磁盘"),
    "step_efi":           _("第2步 – 使用 EFI？"),
    "step_partitions":    _("第3步 – 选择分区"),
    "step_stage3":        _("第4步 – 下载 Stage 3 或进入系统"),
    "step_enter_chroot":  _("第5步 – 进入 chroot"),
    "step_root_passwd":   _("第6步 – 设置 root 密码"),
    "step_pkg_helper":    _("第7步 – 软件包管理"),
    "step_install_opts":  _("第8步 – 安装选项"),
    "step_exit":          _("第9步 – 完成安装"),

    # — Button labels —
    "btn_select":          _("选择"),
    "btn_yes":             _("是"),
    "btn_no":              _("否"),
    "btn_back":            _("◀ 返回"),
    "btn_next":            _("下一步 ▶"),
    "btn_install":         _("开始安装 ▶"),
    "btn_parted":          _("分区磁盘"),
    "btn_download_stage3": _("下载 Stage 3 ▶"),
    "btn_enter_chroot":    _("进入系统 ▶"),
    "btn_packages":        _("软件包 ▶"),
    "btn_terminal":        _("终端 ▶"),
    "btn_root_passwd":     _("设置 root 密码 ▶"),
    "btn_exit":            _("退出"),
    "extracting_text":     _("正在解压…"),

    # — Informational texts —
    "info_choose_option": _("请选择以下选项："),
    "info_stage3": _(
        "将弹出一个终端窗口并启动 links 浏览器。\n"
        "选择 Stage 3 桌面配置文件或 OpenRC 文件并下载。\n"
        "关闭终端后将自动开始解压。"
    ),
    "info_root_passwd": _(
        "点击按钮后，会打开一个新终端并在\n"
        "chroot /mnt/gentoo 中执行 passwd 命令。\n"
        "关闭终端后即可继续。"
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "未找到终端模拟器。\n"
        "请安装 xterm、gnome-terminal 或 konsole。"
    ),
    "err_no_stage3":      _("在 /mnt/gentoo 中未找到 Stage 3。"),
    "err_stage3":         _("请先下载并解压 Stage 3。"),
    "err_field_required1": _("“User” 字段不能为空！"),
    "err_field_required2": _("“jobs” 字段不能为空！"),
    "err_field_integer":  _("“jobs” 字段必须是整数！"),

    "pkg_sync_text":      _("安装 Python 3 和 eix 并同步 Portage 树？"),
    "pkg_sync_info": _(
        "这是一次性操作；后续运行时，软件包 GUI 将直接启动。"
    ),

    # — Installation finished —
    "install_done_title": _("✓ 安装完成！"),
    "install_done_info": _(
        "您可以关闭安装程序，或在已安装系统中\n"
        "执行其他操作。"
    ),
    "btn_close": _("关闭"),

    # — Field labels —
    "label_root": _("根目录 (/):"),
    "label_efi":  _("EFI (/boot)："),

    # — Step —
    "step_export_vars": "导出环境变量",
    "step_config_makeconf_initial": "初始 make.conf 配置",
    "step_generate_locales": "生成本地化(locale)",
    "step_eselect_locale": "通过 eselect 设置语言环境",
    "step_sync_portage": "同步 Portage",
    "step_update_world": "更新系统（world）",
    "step_config_makeconf_final": "最终 make.conf 配置",
    "step_extra_cflags": "设置 EXTRA_CFLAGS",
    "step_install_kernel": "安装内核",
    "step_microcode": "配置微码",
    "step_link_linux": "创建到内核的符号链接",
    "step_genkernel": "构建内核（genkernel）",
    "step_env_update": "Env-update",
    "step_repo": "安装 eselect-repository",
    "step_eselect": "通过 eselect 添加 overlays",
    "step_sync_overlays": "同步 overlays",
    "step_update_world2": "再次更新系统",
    "step_install_programs": "安装程序",
    "step_useradd": "添加用户",
    "step_autostart_x": "自动启动 X",
    "step_set_desktop_env": "配置桌面环境",
    "step_set_desktop_env_xterm": "配置桌面环境（Xterm）",
    "step_sudoers": "配置 sudoers",
    "step_history": "配置命令历史",
    "step_dbus": "将 dbus 添加到自动启动",
    "step_networkmanager": "将 NetworkManager 添加到自动启动",
    "step_autologin": "配置自动登录",
    "step_set_user_passwd": "设置用户密码",
    "step_install_grub_uefi": "安装 GRUB（UEFI）",
    "step_install_grub_bios": "安装 GRUB（BIOS）",
    "env_none": "无（仅限 XTerm）",
        "x_desktop": _("桌面环境："),
    "step_grub_time": _("隐藏 GRUB"),
    "step_history_chown": _("设置权限"),
    # — Final extra hint —
    "install_done_hint": _(
        "现在你可以查看系统配置。\n"
        "在目标设备上，检查 /etc/portage/make.conf 文件\n"
        "并根据你的 CPU 和其他选项调整 MAKEOPTS。"
    ),
    "err_no_unmounted_partitions": _(
        "在选定的磁盘上没有未挂载的分区。\n"
        "请卸载它或选择其他磁盘。"
    ),
    "err_partition_mounted": _("该分区已挂载–请选择其他分区。"),
    "suffix_mounted": _("(已挂载)"),
    "info_set_password": _(
        "将会出现一个终端窗口来设置用户密码。\n"
        "提示：使用强且唯一的密码！"
    ),
    "btn_set_password": _("设置用户密码"),
    "tooltip_partition_help": _("磁盘分区说明 – 详细信息"),
    "info_partition_help": _(
        "UEFI (GPT)：\n"
        " • 300–400 MB FAT32 — 标志：boot，esp\n"
        " • 剩余空间 ext4 — 根文件系统 /\n\n"
        "BIOS / MBR（传统）：\n"
        " • 3 MB（未格式化）— 标志：bios_grub，grub_bios\n"
        " • 剩余空间 ext4 — 根文件系统 /"
    ),
}
