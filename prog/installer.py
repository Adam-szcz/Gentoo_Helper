#!/usr/bin/env python3
import gi, subprocess, threading, multiprocessing, re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import os
# –– włącz ciemny motyw, jeśli temat na to pozwala
settings = Gtk.Settings.get_default()
if settings is not None:                       # działa tylko, gdy DISPLAY jest aktywny
    settings.set_property("gtk-application-prefer-dark-theme", True)
class Installer:
    def __init__(self, parent_window):
        self.parent = parent_window

    def validate_password(self, pwd, result_queue):
        proc = subprocess.run(
            ["sudo", "-kS", "true"],
            input=f"{pwd}\n", text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        result_queue.put(proc.returncode == 0)

    def prompt_password(self, max_attempts=3):
        for attempt in range(1, max_attempts + 1):
            subprocess.run(["sudo", "-k"], stderr=subprocess.DEVNULL)
            dlg = Gtk.Dialog(
                title="Podaj hasło roota",
                parent=self.parent,
                modal=True
            )
            dlg.set_default_size(350, 120)
            dlg.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
            dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
            content = dlg.get_content_area()
            instr = Gtk.Label(label=f"Próba {attempt}/{max_attempts}: Podaj hasło administratora")
            instr.set_xalign(0)
            entry = Gtk.Entry(visibility=False)
            entry.set_placeholder_text("Hasło")
            status = Gtk.Label(label="")
            status.set_xalign(0)
            for w in (instr, entry, status):
                content.add(w); w.show()
            dlg.set_default_response(Gtk.ResponseType.OK)
            entry.connect("activate", lambda w: dlg.response(Gtk.ResponseType.OK))
            if dlg.run() != Gtk.ResponseType.OK:
                dlg.destroy(); return None
            pwd = entry.get_text(); status.set_text("Poczekaj…"); entry.set_sensitive(False)
            for b in dlg.get_action_area().get_children(): b.set_sensitive(False)
            while Gtk.events_pending(): Gtk.main_iteration()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=self.validate_password, args=(pwd,q))
            p.start(); p.join(); dlg.destroy()
            if q.get(): return pwd
        return None

    def run_with_progress(self, cmd, password, on_update, on_finish, on_error):
        def worker():
            # 1) jeśli jesteśmy już rootem (np. w chroocie), pomijamy sudo
            if os.geteuid() == 0:
                full_cmd = cmd
            else:
                # 2) inaczej próbujemy sudo bez pytania, a gdy nie, to z -S
                try:
                    ok = subprocess.run(
                        ["sudo", "-n", "true"],
                        stderr=subprocess.DEVNULL
                    ).returncode == 0
                except FileNotFoundError:
                    ok = False
                if ok:
                    full_cmd = ["sudo"] + cmd
                else:
                    full_cmd = ["sudo", "-S"] + cmd

            # 3) odpalamy proces i przekazujemy output do GUI
            proc = subprocess.Popen(
                full_cmd,
                stdin=subprocess.PIPE   if (password and not os.geteuid()==0) else None,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            if password and not os.geteuid()==0:
                proc.stdin.write(password + "\n")
                proc.stdin.flush()

            for line in proc.stdout:
                GLib.idle_add(on_update, line.rstrip("\n"))
            ret = proc.wait()
            GLib.idle_add(on_finish if ret == 0 else lambda: on_error(f"Proces zakończył się z kodem {ret}"))

        threading.Thread(target=worker, daemon=True).start()


    def install_packages(self, pkgs):
        # jeśli nie ma zaznaczonych pakietów, od razu komunikat
        if not pkgs:
            self.parent.show_info("Nie zaznaczono żadnego pakietu.")
            return
        # pomijamy ‛emerge --sync’: od razu wysyłamy do emerge
        self._next_pkgs = []
        self.install_packages_with_args(pkgs, [])


    def uninstall_packages(self, pkgs):
        self.install_packages_with_args(pkgs, ["-C"])

    def depclean_packages(self):
        self.install_packages_with_args([], ["--depclean"])

    def world_update(self, flags):
            """
            Wrapper na emerge @world: flagi to lista stringów
            np. ["--update","--deep","--newuse"].
            """
            # po prostu przekażemy do install_packages_with_args pakiet @world
            return self.install_packages_with_args(
                [ "@world" ],  # traktujemy @world jak zwykły atom
                flags          # przekazujemy wybrane flagi
            )

    def install_packages_with_args(self, pkgs, extra_args):
        # reset następnej listy pakietów, żeby nie pętlić po finish
        self._next_pkgs   = []
        self._last_output = []
        # detect uninstall mode
        is_uninstall = "-C" in extra_args
        # detect sync mode (emerge --sync bez pakietów)
        is_sync = "--sync" in extra_args and not pkgs
        sync_frac = 0.0; sync_dir = 1
        if os.geteuid() == 0:
            pwd = None
        else:
            # spróbuj sudo bez hasła
            try:
                ok = subprocess.run(
                    ["sudo","-n","true"],
                    stderr=subprocess.DEVNULL
                ).returncode == 0
            except FileNotFoundError:
                ok = False

            if ok:
                pwd = None
            else:
                pwd = self.prompt_password()
                if pwd is None:
                    return

        dlg = Gtk.Dialog(title="Operacja na pakietach", parent=self.parent, modal=True)
        dlg.set_default_size(500, 240)
        dlg.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        dlg.get_content_area().add(vbox)

        # Progress widgets
        progress    = Gtk.ProgressBar();  vbox.pack_start(progress,False,False,5)
        pkg_label   = Gtk.Label(label=""); vbox.pack_start(pkg_label,False,False,5)
        # secondary file-level progress (hidden until Compiling + [n/m] detected)
        file_progress = Gtk.ProgressBar()
        file_progress.set_show_text(True)
        file_progress.hide()
        vbox.pack_start(file_progress, False, False, 5)
        phase_label = Gtk.Label(label=""); vbox.pack_start(phase_label,False,False,5)
        # Label for current package (atom), always shown under compile progress
        current_pkg_label = Gtk.Label(label="")
        vbox.pack_start(current_pkg_label, False, False, 5)
        dlg.show_all()

        # define phases
        phases = ["Unpacking source","Compiling","Testing","Installing","Running postinst"]
        current_idx=0; current_tot=0; current_phase_idx=0; file_frac=0.0; file_dir=1

        def on_update(line):
            self._last_output.append(line)
            nonlocal current_idx, current_tot, current_phase_idx, file_frac, file_dir, sync_frac, sync_dir
            pkg = ""
            # 1) schowaj zawsze file_progress na wejściu
            file_progress.hide()

            # 2) wykryj fazę emerge
            m_ph = re.search(
                r">>> (Unpacking source|Compiling|Testing|Installing|Running postinst)",
                line
            ) 
            if m_ph:
                phase = m_ph.group(1)
                current_phase_idx = phases.index(phase)
                phase_label.set_text(phase)

            # 3) wykryj postęp pakietowy (install vs. uninstall)
            if is_uninstall:
                m_pkg = re.search(
                    r">>> Unmerging\s*\((\d+) of (\d+)\)\s+(.+)",
                    line
                )
            else:
                m_pkg = re.search(
                    r">>> (?:Emerging|Installing)\s*\((\d+) of (\d+)\)\s+(.+)",
                    line
                )
            if m_pkg:
                idx, tot, pkg = m_pkg.groups()
                current_idx, current_tot = int(idx), int(tot)
                # Update only the current package atom label
                current_pkg_label.set_text(pkg)

            # jeśli jeszcze nie mamy liczby pakietów, nic nie rób
            if current_tot == 0:
                return False

            # 4) zawsze pokazuj file_progress w fazie Compiling i pulsuj, gdy brak [n/m]
            m_file = re.search(r"\[(\d+)\s*/\s*(\d+)\]", line)
            if current_phase_idx == 1:
                file_progress.show()
                if m_file:
                    f_idx, f_tot = map(int, m_file.groups())
                    file_frac = f_idx / f_tot
                else:
                    # symulacja aktywności: zwiększ/zmniejsz fraction
                    file_frac += 0.02 * file_dir
                    if file_frac >= 1.0:
                        file_frac = 1.0
                        file_dir = -1
                    elif file_frac <= 0.0:
                        file_frac = 0.0
                        file_dir = 1
                file_progress.set_fraction(file_frac)

            # 5) oblicz główny ułamek paska: segment = (phase+1)/#phases
            ph_frac = (current_phase_idx + 1) / len(phases)
            frac = ((current_idx - 1) + ph_frac) / current_tot
            progress.set_fraction(frac)

            # 6) aktualizuj etykietę
            action = "Unmerging" if is_uninstall else "Installing"
            label = f"[{current_idx}/{current_tot}] {action} {pkg}"
            if current_phase_idx == 1 and m_file:
                label += f" ({f_idx}/{f_tot})"
            pkg_label.set_text(label)

            return False

        def on_finish():
            progress.set_fraction(1.0)
            success=Gtk.MessageDialog(parent=self.parent,modal=True,
                message_type=Gtk.MessageType.INFO,text="Operacja zakończona pomyślnie.")
            success.add_button(Gtk.STOCK_OK,Gtk.ResponseType.OK)
            if success.run()==Gtk.ResponseType.OK:
                success.destroy(); dlg.destroy(); GLib.idle_add(self.parent.populate_package_list)
            if self._next_pkgs:
               self.install_packages_with_args(self._next_pkgs, [])
            return False

        def on_error(msg):
            # zbierz cały output emerge
            full = "\n".join(self._last_output).lower()

            # 1) autounmask tylko przy odpowiednim błędzie
            if ("perhaps you need --autounmask-write" in full
                or "use changes are necessary to proceed" in full):
                pkg = pkgs[0]
                # zrób autounmask
                subprocess.run(["emerge", "--autounmask-write", pkg], check=False)
                subprocess.run("yes | etc-update --automode -3",
                               shell=True, check=False)

                # zresetuj log i pasek postępu
                self._last_output.clear()
                progress.set_fraction(0.0)
                status_label.set_text(f"Autounmask i ponowna instalacja {pkg}…")

                # kontynuuj w tym samym dialogu
                self.run_with_progress(
                    ["emerge"] + extra_args + pkgs,
                    pwd, on_update, on_finish, on_error
                )
                return False

            # 2) jeżeli jest build.log → pokaż je i zamknij dialog
            logs = re.findall(r'(/var/tmp/portage/\S+/temp/build\.log)', full)
            if logs:
                dlg.destroy()
                log_path = logs[-1]
                # ... reszta Twojego kodu pokazywania build.log ...
                return False

            # 3) w pozostałych przypadkach – zamknij dialog i pokaż błąd
            dlg.destroy()
            Gtk.MessageDialog(
                parent=self.parent,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                text=msg
            ).run()
            GLib.idle_add(self.parent.populate_package_list)
            return False


        self.run_with_progress(["emerge"]+extra_args+pkgs,pwd,on_update,on_finish,on_error)
        dlg.connect("response",lambda d,r: dlg.destroy() if r==Gtk.ResponseType.CANCEL else None)

    def sync_tree(self, next_pkgs=None):
        """
        Synchronizuje drzewo Portage (emerge --sync) z animowanym paskiem postępu,
        a po zakończeniu – jeśli przekazano listę pakietów – rusza instalację.
        """

        # zapamiętaj, co ma być zainstalowane po syncu
        self._next_pkgs = next_pkgs or []

        # przygotuj output i – jeżeli nie jesteśmy rootem – ewentualne sudo
        self._last_output = []
        if os.geteuid() == 0:
            # już rootem (w chroocie): nie używamy sudo
            pwd = None
        else:
            # spróbuj sudo bez hasła
            try:
                ok = subprocess.run(
                    ["sudo", "-n", "true"],
                    stderr=subprocess.DEVNULL
                ).returncode == 0
            except FileNotFoundError:
                ok = False

            if ok:
                pwd = None
            else:
                pwd = self.prompt_password()
                if pwd is None:
                    Gtk.MessageDialog(
                        parent=self.parent, modal=True,
                        message_type=Gtk.MessageType.ERROR,
                        text="3 błędne próby logowania. Program zostanie zamknięty."
                    ).run()
                    Gtk.main_quit()
                    return


        # dialog sync
        dlg = Gtk.Dialog(title="Synchronizacja Portage", parent=self.parent, modal=True)
        dlg.set_default_size(500, 240)
        dlg.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        dlg.get_content_area().add(vbox)

        progress = Gtk.ProgressBar()
        vbox.pack_start(progress, False, False, 5)
        status_label = Gtk.Label(label="Synchronizacja – proszę czekać…")
        vbox.pack_start(status_label, False, False, 5)
        dlg.show_all()

        # tylko pulsowanie
        is_sync = True
        sync_frac = 0.0
        sync_dir = 1

        def on_update(line):
            nonlocal sync_frac, sync_dir
            self._last_output.append(line)

            # pulsuj pasek
            sync_frac += 0.03 * sync_dir
            if sync_frac >= 1.0:
                sync_frac = 1.0; sync_dir = -1
            elif sync_frac <= 0.0:
                sync_frac = 0.0; sync_dir = 1
            progress.set_fraction(sync_frac)
            return False

        def on_finish():
            progress.set_fraction(1.0)
            status_label.set_text("Synchronizacja zakończona. Zamknę okno za 3 s…")

            def close_and_continue():
                dlg.destroy()
                if self._next_pkgs:
                    self.install_packages_with_args(self._next_pkgs, [])
                return False

            GLib.timeout_add_seconds(3, close_and_continue)
            return False
        def on_error(msg):
            dlg.destroy()
            Gtk.MessageDialog(
                parent=self.parent, modal=True,
                message_type=Gtk.MessageType.ERROR,
                text=f"Synchronizacja nie powiodła się: {msg}"
            ).run()
            return False

        # i wywołaj:
        self.run_with_progress(["emerge","--sync"], pwd, on_update, on_finish, on_error)
        dlg.connect("response", lambda d,r: dlg.destroy() if r==Gtk.ResponseType.CANCEL else None)
