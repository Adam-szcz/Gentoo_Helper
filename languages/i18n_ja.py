"""
i18n_ja.py
----------
Japanese messages for Gentoo Helper.
"""

def _(s):
    return s

MESSAGES = {
    # — Application —
    "app_title": _("Gentoo Helper"),

    # — Wizard step titles —
    "step_select_disk":   _("ステップ1 – ディスクの選択"),
    "step_efi":           _("ステップ2 – EFIを使用しますか？"),
    "step_partitions":    _("ステップ3 – パーティションの選択"),
    "step_stage3":        _("ステップ4 – Stage 3のダウンロードまたはシステムへ入る"),
    "step_enter_chroot":  _("ステップ5 – chrootに入る"),
    "step_root_passwd":   _("ステップ6 – rootパスワードの設定"),
    "step_pkg_helper":    _("ステップ7 – パッケージマネージャ"),
    "step_install_opts":  _("ステップ8 – インストールオプション"),
    "step_exit":          _("ステップ9 – インストールの完了"),

    # — Button labels —
    "btn_select":          _("選択"),
    "btn_yes":             _("はい"),
    "btn_no":              _("いいえ"),
    "btn_back":            _("◀ 戻る"),
    "btn_next":            _("次へ ▶"),
    "btn_install":         _("インストール ▶"),
    "btn_parted":          _("ディスクのパーティション分割"),
    "btn_download_stage3": _("Stage 3をダウンロード ▶"),
    "btn_enter_chroot":    _("システムへ入る ▶"),
    "btn_packages":        _("パッケージ ▶"),
    "btn_terminal":        _("端末 ▶"),
    "btn_root_passwd":     _("rootパスワード設定 ▶"),
    "btn_exit":            _("終了"),
    "extracting_text":     _("展開中…"),

    # — Informational texts —
    "info_choose_option": _("以下のオプションから選択してください:"),
    "info_stage3": _(
        "新しい端末ウィンドウでlinksブラウザが開きます。\n"
        "stage3デスクトッププロファイル | openrcファイルを選択してダウンロードしてください。\n"
        "端末を閉じた後、自動で展開が開始されます。"
    ),
    "info_root_passwd": _(
        "ボタンをクリックすると、新しい端末で/mnt/gentoo chroot内の\n"
        "passwdコマンドが実行されます。\n"
        "端末を閉じると次に進みます。"
    ),

    # — Error & dialog texts —
    "err_no_terminal": _(
        "ターミナルエミュレーターが見つかりません。\n"
        "xterm、gnome-terminal、またはkonsoleをインストールしてください。"
    ),
    "err_no_stage3":      _("Stage 3が/mnt/gentooに見つかりません。"),
    "err_stage3":         _("まずStage 3をダウンロードして展開してください。"),
    "err_field_required1": _("「User」フィールドを空にすることはできません！"),
    "err_field_required2": _("「jobs」フィールドを空にすることはできません！"),
    "err_field_integer":  _("「jobs」フィールドは整数でなければなりません！"),

    "pkg_sync_text":      _("Python 3とeixをインストールし、Portageツリーを同期しますか？"),
    "pkg_sync_info": _(
        "これは一度だけの操作です。次回以降はパッケージGUIがすぐに起動します。"
    ),

    # — Installation finished —
    "install_done_title": _("✓ インストール完了！"),
    "install_done_info": _(
        "インストーラーを閉じるか、インストール済みのシステムで追加操作を行うことができます。"
    ),
    "btn_close": _("閉じる"),

    # — Field labels —
    "label_root": _("ルート（/）："),
    "label_efi":  _("EFI（/boot）："),

    # — Step —
    "step_export_vars": "環境変数のエクスポート",
    "step_config_makeconf_initial": "make.conf 初期設定",
    "step_generate_locales": "ロケールの生成",
    "step_eselect_locale": "eselectでロケールを設定",
    "step_sync_portage": "Portageの同期",
    "step_update_world": "システムの更新（world）",
    "step_config_makeconf_final": "make.conf 最終設定",
    "step_extra_cflags": "EXTRA_CFLAGSの設定",
    "step_install_kernel": "カーネルのインストール",
    "step_microcode": "マイクロコードの設定",
    "step_link_linux": "カーネルへのシンボリックリンク",
    "step_genkernel": "カーネルのビルド（genkernel）",
    "step_env_update": "Env-update",
    "step_repo": "eselect-repositoryのインストール",
    "step_eselect": "eselectでオーバーレイを追加",
    "step_sync_overlays": "オーバーレイの同期",
    "step_update_world2": "システムの再更新",
    "step_install_programs": "プログラムのインストール",
    "step_useradd": "ユーザーの追加",
    "step_autostart_x": "Xの自動起動",
    "step_set_desktop_env": "デスクトップ環境の設定",
    "step_set_desktop_env_xterm": "デスクトップ環境の設定（Xterm）",
    "step_sudoers": "sudoersの設定",
    "step_history": "コマンド履歴の設定",
    "step_dbus": "dbusを自動起動に追加",
    "step_networkmanager": "NetworkManagerを自動起動に追加",
    "step_autologin": "自動ログインの設定",
    "step_set_user_passwd": "ユーザーのパスワード設定",
    "step_install_grub_uefi": "GRUBのインストール（UEFI）",
    "step_install_grub_bios": "GRUBのインストール（BIOS）",
    "env_none": "なし（XTermのみ）",
        "x_desktop": _("デスクトップ環境:"),
    "step_grub_time": _("GRUBを非表示にする"),
    "step_history_chown": _("権限を設定"),
    # — Final extra hint —
    "install_done_hint": _(
        "これでシステム設定を確認できます。\n"
        "ターゲットハードウェアで /etc/portage/make.conf ファイルを確認し、\n"
        "CPUやその他のオプションに合わせてMAKEOPTSを調整してください。"
    ),
    "err_no_unmounted_partitions": _(
        "選択したディスクには未マウントのパーティションがありません。\n"
        "アンマウントするか、別のディスクを選択してください。"
    ),
    "err_partition_mounted": _("このパーティションはマウントされています–別のものを選択してください。"),
    "suffix_mounted": _("(マウント済み)"),
    "info_set_password": _(
        "ユーザーのパスワードを設定するために端末ウィンドウが表示されます。\n"
        "ヒント：強力でユニークなパスワードを使用してください！"
    ),
    "btn_set_password": _("ユーザーのパスワードを設定"),
    "tooltip_partition_help": _("ディスクのパーティション方法 – 詳細"),
    "info_partition_help": _(
        "UEFI (GPT):\n"
        " ・300～400 MB FAT32 — フラグ: boot, esp\n"
        " ・残りを ext4 — ルートファイルシステム /\n\n"
        "BIOS / MBR (レガシー):\n"
        " ・3 MB（未フォーマット）— フラグ: bios_grub, grub_bios\n"
        " ・残りを ext4 — ルートファイルシステム /"
    ),
    "missing_package": _("パッケージ {pkg} が見つかりません。"),
    "install_prompt": _("{pkg} パッケージをインストールしますか？"),
    "install_failed": _("{pkg} パッケージのインストールに失敗しました。"),
}
