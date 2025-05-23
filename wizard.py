#!/usr/bin/env python3
import os
import sys
import errno
import fcntl
import signal
import tempfile
import importlib
import locale
import atexit
import shutil
import threading
import subprocess
import multiprocessing
from pathlib import Path
from datetime import datetime
import re
import pty
import gi
from disk_utils import list_disks, list_partitions

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Pango

# ── blokada instancji ──────────────────────────────────────
_LOCK_PATH = os.path.join(tempfile.gettempdir(), "gentoo_helper.lock")

def show_duplicate_dialog_and_exit(pid=None):
    dialog = Gtk.MessageDialog(
        None, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
        "Gentoo Helper is already running."
    )
    if pid:
        dialog.format_secondary_text(f"Another instance (PID {pid}) is running.\nDo you want to terminate it?")
    else:
        dialog.format_secondary_text("Another instance is running.\nDo you want to terminate it?")
    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.YES

def get_locked_pid(lock_path):
    try:
        with open(lock_path, "r") as f:
            return int(f.read().strip())
    except Exception:
        return None

try:
    _lock_fh = open(_LOCK_PATH, "w+")
    fcntl.flock(_lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    _lock_fh.seek(0)
    _lock_fh.write(str(os.getpid()))
    _lock_fh.truncate()
    _lock_fh.flush()
except OSError as e:
    if e.errno in (errno.EACCES, errno.EAGAIN):
        pid = get_locked_pid(_LOCK_PATH)
        if show_duplicate_dialog_and_exit(pid):
            if pid:
                try:
                    os.kill(pid, signal.SIGTERM)
                except Exception:
                    pass
            import time
            for _ in range(10):
                try:
                    fcntl.flock(_lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError:
                    time.sleep(0.2)
            else:
                print("⚠  Could not acquire lock after killing previous process.")
                sys.exit(1)
        else:
            sys.exit(0)
    else:
        raise

atexit.register(lambda: _lock_fh.close())

# ── i18n helper ────────────────────────────────────────────
def set_language(code: str):
    """Dynamically (re)load language module into global `i18n`."""
    module = importlib.import_module(f"languages.i18n_{code}")
    globals()["i18n"] = module

_SUPPORTED = {"pl", "en", "es", "fr", "de", "pt", "ru", "zh", "ja", "it"}

_loc = (locale.getdefaultlocale()[0] or "").lower()
_lang_short = _loc.split("_", 1)[0]
_code = _lang_short if _lang_short in _SUPPORTED else "pl"
set_language(_code)
print(f"[i18n] ustawiono język: {_code}")

class SetupWizardWindow(Gtk.Window):
    def __init__(self):
        self.timer_running = False
        self.verbose_gui = False
        self.DESKTOP_ENVS = {
            i18n.MESSAGES["env_none"]: {
                "packages": "",
                "start_cmd": ""
            },
            "LXQt": {
                "packages": "lxqt-base/lxqt-meta",
                "start_cmd": "exec startlxqt"
            },
            "Xfce": {
                "packages": "xfce-base/xfce4-meta",
                "start_cmd": "exec startxfce4"
            },
            "LXDE": {
                "packages": "lxde-base/lxde-meta",
                "start_cmd": "exec startlxde"
            },
            "MATE": {
                "packages": "mate-base/mate",
                "start_cmd": "exec mate-session"
            },
            "KDE Plasma": {
                "packages": "kde-plasma/plasma-meta",
                "start_cmd": "exec startplasma-x11"
            },
            "GNOME": {
                "packages": "gnome-base/gnome",
                "start_cmd": "exec gnome-session"
            },
            "GNOME-Light": {
                "packages": "gnome-base/gnome-light",
                "start_cmd": "exec gnome-session"
            },
            "Cinnamon": {
                "packages": "gnome-extra/cinnamon",
                "start_cmd": "exec cinnamon-session"
            },
            "Openbox": {
                "packages": "x11-wm/openbox",
                "start_cmd": "exec openbox-session"
            }
        }

        super().__init__(title=i18n.MESSAGES["app_title"])
        # ---- ADD CSS FOR TRANSPARENT BACKGROUND ----
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b"""
        .transparent-bg, textview, text, .transparent-bg textview, .transparent-bg text {
            background-color: transparent;
            background-image: none;
            border: none;
            box-shadow: none;
        }
        #timer-label {
            font-size: 42px;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 8px #333, 0 0 16px #000;
            padding: 24px;
            border-radius: 20px;
        }
        """)

        self.partitioned = False

        # Set default window size and center it
        self.set_default_size(700, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Remove window decorations
        self.set_decorated(False)

        # Allow dragging the window from anywhere with left mouse
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self._on_drag_begin)

        # Prepare background overlay
        overlay = Gtk.Overlay()
        self.add(overlay)

        ASSET_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets/gentoo_two_squares_smooth.png"
        )
        pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            ASSET_PATH,
            width=800, height=500,
            preserve_aspect_ratio=True
        )
        bg = Gtk.Image.new_from_pixbuf(pix)
        overlay.add(bg)

        # Narrower side panel for wizard steps
        self.step_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12
        )
        self.step_box.set_size_request(260, -1)
        self.step_box.set_halign(Gtk.Align.START)
        self.step_box.set_valign(Gtk.Align.START)
        self.step_box.set_margin_top(25)
        self.step_box.set_margin_start(25)
        overlay.add_overlay(self.step_box)
        # ─── TUTAJ DODAJEMY PASEK POSTĘPU ───
        self.progress_label = Gtk.Label(label="")
        self.progress_label.set_halign(Gtk.Align.START)
        self.progress_label.set_valign(Gtk.Align.CENTER)
        self.progress_label.set_margin_top(12)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_margin_top(6)
        self.progress_bar.set_show_text(True)

        # na start schowane
        self.progress_label.hide()
        self.progress_bar.hide()
        # Stwórz minutnik ZANIM dodasz go do overlay!
        self.timer_label = Gtk.Label()
        self.timer_label.set_halign(Gtk.Align.CENTER)
        self.timer_label.set_valign(Gtk.Align.CENTER)
        self.timer_label.set_justify(Gtk.Justification.CENTER)
        self.timer_label.set_opacity(0.92)
        self.timer_label.set_name("timer-label")
        self.timer_label.set_no_show_all(True)
        overlay.add_overlay(self.timer_label)
        overlay.set_overlay_pass_through(bg, True)
        # Step 1: disk selection
        self._build_welcome()
        self.show_all()

    # ------------------------------------------------------------------
    def _copy_helper_tree(self, dest_root: str):
        """
        Kopiuje Gentoo Helpera do <dest_root>/gento_helper
        – pomija katalogi __pycache__ i pliki *.pyc.
        """
        from pathlib import Path, PurePosixPath
        import shutil, os, fnmatch

        src_root = Path(__file__).resolve().parent          # katalog z wizard.py
        dest_dir = Path(dest_root) / "gento_helper"

        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        def _ignore(path, names):
            ignored = []
            for n in names:
                if n == "__pycache__" or fnmatch.fnmatch(n, "*.pyc"):
                    ignored.append(n)
            return set(ignored)

        shutil.copytree(src_root, dest_dir, ignore=_ignore)

        # pliki, których naprawdę nie chcemy przenosić (opcjonalnie)
        for extra in ("gento_helper.tar.gz",):
            p = dest_dir / PurePosixPath(extra)
            if p.exists():
                p.unlink()

    def _run_in_terminal(self, cmd_args, cwd=None, callback=None):
        # Launch the given command list in the selected terminal emulator.
        # If callback is provided, register it to be called when the process exits.
        term = self._pick_terminal()
        if not term:
            return self._error_dialog(i18n.MESSAGES["err_no_terminal"])

        # gnome-terminal uses “--”, others use “-e”
        if term == "gnome-terminal":
            full_cmd = [term, "--"] + cmd_args
        else:
            full_cmd = [term, "-e"] + cmd_args

        proc = subprocess.Popen(full_cmd, cwd=cwd)
        if callback:
            GLib.child_watch_add(GLib.PRIORITY_DEFAULT, proc.pid, callback)
        return proc


    def _ensure_mounted(self, src: str, dst: str, *, fs_type: str = None,
                        bind: bool = False, rbind: bool = False):
        """
        Ensure that src is mounted on dst.
        - Creates dst if it doesn't exist.
        - If bind=True, does `mount --bind src dst`.
        - If rbind=True, does `mount --rbind src dst`.
        - Otherwise mounts with optional fs_type.
        """
        import os, subprocess  # jeśli nie masz ich na górze pliku
        if not os.path.ismount(dst):
            os.makedirs(dst, exist_ok=True)
            if bind:
                subprocess.run(["mount", "--bind", src, dst], check=True)
            elif rbind:
                subprocess.run(["mount", "--rbind", src, dst], check=True)
            else:
                cmd = ["mount"]
                if fs_type:
                    cmd += ["-t", fs_type]
                cmd += [src, dst]
                subprocess.run(cmd, check=True)

    def _on_drag_begin(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            # x_root / y_root must be ints
            self.begin_move_drag(
                event.button,
                int(event.x_root), int(event.y_root),
                event.time
            )

    # ── zamknij GTK i (ew.) terminal, w którym odpalono kreator ──
    def _quit_with_parent(self, _btn=None):
        Gtk.main_quit()

        import os, signal, re
        def proc_comm(pid):
            try:
                with open(f"/proc/{pid}/comm") as f:
                    return f.read().strip()
            except Exception:
                return ""

        def proc_ppid(pid):
            try:
                with open(f"/proc/{pid}/status") as f:
                    for ln in f:
                        if ln.startswith("PPid:"):
                            return int(ln.split()[1])
            except Exception:
                pass
            return 1   # init

        shells   = {"bash", "zsh", "fish", "dash", "ash"}
        terms    = {
            "qterminal", "konsole", "xterm", "gnome-terminal-",
            "xfce4-terminal", "lxterminal", "alacritty", "kitty"
        }

        ppid  = os.getppid()          # rodzic (zwykle shell *albo* terminal)
        pname = proc_comm(ppid)

        # 1) jeśli rodzicem jest powłoka → sprawdź dziadka
        if pname in shells:
            gpid  = proc_ppid(ppid)   # dziadek
            gname = proc_comm(gpid)
            if any(re.match(t, gname) for t in terms):
                try:
                    os.kill(gpid, signal.SIGTERM)
                except Exception:
                    pass
            return

        # 2) jeśli rodzicem **jest** terminal → zamknij go
        if any(re.match(t, pname) for t in terms):
            try:
                os.kill(ppid, signal.SIGTERM)
            except Exception:
                pass


    # ── posprzątaj paczkę gento_helper i zamknij kreator ──
    def _cleanup_and_quit(self, _btn=None):
        import shutil, os
        try:
            shutil.rmtree("/mnt/gentoo/gento_helper")
        except FileNotFoundError:
            pass                  
        except Exception as e:
            print(f"[warn] nie mogę skasować /mnt/gentoo/gento_helper: {e}")
        self._quit_with_parent()   


    def _build_step_finished(self):
        # usuń stare widżety
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        lbl  = Gtk.Label(label=i18n.MESSAGES["install_done_title"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        info = Gtk.Label(label=i18n.MESSAGES["install_done_info"])
        info.set_xalign(0)

        # ── przyciski ────────────────────────────────────────
        btn_pkg   = Gtk.Button(label=i18n.MESSAGES["btn_packages"])
        btn_pkg.connect("clicked", self._run_pkg_helper)

        btn_term  = Gtk.Button(label=i18n.MESSAGES["btn_terminal"])
        btn_term.connect("clicked", self._run_enter_chroot)


        btn_close = Gtk.Button(label=i18n.MESSAGES["btn_close"])
        btn_close.connect("clicked", self._cleanup_and_quit)

        hbox = Gtk.Box(spacing=12)
        for b in (btn_pkg, btn_term, btn_close):
            hbox.pack_start(b, False, False, 0)

        # ── dodatkowy hint POD przyciskami ───────────────────
        hint = Gtk.Label(label=i18n.MESSAGES.get("install_done_hint", ""))
        hint.set_xalign(0)
        hint.set_margin_top(10)
        hint.set_vexpand(True)
        hint.set_line_wrap(True)
        hint.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        # ── układ w kolumnie ─────────────────────────────────
        self.step_box.pack_start(lbl, False, False, 10)
        self.step_box.pack_start(info, False, False, 10)
        self.step_box.pack_start(self.timer_label, False, False, 4)  # <-- TIMER w tym miejscu!
        self.step_box.pack_start(hbox, False, False, 10)
        self.step_box.pack_start(hint, False, False, 10)
        self.step_box.show_all()

    # ────────────────────────────────────────────────────────────
    def _make_nav_buttons(self, back_cb, next_cb, next_label=None):
        """Return an H-box with ◀ Back and Next ▶ buttons."""
        nav = Gtk.Box(spacing=12)

        # Back
        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_back.connect("clicked", back_cb)
        nav.pack_start(btn_back, False, False, 0)

        # Next / Install
        lbl_next = next_label or i18n.MESSAGES["btn_next"]
        btn_next = Gtk.Button(label=lbl_next)
        btn_next.connect("clicked", next_cb)
        nav.pack_end(btn_next, False, False, 0)
        self.btn_next = btn_next
        return nav
    # ────────────────────────────────────────────────────────────

    def _build_step_select_disk(self, _btn=None):
        # Clear previous widgets
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # Title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_select_disk"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # Disk combo
        self.combo = Gtk.ComboBoxText(hexpand=False)
        self.combo.set_size_request(200, -1)
        for d in list_disks():
            txt = f"{d['path']} — {d['size']}"
            if d['model']:
                txt += f" ({d['model']})"
            self.combo.append_text(txt)
        self.combo.set_active(0)

        # --- TU USTAWIAMY selected_disk na starcie ---
        self.selected_disk = self.combo.get_active_text().split()[0]

        # --- ZAWSZE AKTUALIZUJ po zmianie ---
        def on_disk_changed(combo):
            self.selected_disk = combo.get_active_text().split()[0]
        self.combo.connect("changed", on_disk_changed)

        # Partition tool
        # ── wiersz z przyciskiem „Partycjonuj” i ikonką pomocy ──────────
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        btn_parted = Gtk.Button(label=i18n.MESSAGES.get("btn_parted"))
        btn_parted.set_size_request(370, -1)
        row.pack_start(btn_parted, False, False, 0)

        btn_help = Gtk.Button.new_from_icon_name("dialog-information-symbolic",
                                                 Gtk.IconSize.BUTTON)
        btn_help.set_tooltip_text(i18n.MESSAGES.get("tooltip_partition_help"))
        row.pack_start(btn_help, False, False, 0)

        # — okno z instrukcją partycjonowania —
        def on_part_help(_w):
            dlg = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Minimalne partycjonowanie dysku"
            )
            dlg.format_secondary_text(i18n.MESSAGES.get("info_partition_help"))
            dlg.run()
            dlg.destroy()

        btn_help.connect("clicked", on_part_help)
        btn_parted.connect("clicked", self._run_gparted)

        # ── pasek nawigacji (bez zmian) ─────────────────────────────────
        nav = self._make_nav_buttons(
            back_cb=self._build_welcome,
            next_cb=self._build_step_efi,
            next_label=i18n.MESSAGES["btn_next"]
        )

        # ── pakowanie: wstawiamy ROW zamiast pojedynczych przycisków ───
        for w in (lbl, self.combo, row, nav):
            self.step_box.pack_start(w, False, False, 10)

        self.step_box.show_all()



    # ── helper: is the device currently mounted? ────────────
    def _is_mounted(self, device_path: str) -> bool:
        """
        Return True if *device_path* (e.g. '/dev/sda3') appears in /proc/self/mounts.
        """
        try:
            with open("/proc/self/mounts", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(device_path + " "):
                        return True
        except FileNotFoundError:
            # extremely rare – proc not mounted
            pass
        return False

    def _run_gparted(self, _btn):
        device = (self.combo.get_active_text() or "/dev/sda").split()[0]

        # ➜ zablokuj „Dalej” na czas pracy GParted
        if hasattr(self, "btn_next"):
            self.btn_next.set_sensitive(False)

        try:
            proc = subprocess.Popen(
                ["gparted", device],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            GLib.child_watch_add(
                GLib.PRIORITY_DEFAULT,
                proc.pid,
                self._after_gparted
            )
        except FileNotFoundError:
            # GParted nie zainstalowany – odblokuj natychmiast
            self._after_gparted(None, 0)


    def _build_welcome(self, _btn=None):
        """First screen: logo + language selector + Start button."""
        # wipe panel in case of re-entry
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # headline
        lbl = Gtk.Label(label="Gentoo Helper")
        lbl.get_style_context().add_class("h2")
        lbl.set_xalign(0)

        # language selector
        lang_combo = Gtk.ComboBoxText()
        for code, label in [
                ("pl", "Polski"),
                ("en", "English"),
                ("es", "Español"),
                ("fr", "Français"),
                ("it", "Italiano"),
                ("de", "Deutsch"),
                ("pt", "Português (BR)"),
                ("ru", "Русский"),
                ("zh", "简体中文"),
                ("ja", "日本語"),

            ]:
            lang_combo.append(code, label)
        # pre-select current locale
        lang_combo.set_active_id(_code)

        def on_start(_btn):
            code = lang_combo.get_active_id()
            set_language(code)          # reload i18n → global
            # destroy welcome widgets
            self.step_box.foreach(lambda w: self.step_box.remove(w))
            # build real step 1 and hide combo
            self._build_step_select_disk()

        btn_start = Gtk.Button(label="Start ▶")
        btn_start.connect("clicked", on_start)

        # pack vertically
        for w in (lbl, lang_combo, btn_start):
            self.step_box.pack_start(w, False, False, 10)
        self.step_box.show_all()


    def _build_step_efi(self, _btn=None):
        # clear previous widgets
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_efi"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # radio buttons: UEFI / BIOS
        btn_yes = Gtk.RadioButton.new_with_label_from_widget(
            None,
            i18n.MESSAGES["btn_yes"] + " (UEFI)"
        )
        btn_no = Gtk.RadioButton.new_with_label_from_widget(
            btn_yes,
            i18n.MESSAGES["btn_no"] + " (BIOS)"
        )
        btn_yes.set_active(True)
        self.efi_choice = True
        btn_yes.connect("toggled", lambda b: setattr(self, "efi_choice", b.get_active()))
        btn_no.connect("toggled",  lambda b: setattr(self, "efi_choice", not b.get_active()))

        # navigation bar
        nav = Gtk.Box(spacing=12)
        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_back.connect("clicked", self._build_step_select_disk)
        btn_next = Gtk.Button(label=i18n.MESSAGES["btn_next"])
        btn_next.connect("clicked", self._build_step_partitions)
        nav.pack_start(btn_back, False, False, 0)
        nav.pack_end(btn_next, False, False, 0)

        # pack widgets
        for w in (lbl, btn_yes, btn_no, nav):
            self.step_box.pack_start(w, False, False, 0)
        self.step_box.show_all()


    def _build_step_partitions(self, _btn=None):
        # clear previous widgets
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_partitions"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        parts = list_partitions(self.combo.get_active_text().split()[0])

        # ── podziel na zamontowane i niezamontowane ──
        unmounted = [p for p in parts if not self._is_mounted(p)]
        mounted   = [p for p in parts if     self._is_mounted(p)]

        if not unmounted:
            self._error_dialog(i18n.MESSAGES["err_no_unmounted_partitions"])
            return self._build_step_select_disk()

        # root selection
        root_lbl = Gtk.Label(label=i18n.MESSAGES["label_root"]); root_lbl.set_xalign(0)
        root_combo = Gtk.ComboBoxText()
        for p in unmounted:
            root_combo.append_text(p)
        for p in mounted:
            root_combo.append_text(f"{p}  {i18n.MESSAGES['suffix_mounted']}")
        root_combo.set_active(0)

        # EFI (jeśli UEFI)
        if self.efi_choice:
            efi_lbl = Gtk.Label(label=i18n.MESSAGES["label_efi"]); efi_lbl.set_xalign(0)
            efi_combo = Gtk.ComboBoxText()
            for p in unmounted:
                efi_combo.append_text(p)
            for p in mounted:
                efi_combo.append_text(f"{p}  {i18n.MESSAGES['suffix_mounted']}")
            efi_combo.set_active(0)
        else:
            efi_combo = None

        # ── nawigacja ──
        nav = Gtk.Box(spacing=12)
        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_back.connect("clicked", self._build_step_efi)
        btn_next = Gtk.Button(label=i18n.MESSAGES["btn_next"])

        def update_next(_combo=None):
            sel = root_combo.get_active_text() or ""
            btn_next.set_sensitive(i18n.MESSAGES["suffix_mounted"] not in sel)

        update_next()  # stan początkowy
        root_combo.connect("changed", update_next)

        def on_next(_b):
            if i18n.MESSAGES["suffix_mounted"] in root_combo.get_active_text():
                return self._error_dialog(i18n.MESSAGES["err_partition_mounted"])
            self.root_part = root_combo.get_active_text()
            self.efi_part  = efi_combo.get_active_text() if efi_combo else None
            self._build_step_stage3()

        btn_next.connect("clicked", on_next)
        nav.pack_start(btn_back, False, False, 0)
        nav.pack_end(btn_next, False, False, 0)

        # ── ułóż w panelu ──
        self.step_box.pack_start(lbl, False, False, 0)
        self.step_box.pack_start(root_lbl, False, False, 0)
        self.step_box.pack_start(root_combo, False, False, 0)
        if self.efi_choice:
            self.step_box.pack_start(efi_lbl, False, False, 0)
            self.step_box.pack_start(efi_combo, False, False, 0)

        self.step_box.pack_start(nav, False, False, 10)
        self.step_box.show_all()


    # --------------------  STEP 4 / Stage 3  -------------------- #
    def _build_step_stage3(self, _btn=None):
        # clear previous widgets
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # if already unpacked, go straight to password step
        if _btn is None and Path("/mnt/gentoo/system.txt").exists():
            self._build_step_root_passwd()
            return

        # title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_stage3"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # informational text
        info = Gtk.Label(label=i18n.MESSAGES["info_stage3"])
        info.set_xalign(0)

        # download button
        btn_start = Gtk.Button(label=i18n.MESSAGES["btn_download_stage3"])
        btn_start.connect("clicked", self._run_links)

        # enter-chroot button
        btn_enter = Gtk.Button(label=i18n.MESSAGES["btn_enter_chroot"])
        btn_enter.connect("clicked", self._build_step_enter_chroot)

        # auto-extract on first entry
        if self._find_stage3() and _btn is None:
            btn_start.set_visible(False)
            GLib.idle_add(self._extract_stage3, self._find_stage3())

        ### ——— NOWE PRZYCISKI ———
        btn_openrc = Gtk.Button(label="Pobierz Stage3 OpenRC")
        btn_openrc.connect("clicked", self._download_openrc)   

        btn_systemd = Gtk.Button(label="Pobierz Stage3 systemd")
        btn_systemd.set_sensitive(False)          # na razie wyszarzony
        ### ————————————————

        # pack widgets
        for w in (lbl, info,            # teksty
                  btn_openrc, btn_systemd,  # nowe
                  btn_start, btn_enter):    # stare
            self.step_box.pack_start(w, False, False, 0)
        self.step_box.show_all()


    def _build_step_enter_chroot(self, _btn=None):
        # clear previous widgets
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_enter_chroot"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # instruction text
        info = Gtk.Label(label=i18n.MESSAGES["info_choose_option"])
        info.set_xalign(0)

        # --- NOWE PRZYCISKI NAD ISTNIEJĄCYMI ---
        btn_openrc = Gtk.Button(label="Pobierz Stage3 OpenRC")
        btn_openrc.connect("clicked", self._run_links)

        btn_systemd = Gtk.Button(label="Pobierz Stage3 systemd")
        btn_systemd.set_sensitive(False)          # szary / nieaktywny na razie

        # buttons: packages / terminal / back
        btn_pkg = Gtk.Button(label=i18n.MESSAGES["btn_packages"])
        btn_pkg.connect("clicked", self._run_pkg_helper)

        btn_terminal = Gtk.Button(label=i18n.MESSAGES["btn_terminal"])
        btn_terminal.connect("clicked", self._run_enter_chroot)

        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_back.connect("clicked", self._build_step_stage3)

        # pack widgets with 10px spacing
        for w in (lbl, info, btn_pkg, btn_terminal, btn_back):
            self.step_box.pack_start(w, False, False, 10)
        self.step_box.show_all()

    def _run_links(self, _btn):
        # 1) Mount /mnt/gentoo if needed
        self._ensure_mounted(self.root_part, "/mnt/gentoo")

        # 2) If already unpacked, skip
        if Path("/mnt/gentoo/system.txt").exists():
            self._finish_stage3()
            return

        # 3) If stage3 archive exists, extract immediately
        if self._find_stage3():
            self._extract_stage3(self._find_stage3())
            return

        # 4) Launch links in terminal
        term = self._pick_terminal()
        if not term:
            return self._error_dialog(i18n.MESSAGES["err_no_terminal"])

        cmd = [term, "--", "links", "https://www.gentoo.org/downloads/"] \
              if term == "gnome-terminal" else \
              [term, "-e", "links", "https://www.gentoo.org/downloads/"]

        proc = subprocess.Popen(cmd, cwd="/mnt/gentoo")
        GLib.child_watch_add(GLib.PRIORITY_DEFAULT, proc.pid, self._after_links)

    # ---------- URL do najnowszego stage3-openrc ----------
    def _latest_stage3_openrc_url(self):
        """
        Zwraca pełny URL do najświeższego archiwum Stage3-OpenRC (amd64-desktop).

        Plik latest-*.txt zawiera komentarze, rozmiary i podpis PGP – bierzemy
        pierwszą nie-pustą linię, która NIE zaczyna się od '#', '-----' ani 'MD5',
        a następnie pierwszy token przed spacją.
        """
        import urllib.request
        base = "https://distfiles.gentoo.org/releases/amd64/autobuilds/"

        txt = urllib.request.urlopen(
            base + "latest-stage3-amd64-desktop-openrc.txt",
            timeout=10
        ).read().decode(errors="replace")

        for raw in txt.splitlines():
            line = raw.strip()
            if (not line or line.startswith("#") or line.startswith("-----")
                    or line.lower().startswith("md5")):
                continue                    # pomiń komentarze / PGP / sumy
            rel_path = line.split()[0]      # token przed spacją = ścieżka
            if rel_path.endswith(".tar.xz"):
                return base + rel_path

        raise RuntimeError("Nie znalazłem ścieżki do Stage3 w latest-*.txt")

    # ---------------- pobieranie Stage3 (OpenRC) ----------------
    def _download_openrc(self, _btn):
        from pathlib import Path
        import urllib.request, threading, os
        # 1) – upewnij się, że /mnt/gentoo jest podmontowane
        self._ensure_mounted(self.root_part, "/mnt/gentoo")

        # 2) – jeśli już gotowe, pomiń wszystko
        if Path("/mnt/gentoo/system.txt").exists():
            return self._finish_stage3()

        # 3) – jeśli archiwum już leży w /mnt/gentoo, od razu rozpakuj
        prev = self._find_stage3()
        if prev:
            return self._extract_stage3(prev)

        # 4) – wyczyść panel i pokaż TYLKO pasek
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        lbl = Gtk.Label(label="Pobieranie Stage3 (OpenRC)…")
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_show_text(True)   # % w samym pasku
        self.progress_bar.set_text("0 %")
        self.progress_bar.show()

        # wrzuć do panelu (etykieta + pasek)
        for w in (lbl, self.progress_label, self.progress_bar):
            self.step_box.pack_start(w, False, False, 10)
        self.step_box.show_all()

        # 5) – pobieranie w tle
        url = self._latest_stage3_openrc_url()
        dest = os.path.join("/mnt/gentoo", os.path.basename(url))

        def worker():
            try:
                with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
                    total = int(r.getheader("Content-Length", "0") or 0)
                    done  = 0
                    blk   = 65536          # większy blok = mniej zrywań
                    last_pct = -1

                    while True:
                        chunk = r.read(blk)
                        if not chunk:
                            break
                        f.write(chunk)
                        done += len(chunk)

                        if total:
                            pct = int(done * 100 / total)
                            if pct > last_pct:          # tylko gdy rośnie
                                last_pct = pct
                                frac = pct / 100
                                GLib.idle_add(self.progress_bar.set_fraction, frac)
                                GLib.idle_add(self.progress_bar.set_text, f"{pct} %")
                        else:
                            GLib.idle_add(self.progress_bar.pulse)


                # pobrane – przechodzimy do rozpakowywania
                GLib.idle_add(self.progress_label.set_text, "Rozpakowywanie…")
                GLib.idle_add(self.progress_bar.set_text, i18n.MESSAGES["extracting_text"])
                GLib.idle_add(self._extract_stage3, dest)

            except Exception as e:
                GLib.idle_add(self._error_dialog, f"Błąd pobierania:\n{e}")

        threading.Thread(target=worker, daemon=True).start()


    def _after_links(self, _pid, _status):
        # Called after the links terminal closes; proceed if a stage3 tarball was found
        stage3 = self._find_stage3()
        if not stage3:
            return self._error_dialog(i18n.MESSAGES["err_no_stage3"])
        self._extract_stage3(stage3)

    def _find_stage3(self):
        # Search for stage3-*.tar.xz files in /mnt/gentoo and its /boot subdir
        dirs = ["/mnt/gentoo"]
        if os.path.isdir("/mnt/gentoo/boot"):
            dirs.append("/mnt/gentoo/boot")

        files = []
        for d in dirs:
            try:
                entries = os.listdir(d)
            except OSError:
                # skip directories that can’t be accessed
                continue
            for f in entries:
                if f.startswith("stage3") and f.endswith(".tar.xz"):
                    files.append(os.path.join(d, f))

        if not files:
            return None
        files.sort(key=os.path.getmtime, reverse=True)
        return files[0]

    def _extract_stage3(self, tarball):
        # --- jeden, wspólny pasek dla pobierania i rozpakowywania ---
        if not self.progress_label.get_parent():
            self.step_box.pack_start(self.progress_label, False, False, 10)
        self.progress_label.set_text(i18n.MESSAGES["extracting_text"])
        self.progress_label.show()
        if hasattr(self, "progress_bar") and self.progress_bar.get_parent():
            self.prog = self.progress_bar          # ← re-use
        else:
            self.prog = Gtk.ProgressBar()
            self.step_box.pack_start(self.prog, False, False, 10)
            self.step_box.show_all()

        self.prog.set_show_text(False)             # bez napisu
        self.prog.set_fraction(0)


        def pulse():
            # pulse the progress bar to indicate ongoing extraction
            self.prog.pulse()
            return True

        GLib.timeout_add(150, pulse)

        def untar():
            # extract the stage3 archive
            subprocess.call(
                ["tar", "xpf", tarball, "-C", "/mnt/gentoo"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            # mark completion
            Path("/mnt/gentoo/system.txt").touch()
            # remove the archive to save space
            try:
                os.remove(tarball)
            except OSError:
                pass
            # cleanup and advance
            GLib.idle_add(self.prog.destroy)
            GLib.idle_add(self._finish_stage3)

        # run extraction in a background thread
        threading.Thread(target=untar, daemon=True).start()

    def _bind_system_dirs(self):
        """
        Mount essential system directories (proc, sys, dev (+ devpts), run),
        opcjonalnie EFI, oraz skopiuj /etc/resolv.conf do chroota.
        """
        # — EFI (jeśli potrzebne) —
        if getattr(self, "efi_part", None):
            boot_dst = "/mnt/gentoo/boot"
            os.makedirs(boot_dst, exist_ok=True)
            if not os.path.ismount(boot_dst):
                subprocess.run(["mount", self.efi_part, boot_dst], check=True)

        # — X11 socket (GUI w chroocie) —
        os.makedirs("/mnt/gentoo/tmp/.X11-unix", exist_ok=True)   # ← DODAJ
        if (os.path.exists("/tmp/.X11-unix")
                and not os.path.ismount("/mnt/gentoo/tmp/.X11-unix")):
            subprocess.run(
                ["mount", "--bind", "/tmp/.X11-unix", "/mnt/gentoo/tmp/.X11-unix"],
                check=True
            )

        # — Przygotuj punkty montowania —
        for sub in ("proc", "sys", "dev", "run"):
            os.makedirs(f"/mnt/gentoo/{sub}", exist_ok=True)
        os.makedirs("/mnt/gentoo/dev/pts", exist_ok=True)

        # — procfs —
        if not os.path.ismount("/mnt/gentoo/proc"):
            subprocess.run(["mount", "-t", "proc", "proc", "/mnt/gentoo/proc"], check=True)

        # — sysfs —
        if not os.path.ismount("/mnt/gentoo/sys"):
            subprocess.run(["mount", "--rbind", "/sys", "/mnt/gentoo/sys"], check=True)
            subprocess.run(["mount", "--make-rslave", "/mnt/gentoo/sys"], check=True)

        # — devtmpfs —
        if not os.path.ismount("/mnt/gentoo/dev"):
            subprocess.run(["mount", "--rbind", "/dev", "/mnt/gentoo/dev"], check=True)
            subprocess.run(["mount", "--make-rslave", "/mnt/gentoo/dev"], check=True)

        # — devpts (pty) —
        if not os.path.ismount("/mnt/gentoo/dev/pts"):
            subprocess.run([
                "mount", "-t", "devpts", "devpts", "/mnt/gentoo/dev/pts",
                "-o", "gid=5,mode=620"
            ], check=True)

        # — tmpfs /run —
        if not os.path.ismount("/mnt/gentoo/run"):
            subprocess.run(["mount", "--rbind", "/run", "/mnt/gentoo/run"], check=True)
            subprocess.run(["mount", "--make-rslave", "/mnt/gentoo/run"], check=True)

        # — X11 socket (GUI w chroocie) —
        os.makedirs("/mnt/gentoo/tmp/.X11-unix", exist_ok=True) 
        if (os.path.exists("/tmp/.X11-unix")
                and not os.path.ismount("/mnt/gentoo/tmp/.X11-unix")):
            subprocess.run(
                ["mount", "--bind", "/tmp/.X11-unix", "/mnt/gentoo/tmp/.X11-unix"],
                check=True
            )

        # — Wayland (opcjonalnie) —
        uid = os.getenv("SUDO_UID") or str(os.getuid())
        wl_src = f"/run/user/{uid}"
        wl_dst = f"/mnt/gentoo/run/user/{uid}"
        if os.path.exists(wl_src) and not os.path.ismount(wl_dst):
            os.makedirs(wl_dst, exist_ok=True)
            subprocess.run(["mount", "--rbind", wl_src, wl_dst], check=True)
            subprocess.run(["mount", "--make-rslave", wl_dst], check=True)


        # — skopiuj DNS —
        subprocess.run([
            "cp", "-L",
            "/etc/resolv.conf",
            "/mnt/gentoo/etc/resolv.conf"
        ], check=True)


    def _finish_stage3(self):
        # bind system dirs and proceed to root password step
        self._bind_system_dirs()
        self._build_step_root_passwd()

    def _after_root_passwd(self, _pid, _status):
        """
        Called after the root password is set; proceed to installation options.
        """
        self._build_step_install_options()


    # -------------------- STEP 5 / Ustaw hasło roota -------------------- #
    def _build_step_root_passwd(self, _btn=None):
        # Clear the wizard panel
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # Title for root password step
        lbl = Gtk.Label(label=i18n.MESSAGES["step_root_passwd"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # Instruction text
        info = Gtk.Label(label=i18n.MESSAGES["info_root_passwd"])
        info.set_xalign(0)

        # Button to launch passwd in chroot
        btn_passwd = Gtk.Button(label=i18n.MESSAGES["btn_root_passwd"])
        btn_passwd.connect("clicked", self._run_root_passwd)

        # Back navigation
        nav = Gtk.Box(spacing=12)
        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_back.connect("clicked", self._build_step_stage3)
        nav.pack_start(btn_back, False, False, 0)

        # Pack widgets with 10px spacing
        for w in (lbl, info, btn_passwd, nav):
            self.step_box.pack_start(w, False, False, 10)
        self.step_box.show_all()

    def _build_step_user_passwd(self, _btn=None):
        """
        Show dialog to set password for the user account after installation.
        """
        # Clear the current panel
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # Title
        lbl = Gtk.Label(label=f"User: {self.NASZUSER}")
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # Info text
        info = Gtk.Label(label=i18n.MESSAGES["info_set_password"])
        info.set_xalign(0)

        # Button to start passwd in chroot
        btn_passwd = Gtk.Button(label=i18n.MESSAGES["btn_set_password"])
        btn_passwd.connect("clicked", self._run_user_passwd)

        self.step_box.pack_start(lbl, False, False, 10)
        self.step_box.pack_start(info, False, False, 10)
        self.step_box.pack_start(btn_passwd, False, False, 10)
        self.step_box.show_all()

    def _run_user_passwd(self, _btn):
        """
        Run passwd in chroot for the user, then go to finish screen.
        """
        self._run_in_terminal(
            ["chroot", "/mnt/gentoo", "passwd", self.NASZUSER],
            callback=self._after_user_passwd
        )

    def _after_user_passwd(self, _pid, _status):
        """
        After setting user password, show final installation screen.
        """
        self._build_step_finished()



    def _run_root_passwd(self, _btn):
        # Launch passwd inside the chroot and call _after_root_passwd when done
        self._run_in_terminal(
            ["chroot", "/mnt/gentoo", "/bin/passwd"],
            callback=self._after_root_passwd
        )

    def _run_enter_chroot(self, _btn=None):
        # Ensure root partition is mounted at /mnt/gentoo
        self._ensure_mounted(self.root_part, "/mnt/gentoo")

        # Verify that Stage3 has been unpacked
        if not Path("/mnt/gentoo/bin/bash").is_file():
            return self._error_dialog(i18n.MESSAGES["err_stage3"])

        # Bind system directories and copy DNS
        self._bind_system_dirs()

        # Launch an interactive shell inside the chroot
        self._run_in_terminal(
            ["chroot", "/mnt/gentoo", "/bin/bash"]
        )


    def _run_pkg_helper(self, _btn=None):
        # Ensure root partition is mounted at /mnt/gentoo
        self._ensure_mounted(self.root_part, "/mnt/gentoo")

        # Verify that Stage3 has been unpacked
        if not Path("/mnt/gentoo/bin/bash").is_file():
            return self._error_dialog(i18n.MESSAGES["err_stage3"])

        # Bind system directories and copy DNS
        self._bind_system_dirs()

        # --- skopiuj pliki Gentoo Helpera do /gento_helper -------------
        try:
            self._copy_helper_tree("/mnt/gentoo")
        except Exception as e:
            return self._error_dialog(f"Błąd kopiowania plików:\n{e}")

        # Determine if this is the first run (sync + eix + python)
        sync_flag = Path("/mnt/gentoo/system.txt")
        first_run = not (sync_flag.exists() and sync_flag.read_text().strip() == "sync")

        # ── przygotuj ENV (DISPLAY + XDG_RUNTIME_DIR) ───────────────────
        env = os.environ.copy()
        env.setdefault("DISPLAY", ":0")

        uid = env.get("SUDO_UID") or env.get("UID") or str(os.getuid())
        env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")

        # (nie zaszkodzi wyświetlić info do logu)
        print("[info] DISPLAY =", env["DISPLAY"], " XDG_RUNTIME_DIR =", env["XDG_RUNTIME_DIR"])

        # ── pierwszy raz: pokaż dialog i dodaj emerge --sync, python, eix ─
        if first_run:
            dlg = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.NONE,
                text=i18n.MESSAGES["pkg_sync_text"]
            )
            dlg.format_secondary_text(i18n.MESSAGES["pkg_sync_info"])
            dlg.add_button(i18n.MESSAGES.get("pkg_sync_no", i18n.MESSAGES["btn_back"]),
                           Gtk.ResponseType.CANCEL)
            dlg.add_button(i18n.MESSAGES.get("pkg_sync_yes", i18n.MESSAGES["btn_next"]),
                           Gtk.ResponseType.OK)
            if dlg.run() != Gtk.ResponseType.OK:
                dlg.destroy()
                return          # użytkownik wybrał „Wstecz”
            dlg.destroy()
            try:
                sync_flag.write_text("sync")
            except Exception:
                pass

            inner = (
                "emerge --sync && "
                "emerge dev-lang/python app-portage/eix && "
                "python3 /gento_helper/prog/main.py"
            )
        else:
            inner = "python3 /gento_helper/prog/main.py"

        try:
            subprocess.run(["xhost", "+SI:localuser:root"], check=True)
        except Exception as e:
            print("[warn] Nie udało się wykonać xhost:", e)

        # ── odpal w chroocie z przygotowanym ENV ────────────────────────
        self._run_in_terminal([
            "chroot", "/mnt/gentoo", "bash", "-lc",
            f"export DISPLAY='{env['DISPLAY']}' XDG_RUNTIME_DIR='{env['XDG_RUNTIME_DIR']}'; {inner}"
       ])



    # -------------------- STEP 7 / Opcje instalacji -------------------- #
    def _build_step_install_options(self, _btn=None):

        # ─────────────────────────────────────────────────────────────
        # Pełne listy architektur GCC 14
        march_list = [
            # Intel/CPU klasa x86 32-bit
            "i386","i486","i586","pentium","lakemont","pentium-mmx","winchip-c6",
            "winchip2","c3","samuel-2","c3-2","nehemiah","c7","esther","i686",
            "pentiumpro","pentium2","pentium3","pentium3m","pentium-m","pentium4",
            "pentium4m","prescott","nocona","core2","nehalem","corei7","westmere",
            "sandybridge","corei7-avx","ivybridge","core-avx-i","haswell","core-avx2",
            "broadwell","skylake","skylake-avx512","cannonlake","icelake-client",
            "rocketlake","icelake-server","cascadelake","tigerlake","cooperlake",
            "sapphirerapids","emeraldrapids","alderlake","raptorlake","meteorlake",
            "graniterapids","graniterapids-d","arrowlake","arrowlake-s","lunarlake",
            "pantherlake","bonnell","atom","silvermont","slm","goldmont",
            "goldmont-plus","tremont","gracemont","sierraforest","grandridge",
            "clearwaterforest","knl","knm","intel","geode",
            # AMD / VIA / x86-64
            "k6","k6-2","k6-3","athlon","athlon-tbird","athlon-4","athlon-xp",
            "athlon-mp","x86-64","x86-64-v2","x86-64-v3","x86-64-v4","eden-x2",
            "nano","nano-1000","nano-2000","nano-3000","nano-x2","eden-x4","nano-x4",
            "lujiazui","yongfeng","k8","k8-sse3","opteron","opteron-sse3",
            "athlon64","athlon64-sse3","athlon-fx","amdfam10","barcelona",
            "bdver1","bdver2","bdver3","bdver4","znver1","znver2","znver3",
            "znver4","znver5","btver1","btver2","generic","native"
        ]

        mtune_list = [
            "generic","i386","i486","pentium","lakemont","pentiumpro","pentium4",
            "nocona","core2","nehalem","sandybridge","haswell","bonnell",
            "silvermont","goldmont","goldmont-plus","tremont","sierraforest",
            "grandridge","clearwaterforest","knl","knm","skylake","skylake-avx512",
            "cannonlake","icelake-client","icelake-server","cascadelake",
            "tigerlake","cooperlake","sapphirerapids","alderlake","rocketlake",
            "graniterapids","graniterapids-d","arrowlake","arrowlake-s",
            "pantherlake","intel","lujiazui","yongfeng","geode","k6","athlon",
            "k8","amdfam10","bdver1","bdver2","bdver3","bdver4","btver1",
            "btver2","znver1","znver2","znver3","znver4","znver5","native"
        ]
        # ─────────────────────────────────────────────────────────────


        # Clear the wizard panel
        self.step_box.foreach(lambda w: self.step_box.remove(w))

        # Step title
        lbl = Gtk.Label(label=i18n.MESSAGES["step_install_opts"])
        lbl.get_style_context().add_class("h3")
        lbl.set_xalign(0)

        # Input fields grid
        grid = Gtk.Grid(row_spacing=6, column_spacing=6)
                # ▼ wybór locale (dla locale-gen + eselect locale)
        grid.attach(Gtk.Label(label="Locale:"), 0, 0, 1, 1)
        self.locale_combo = Gtk.ComboBoxText()
        # lista kodów w formacie <kod_kraju>, np. "pl_PL", "de_DE", "en_US"
        for code, name in [
            ("pl_PL", "Polski"),
            ("en_US", "English"),
            ("es_ES", "Español"),
            ("fr_FR", "Français"),
            ("it_IT", "Italiano"),
            ("de_DE", "Deutsch"),
            ("pt_BR", "Português (BR)"),
            ("ru_RU", "Русский"),
            ("zh_CN", "简体中文"),
            ("ja_JP", "日本語"),
        ]:
            self.locale_combo.append(code, f"{code} — {name}")
        # domyślnie Polska
        self.locale_combo.set_active_id("pl_PL")
        grid.attach(self.locale_combo,        1, 0, 1, 1)

        grid.attach(Gtk.Label(label="User:"),   0, 1, 1, 1)
        self.user_entry = Gtk.Entry()
        self.user_entry.set_text(getattr(self, "username", ""))
        grid.attach(self.user_entry,            1, 1, 1, 1)

        grid.attach(Gtk.Label(label="march:"),  0, 2, 1, 1)
        self.march_entry = Gtk.Entry(text="native")
        compl_march = Gtk.EntryCompletion()
        store_m = Gtk.ListStore(str)
        for a in march_list:
            store_m.append([a])
        compl_march.set_model(store_m)
        compl_march.set_text_column(0)
        compl_march.set_inline_completion(True)
        compl_march.set_popup_completion(True)
        self.march_entry.set_completion(compl_march)
        grid.attach(self.march_entry, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="mtune:"),  0, 3, 1, 1)
        self.mtune_entry = Gtk.Entry(text="native")
        compl_mtune = Gtk.EntryCompletion()
        store_t = Gtk.ListStore(str)
        for a in mtune_list:
            store_t.append([a])
        compl_mtune.set_model(store_t)
        compl_mtune.set_text_column(0)
        compl_mtune.set_inline_completion(True)
        compl_mtune.set_popup_completion(True)
        self.mtune_entry.set_completion(compl_mtune)
        grid.attach(self.mtune_entry, 1, 3, 1, 1)

        grid.attach(Gtk.Label(label="jobs:"),0, 4, 1, 1)
        self.cor_entry = Gtk.Entry(text=str(multiprocessing.cpu_count()))
        grid.attach(self.cor_entry,             1, 4, 1, 1)

        # GPU checkboxes
        hbox_gpu = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        for label in ("Intel", "Intel Iris", "Nvidia", "AMD"):
            cb = Gtk.CheckButton(label=label)
            setattr(self, f"cb_{label.replace(' ', '').lower()}", cb)
            hbox_gpu.pack_start(cb, False, False, 0)

        # Extras checkboxes
        extras = [
            ("VLC",      "media-video/vlc"),
            ("GPARTED",  "sys-block/gparted"),
            ("STEAM",    "games-util/steam-launcher"),
            ("FIREFOX",  "www-client/firefox"),
            ("CHROMIUM", "www-client/chromium"),
            ("GIMP",     "media-gfx/gimp"),
            ("HTOP",     "sys-process/htop"),
            ("OBS",      "media-video/obs-studio"),
        ]
        grid_extra = Gtk.Grid(row_spacing=6, column_spacing=12)
        self.extra_cbs = {}
        for idx, (label, _pkg) in enumerate(extras):
            cb = Gtk.CheckButton(label=label)
            self.extra_cbs[label] = cb
            col, row = idx % 4, idx // 4
            grid_extra.attach(cb, col, row, 1, 1)

        # Scrolled middle section
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(-1, 280)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        scrolled.add(inner)
        inner.pack_start(grid,       False, False, 0)
        inner.pack_start(hbox_gpu,   False, False, 10)
        inner.pack_start(grid_extra, False, False, 10)
                # ─── Wybór środowiska graficznego ───
        lbl_env = Gtk.Label(i18n.MESSAGES["x_desktop"])
        lbl_env.set_xalign(0)
        inner.pack_start(lbl_env, False, False, 10)

        env_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        inner.pack_start(env_box, False, False, 5)

        self.desktop_env_buttons = []
        first_btn = None
        for env_name in self.DESKTOP_ENVS.keys():
            if first_btn is None:
                # pierwszy przycisk rozpoczyna grupę
                radio_btn = Gtk.RadioButton.new_with_label(None, env_name)
                first_btn = radio_btn
            else:
                # kolejne dołączają do pierwszego
                radio_btn = Gtk.RadioButton.new_with_label_from_widget(first_btn, env_name)
            env_box.pack_start(radio_btn, False, False, 2)
            self.desktop_env_buttons.append(radio_btn)


        # domyślnie zaznacz pierwszy ("Brak (tylko XTerm)")
        self.desktop_env_buttons[0].set_active(True)

        # Install button callback
        def on_install(_):
            # 1) Walidacja pozostałych pól ------------------------------
            if not self.user_entry.get_text().strip():
                return self._error_dialog(i18n.MESSAGES["err_field_required1"])
            if not self.cor_entry.get_text().strip():
                return self._error_dialog(i18n.MESSAGES["err_field_required2"])
            if not self.cor_entry.get_text().isdigit():
                return self._error_dialog(i18n.MESSAGES["err_field_integer"])

            # 2) march / mtune -----------------------------------------
            #   • puste = bezpieczne domyślne
            #   • jeżeli wpisano i nie ma na liście → zapytaj
            m_arch = self.march_entry.get_text().strip() or "x86-64"
            m_tune = self.mtune_entry.get_text().strip() or "generic"

            custom_incorrect = (
                (self.march_entry.get_text().strip() and m_arch not in march_list) or
                (self.mtune_entry.get_text().strip() and m_tune not in mtune_list)
            )
            if custom_incorrect:
                dlg = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.OK_CANCEL,
                    text="Nietypowe ustawienia march/mtune",
                    secondary_text=(
                        f"march = {m_arch}\n"
                        f"mtune = {m_tune}\n\n"
                        "Czy na pewno kontynuować?"
                    )
                )
                if dlg.run() != Gtk.ResponseType.OK:
                    dlg.destroy()
                    return                      # przerwij instalację
                dlg.destroy()

            # 2,5) użyj finalnych wartości --------------------------------
            march = m_arch
            mtune = m_tune

            # 3) Timer instalacji
            self.install_start_time = datetime.now()
            self.timer_label.set_no_show_all(False)
            self.timer_label.show()
            self._start_install_timer()

            # 4) Przechowaj wartości
            self.NASZUSER  = self.user_entry.get_text().lower()
            self.NASZMARCH = march
            self.NASZMTUNE = mtune
            self.NASZCOR   = self.cor_entry.get_text()
            self.LOCALE    = self.locale_combo.get_active_id()
            self.NASZEXTRA = " ".join(
                pkg for lbl, pkg in {
                    "VLC":      "media-video/vlc",
                    "GPARTED":  "sys-block/gparted",
                    "STEAM":    "games-util/steam-launcher",
                    "FIREFOX":  "www-client/firefox",
                    "CHROMIUM": "www-client/chromium",
                    "GIMP":     "media-gfx/gimp",
                    "HTOP":     "sys-process/htop",
                    "OBS":      "media-video/obs-studio",
                }.items()
                if self.extra_cbs[lbl].get_active()
            )
            self.NASZINTEL     = self.cb_intel.get_active()      and "i965"  or ""
            self.NASZINTELIRIS = self.cb_inteliris.get_active()  and "intel" or ""
            self.NASZNVIDIA    = self.cb_nvidia.get_active()     and "nvidia" or ""
            self.NASZAMD       = self.cb_amd.get_active()        and "amd"    or ""

            # 5) Przełącz na widok logu
            self.step_box.foreach(lambda w: self.step_box.remove(w))

            # 6) ScrolledWindow z TextView
            log_sc = Gtk.ScrolledWindow()
            log_sc.set_vexpand(True)
            log_sc.set_min_content_height(200)
            log_sc.set_shadow_type(Gtk.ShadowType.NONE)
            log_sc.set_margin_top(12)
            log_sc.set_margin_bottom(12)

            self.log_view = Gtk.TextView(editable=False, wrap_mode=Gtk.WrapMode.WORD)
            self.log_buf  = self.log_view.get_buffer()
            self.log_view.get_style_context().add_class("transparent-bg")
            log_sc.get_style_context().add_class("transparent-bg")
            try:
                self.log_view.override_background_color(
                    Gtk.StateFlags.NORMAL,
                    Gdk.RGBA(0, 0, 0, 0)
                )
            except Exception:
                pass

            log_sc.add(self.log_view)
            self.step_box.pack_start(log_sc, True, True, 0)

            # ➜ Jeden label pod scrollem: [i/total] pakiet
            self.emerge_output_label = Gtk.Label(label="")
            self.emerge_output_label.set_xalign(0)
            self.emerge_output_label.set_margin_top(6)
            self.step_box.pack_start(self.emerge_output_label, False, False, 5)

            # ➜ Pasek postępu pod labelką
            self.step_box.pack_start(self.progress_bar, False, False, 2)
            # Second progress bar (for files/percent, no label)
            self.substep_bar = Gtk.ProgressBar()
            self.substep_bar.set_margin_top(2)
            self.substep_bar.set_show_text(False)
            self.substep_bar.hide()
            self.step_box.pack_start(self.substep_bar, False, False, 2)

            self.step_box.show_all()

            # 7) Start instalacji w tle
            threading.Thread(target=self.start_installation, daemon=True).start()


        # Outer container: header + scrolled + buttons
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        outer.pack_start(lbl,    False, False, 0)
        outer.pack_start(scrolled, True,  True,  0)

        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_back = Gtk.Button(label=i18n.MESSAGES["btn_back"])
        btn_next = Gtk.Button(label=i18n.MESSAGES["btn_install"])
        btn_back.connect("clicked", self._build_step_root_passwd)
        btn_next.connect("clicked", on_install)
        btn_row.pack_start(btn_back, False, False, 0)
        btn_row.pack_start(btn_next, False, False, 0)
        outer.pack_start(btn_row, False, False, 0)

        # Load everything into the panel
        self.step_box.pack_start(outer, True, True, 0)
        self.step_box.show_all()

    # ——— simple error/info dialog ———
    def _error_dialog(self, msg):
        # Show a message dialog and wait for the user to acknowledge
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=msg
        )
        dialog.run()
        dialog.destroy()

    # ——— find an available terminal emulator ———
    def _pick_terminal(self):
        # Return the first terminal emulator found in PATH
        candidates = [
            "qterminal", "gnome-terminal", "konsole",
            "xfce4-terminal", "lxterminal", "alacritty", "kitty", "xterm" 
        ]
        for cmd in candidates:
            if shutil.which(cmd):
                return cmd
        return None

    def start_installation(self):
        programy = ["net-libs/nodejs",
                    "sys-fs/ntfs3g",
                    "sys-firmware/sof-firmware",
                    "net-wireless/blueman",
                    "app-admin/sudo",
                    "x11-base/xorg-server",
                    "x11-apps/mesa-progs",
                    "media-libs/mesa",
                    "net-misc/networkmanager",
                    "x11-misc/arandr",
                    "net-p2p/qbittorrent",
                    "app-editors/pluma",
                    "media-sound/alsa-utils",
                    "sys-boot/grub"]

        programy.extend(self.NASZEXTRA.split())

        # ─── Add selected desktop environment (if any) ───
        selected_env_name = self.get_selected_desktop_env()
        env_data = self.DESKTOP_ENVS.get(selected_env_name)

        if env_data and env_data["packages"]:
            programy.append(env_data["packages"])

        # Helper: run emerge with autounmask; if it fails with exit code 1,
        # automatically accept changes in etc-update and retry.
        def _auto_emerge(pkgs: str) -> str:
            return (
                f"emerge --autounmask-write --autounmask-backtrack=y {pkgs} || "
                f"(yes | etc-update --automode -3 && emerge {pkgs})"
            )

        steps = [
            (i18n.MESSAGES["step_export_vars"], (
                f'export NASZUSER="{self.NASZUSER}" '
                f'export NASZMARCH="{self.NASZMARCH}" '
                f'export NASZMTUNE="{self.NASZMTUNE}" '
                f'export COR="{self.NASZCOR}" '
                f'export NASZINTEL="{self.NASZINTEL}" '
                f'export NASZNVIDIA="{self.NASZNVIDIA}" '
                f'export NASZAMD="{self.NASZAMD}" '
                f'export NASZINTELIRIS="{self.NASZINTELIRIS}"'
            )),
#            (i18n.MESSAGES["step_config_makeconf_initial"],
 #f"""cat <<'EOF' >/etc/portage/make.conf
# These settings were set by the catalyst build script that automatically
# built this stage.
# Please consult /usr/share/portage/config/make.conf.example for a more
# detailed example.
#COMMON_FLAGS="-O3 -pipe -flto"
#CFLAGS="${{COMMON_FLAGS}}"
#CXXFLAGS="${{COMMON_FLAGS}}"
#FCFLAGS="${{COMMON_FLAGS}}"
#FFLAGS="${{COMMON_FLAGS}}"
#VIDEO_CARDS="{self.NASZINTEL} {self.NASZNVIDIA} {self.NASZAMD} {self.NASZINTELIRIS}"
#MAKEOPTS="-j{self.NASZCOR}"
# NOTE: This stage was built with the bindist USE flag enabled

# This sets the language of build output to English.
# Please keep this setting intact when reporting bugs.
#LC_MESSAGES=C.utf8
#EOF"""
#),
            (i18n.MESSAGES["step_generate_locales"],
 f"""cat <<'EOF'>> /etc/locale.gen
{self.LOCALE}.UTF-8 UTF-8
en_US.UTF-8 UTF-8
EOF"""
),
            (i18n.MESSAGES["step_eselect_locale"], f"locale-gen && eselect locale set {self.LOCALE}.utf8"),
            (i18n.MESSAGES["step_sync_portage"], 'env-update && source /etc/profile && emerge --sync'),
            #(i18n.MESSAGES["step_update_world"], 'env-update && source /etc/profile && emerge --update --deep --newuse @world'),
            (i18n.MESSAGES["step_config_makeconf_final"],
 f"""cat <<'EOF' >/etc/portage/make.conf
CHOST="x86_64-pc-linux-gnu"
COMMON_FLAGS="-march={self.NASZMARCH} -mtune={self.NASZMTUNE} -O3 -pipe -flto"
CFLAGS="${{COMMON_FLAGS}}"
CXXFLAGS="${{COMMON_FLAGS}}"
FCFLAGS="${{COMMON_FLAGS}}"
FFLAGS="${{COMMON_FLAGS}}"
MAKEOPTS="-j{self.NASZCOR}"
VIDEO_CARDS="{self.NASZINTEL} {self.NASZNVIDIA} {self.NASZAMD} {self.NASZINTELIRIS}"
USE="alsa pulseaudio vulkan opengl -systend -gpm"
ACCEPT_LICENSE="*"
ACCEPT_KEYWORDS="~amd64"
LC_MESSAGES="pl_PL.UTF-8"
LINGUAS="pl"
#FEATURES="ccache"
#CCACHE_DIR="$HOME/.ccache"
GENTOO_MIRRORS="http://ftp.vectranet.pl/gentoo/ https://mirror.init7.net/gentoo/"
EOF"""
),
            (i18n.MESSAGES["step_extra_cflags"], f'export EXTRA_CFLAGS="-march={self.NASZMARCH} -mtune={self.NASZMTUNE} -O3 -pipe -flto" && export EXTRA_CXXFLAGS="-march={self.NASZMARCH} -mtune={self.NASZMTUNE} -O3 -pipe -flto"'),
            (i18n.MESSAGES["step_install_kernel"], 'emerge sys-kernel/gentoo-sources sys-kernel/genkernel'),
            (i18n.MESSAGES["step_microcode"],
 f"""cat <<'EOF' >>/etc/genkernel.conf
MICROCODE="intel"
SANDBOX="yes"
MAKEOPTS="$(portageq envvar MAKEOPTS)"
EOF"""
),
            (i18n.MESSAGES["step_link_linux"], 'ln -sf /usr/src/linux-* /usr/src/linux'),
            (i18n.MESSAGES["step_genkernel"], 'genkernel all'),
            (i18n.MESSAGES["step_env_update"], 'env-update && source /etc/profile'),
            (i18n.MESSAGES["step_repo"], 'emerge app-eselect/eselect-repository'),
            (i18n.MESSAGES["step_eselect"], 'eselect repository enable guru steam-overlay'),
            (i18n.MESSAGES["step_sync_overlays"], 'emerge --sync'),
            (i18n.MESSAGES["step_update_world2"], 'env-update && source /etc/profile && emerge --update --deep --newuse @world'),
            (i18n.MESSAGES["step_install_programs"], _auto_emerge(' '.join(programy))),
            (i18n.MESSAGES["step_useradd"], f'useradd -m -G wheel,audio,video,input,tty -s /bin/bash {self.NASZUSER}'),
            (i18n.MESSAGES["step_useradd"],
f"""cat <<'EOF' >> /home/{self.NASZUSER}/.bash_profile
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    sleep 5
    exec startx
fi
EOF"""
),
            (i18n.MESSAGES["step_set_desktop_env"],
f"""cat <<'EOF' >/home/{self.NASZUSER}/.xinitrc
{env_data["start_cmd"]}
EOF"""
            ) if env_data["start_cmd"] else (
            i18n.MESSAGES["step_set_desktop_env_xterm"],
f"""touch /home/{self.NASZUSER}/.xinitrc"""
),
            (i18n.MESSAGES["step_sudoers"],
 f"""cat <<'EOF' >>/etc/sudoers
{self.NASZUSER} ALL=(ALL:ALL) ALL
EOF"""
),
            (i18n.MESSAGES["step_history"],
 f"""cat <<'EOF' >/home/{self.NASZUSER}/.bash_history
sudo env-update && source /etc/profile && sudo emerge --update --deep --newuse @world &&
sudo env-update && source /etc/profile && sudo emerge x11-drivers/xf86-video-intel x11-drivers/nvidia-drivers
sudo nmtui
sudo nano /etc/portage/make.conf
sudo ccache -M 100G
sudo ccache -s
EOF"""
),
            (i18n.MESSAGES["step_history_chown"],
 f"""chown {self.NASZUSER}:{self.NASZUSER} /home/{self.NASZUSER}/.bash_history"""
),
            (i18n.MESSAGES["step_grub_time"],
 f"""cat <<'EOF' >>/etc/default/grub
GRUB_TIMEOUT=0
GRUB_TIMEOUT_STYLE=hidden
EOF"""
),
            (i18n.MESSAGES["step_dbus"], 'rc-update add dbus default'),
            (i18n.MESSAGES["step_networkmanager"], 'rc-update add NetworkManager default'),
            (i18n.MESSAGES["step_autologin"], f'sed -i "s|^c1:.*agetty.*|c1:12345:respawn:/sbin/agetty --noclear -a {self.NASZUSER} 38400 tty1 linux|" /etc/inittab'),
            ( "Install Gentoo Helper",
              "bash /gento_helper/install.sh" ),

]
# --- GRUB installation step -------------------------------------------------

        if self.efi_choice:
            steps.append((i18n.MESSAGES["step_install_grub_uefi"], f'grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=Gentoo && grub-mkconfig -o /boot/grub/grub.cfg'))
        else:
            steps.append((i18n.MESSAGES["step_install_grub_bios"], f'grub-install --target=i386-pc {self.selected_disk} && grub-mkconfig -o /boot/grub/grub.cfg'))
# ---------------------------------------------------------------

        # Which steps should be executed in the external terminal?
        external = {
            #i18n.MESSAGES["step_update_world"],
            i18n.MESSAGES["step_install_kernel"],
            i18n.MESSAGES["step_genkernel"],
            i18n.MESSAGES["step_repo"],
            i18n.MESSAGES["step_update_world2"],
            i18n.MESSAGES["step_install_programs"],
            i18n.MESSAGES["step_set_desktop_env"],  # jeżeli masz też krok "Środowisko LXQT"
            i18n.MESSAGES["step_set_user_passwd"],   # jeżeli chodzi o "Ustawienia" (ustawienie hasła)
            i18n.MESSAGES["step_install_grub_uefi"] if self.efi_choice else         i18n.MESSAGES["step_install_grub_bios"]
        }

        total = len(steps)
        for idx, (label, cmd) in enumerate(steps, 1):
            GLib.idle_add(self.append_log, f"→ {label}")

            full_cmd = ["chroot", "/mnt/gentoo", "/bin/bash", "-lc", cmd]

            GLib.idle_add(self.progress_bar.hide)
            GLib.idle_add(self.substep_bar.hide)
            GLib.idle_add(self.emerge_output_label.set_text, "")

            if 'emerge' in cmd:
                seen_progress = False
                last_i = last_tot = last_pkg = None
                master_fd, slave_fd = pty.openpty()
                proc = subprocess.Popen(
                    full_cmd,
                    stdout=slave_fd, stderr=slave_fd,
                    bufsize=0, text=True
                )
                os.close(slave_fd)

                with os.fdopen(master_fd) as stdout:
                    while True:
                        try:
                            line = stdout.readline()
                            if not line:
                                break
                        except OSError:
                            break
                        # ─── DODAJ TEN FRAGMENT ABY PRZYWRÓCIĆ LOGI W TERMINALU ───
                        if label in external:
                            sys.stdout.write(line)
                            sys.stdout.flush()
                        clean = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)

                        if self.verbose_gui:
                            GLib.idle_add(self.append_log, clean.rstrip('\n'))

                        m2 = re.search(r'>>> (?:Emerging|Installing) \(\s*(\d+)\s+of\s+(\d+)\s*\)\s+([^\s]+)', clean)
                        m1 = re.search(r'\[\s*(\d+)\s*(?:\/|of)\s*(\d+)\s*\]\s+(.+)', clean)
                        m_pct = re.search(r'\[\s*(\d{1,3})\s*%\]\s+(.+)', clean)

                        if m2:
                            cur, tot, full = m2.groups()
                            pkg = full.split("::")[0]
                            pkg = re.sub(r"-\d[0-9._-]*$", "", pkg)
                            last_i, last_tot, last_pkg = cur, tot, pkg
                            frac = int(cur) / int(tot)
                            pct = int(frac * 100)

                            GLib.idle_add(self.progress_bar.set_fraction, frac)
                            GLib.idle_add(self.progress_bar.set_text, f"{pct} %")
                            if not seen_progress:
                                seen_progress = True
                                GLib.idle_add(self.progress_bar.show)

                            GLib.idle_add(
                                self.emerge_output_label.set_text,
                                f"[{cur}/{tot}] {pkg}"
                            )

                        phase_patterns = [
                            (r">>> Unpacking", "Unpacking..."),
                            (r">>> Installing", "Installing..."),
                            (r">>> Completed", "Completed!"),
                            (r">>> Emerging", "Emerging..."),
                            (r"Copying", "Copying..."),
                            (r"checking", "Checking..."),
                        ]

                        for pat, txt in phase_patterns:
                            if re.search(pat, clean):
                                if last_i and last_tot and last_pkg:
                                    GLib.idle_add(
                                        self.emerge_output_label.set_text,
                                        f"[{last_i}/{last_tot}] {last_pkg}  {txt}"
                                    )

                        if m1 or m_pct:
                            GLib.idle_add(self.substep_bar.show)
                            if m1:
                                sub, subtot, _ = m1.groups()
                                GLib.idle_add(self.substep_bar.set_fraction, int(sub) / int(subtot))
                            else:
                                pct, _ = m_pct.groups()
                                GLib.idle_add(self.substep_bar.set_fraction, int(pct) / 100)

                        if ">>> Completed" in clean:
                            GLib.idle_add(self.substep_bar.hide)

                proc.wait()
                GLib.idle_add(self.progress_bar.hide)
                GLib.idle_add(self.substep_bar.hide)
                GLib.idle_add(self.emerge_output_label.set_text, "")

            elif 'genkernel' in cmd:
                genkernel_steps = [
                    "kernel: >> Initializing",
                    "Running 'make mrproper'",
                    "Running 'make oldconfig'",
                    "We are now building Linux kernel",
                    "Compiling",
                    "Installing",
                    "Generating module dependency data",
                    "Compiling out-of-tree module",
                    "Saving config of successful build",
                    "initramfs: >> Initializing",
                    "Appending devices cpio data",
                    "Appending busybox cpio data",
                    "Appending modprobed cpio data",
                    "Deduping cpio data",
                    "Compressing cpio data",
                    "Kernel compiled successfully!"
                ]
                total_genkernel_steps = len(genkernel_steps)
                master_fd, slave_fd = pty.openpty()
                proc = subprocess.Popen(full_cmd, stdout=slave_fd, stderr=slave_fd, bufsize=0, text=True)
                os.close(slave_fd)

                with os.fdopen(master_fd) as stdout:
                    while True:
                        try:
                            line = stdout.readline()
                            if not line:
                                break
                        except OSError:
                            break
                        if label in external:
                            sys.stdout.write(line)
                            sys.stdout.flush()
                        clean = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)
                        for idx2, step in enumerate(genkernel_steps):
                            if step in clean:
                                progress = (idx2 + 1) / total_genkernel_steps
                                pct = int(progress * 100)
                                GLib.idle_add(self.progress_bar.set_fraction, progress)
                                GLib.idle_add(self.progress_bar.set_text, f"{pct} %")
                                GLib.idle_add(self.progress_bar.show)
                                GLib.idle_add(
                                    self.emerge_output_label.set_text,
                                    f"[genkernel] {step}"
                                )
                                break
                proc.wait()
                GLib.idle_add(self.progress_bar.hide)
                GLib.idle_add(self.emerge_output_label.set_text, "")

            else:
                proc = subprocess.run(full_cmd, capture_output=True, text=True)
                if self.verbose_gui:
                    if proc.stdout:
                        for l in proc.stdout.splitlines():
                            GLib.idle_add(self.append_log, l)
                    if proc.stderr:
                        for l in proc.stderr.splitlines():
                            GLib.idle_add(self.append_log, l)

                GLib.idle_add(self.progress_bar.hide)
                GLib.idle_add(self.substep_bar.hide)
                GLib.idle_add(self.emerge_output_label.set_text, "")

            status = "OK" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
            GLib.idle_add(self.append_log, f"✓ {label}: {status}")

        GLib.idle_add(self._stop_install_timer)
        GLib.idle_add(self.append_log, i18n.MESSAGES["install_done_title"])
        GLib.idle_add(self._build_step_user_passwd)

    def get_selected_desktop_env(self):
        for btn in self.desktop_env_buttons:
            if btn.get_active():
                return btn.get_label()
        return i18n.MESSAGES["env_none"]

    # --------------------  GTK callback -------------------- #
    def _after_gparted(self, _pid, _status):
        self.partitioned = True
        self.btn_next.set_sensitive(True)

    # ------------------------------------------------------------------ #
    def append_log(self, text: str):
        """Appends a line to the log window and scrolls to the bottom."""
        end_iter = self.log_buf.get_end_iter()
        self.log_buf.insert(end_iter, text + "\n")
        self.log_view.scroll_mark_onscreen(self.log_buf.get_insert())

    def _start_install_timer(self):
        from datetime import datetime
        self.timer_running = True  # <-- uruchamiamy timer

        def update_timer():
            if not getattr(self, "timer_running", True):
                return False  # Przestań aktualizować timer

            if not hasattr(self, "install_start_time") or self.install_start_time is None:
                return False
            delta = datetime.now() - self.install_start_time
            days = delta.days
            hours, rem = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            self.timer_label.set_text(
                f"{days} day{'s' if days != 1 else ''}  {hours} hour{'s' if hours != 1 else ''}\n"
                f"{minutes} min  {seconds} sec"
            )
            return True  # Kontynuuj aktualizację

        GLib.timeout_add_seconds(1, update_timer)
        update_timer()

    def _stop_install_timer(self):
        self.timer_running = False
        if hasattr(self, "install_start_time") and self.install_start_time is not None:
            from datetime import datetime
            delta = datetime.now() - self.install_start_time
            days = delta.days
            hours, rem = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            self.timer_label.set_text(
                f"{days} day{'s' if days != 1 else ''}  {hours} hour{'s' if hours != 1 else ''}\n"
                f"{minutes} min  {seconds} sec"
            )

