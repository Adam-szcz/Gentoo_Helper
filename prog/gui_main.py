#!/usr/bin/env python3
import gi, shutil, subprocess
from installer import Installer
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
if not Gtk.init_check()[0]:    # ← dodaj tę linijkę
    raise SystemExit("Gtk init failed — brak DISPLAY?")
class GentooHelperApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gentoo Helper")
        self.set_default_size(800, 600)
        self.set_resizable(True)
        self.connect("destroy", Gtk.main_quit)

        self.installer = Installer(self)

        # Search/filter entry
        search = Gtk.SearchEntry()
        search.set_placeholder_text("Filtruj pakiety…")
        search.connect("search-changed", self.on_search_changed)

        # Main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        vbox.pack_start(search, False, False, 5)

        header = Gtk.Label(label="Gentoo Helper – wybierz pakiety do instalacji")
        vbox.pack_start(header, False, False, 5)

        # Package list store: [selected, atom, versions, is_installed]
        self.pkg_store = Gtk.ListStore(bool, str, str, bool)
        self.search_text = ""
        self.filter = self.pkg_store.filter_new()
        self.filter.set_visible_func(self._filter_func, None)

        # TreeView setup
        tree = Gtk.TreeView(model=self.filter)
        # Toggle column
        toggle = Gtk.CellRendererToggle()
        toggle.connect("toggled", self.on_toggle)
        tree.append_column(Gtk.TreeViewColumn("", toggle, active=0))
        # Package name
        name_col = Gtk.TreeViewColumn("Nazwa pakietu", Gtk.CellRendererText(), text=1)
        tree.append_column(name_col)
        # Version column
        ver_renderer = Gtk.CellRendererText()
        ver_col = Gtk.TreeViewColumn(
            "Wersja (zainstalowana / dostępna)", ver_renderer, text=2
        )
        ver_col.set_cell_data_func(ver_renderer, self._color_cell)
        tree.append_column(ver_col)

        # Scrolled package list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.add(tree)
        vbox.pack_start(scrolled, True, True, 5)

        # Bottom buttons container
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(bottom_box, False, False, 5)

        # po scrollu z listą pakietów, przed bottom_box
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(sep, False, False, 5)

        # skrzynka na wybór operacji world
        world_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(world_box, False, False, 5)

        label = Gtk.Label(label="World update:")
        world_box.pack_start(label, False, False, 5)

        self.world_combo = Gtk.ComboBoxText()
        # opcja domyślna – brak dodatkowej operacji
        self.world_combo.append_text("Brak")
        # przykładowe warianty
        self.world_combo.append_text("--update --deep --newuse @world")
        self.world_combo.append_text("--update --newuse --with-bdeps=y @world")
        self.world_combo.append_text("--sync")
        self.world_combo.append_text("@preserved-rebuild")

        self.world_combo.set_active(0)
        world_box.pack_start(self.world_combo, False, False, 5)

        # Install button
        install_btn = Gtk.Button(label="Install selected")
        install_btn.connect("clicked", self.on_install_clicked)
        bottom_box.pack_start(install_btn, True, True, 5)

        # Uninstall button
        uninstall_btn = Gtk.Button(label="Uninstall selected")
        uninstall_btn.connect("clicked", self.on_uninstall_clicked)
        bottom_box.pack_start(uninstall_btn, True, True, 5)

        # Populate initial list
        if not shutil.which("eix"):
            self.ask_install_eix()
        else:
            # — pierwsze uruchomienie w chroocie: zbuduj bazę EIX
            subprocess.run(["eix-update"], check=False)
            self.populate_package_list()


    def _filter_func(self, model, iter, data):
        return self.search_text in model[iter][1].lower()

    def on_search_changed(self, entry):
        self.search_text = entry.get_text().lower()
        self.filter.refilter()

    def on_toggle(self, widget, path):
        itr = self.filter.get_iter(Gtk.TreePath(path))
        real = self.filter.convert_iter_to_child_iter(itr)
        self.pkg_store[real][0] = not self.pkg_store[real][0]

    def _color_cell(self, column, cell, model, iter, data):
        cell.set_property("foreground", "green" if model[iter][3] else None)

    def populate_package_list(self):
        try:
            out_all = subprocess.check_output([
                "eix", "--format", "<category>/<name>:<bestversion:NAMEVERSION>\n"
            ], text=True, stderr=subprocess.DEVNULL)
            out_inst = subprocess.check_output([
                "eix", "-I", "--format", "<category>/<name>:<installedversions:NAMEVERSION>\n"
            ], text=True, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            return self.show_error(f"Błąd pobierania wersji: {e}")

        all_map = {l.split(':',1)[0]: l.split(':',1)[1].strip()
                   for l in out_all.splitlines() if ':' in l}
        inst_map = {l.split(':',1)[0]: l.split(':',1)[1].strip()
                    for l in out_inst.splitlines() if ':' in l}

        self.pkg_store.clear()
        for atom in sorted(all_map):
            inst = inst_map.get(atom, "")
            versions = f"{inst or '-'} / {all_map[atom]}"
            self.pkg_store.append([False, atom, versions, bool(inst)])

    def ask_install_eix(self):
        dlg = Gtk.MessageDialog(
            parent=self, modal=True, destroy_with_parent=True,
            message_type=Gtk.MessageType.WARNING,
            text="This GUI requires the app-portage/eix program. Run the program in the terminal!"
        )
        dlg.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        if dlg.run() == Gtk.ResponseType.OK:
            subprocess.run(["emerge", "app-portage/eix"], check=False)
            if os.path.exists("/usr/bin/eix-update"):
                subprocess.run(["/usr/bin/eix-update"], check=False)
            else:
                print("The file /usr/bin/eix-update is missing – the eix installation may have failed.")
            dlg.destroy()
            self.populate_package_list()
        else:
            dlg.destroy()



    def show_error(self, msg):
        Gtk.MessageDialog(
            parent=self, modal=True, destroy_with_parent=True,
            message_type=Gtk.MessageType.ERROR, text=msg
        ).run()

    def show_info(self, msg):
        dlg = Gtk.MessageDialog(
            parent=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=msg
        )
        dlg.run()
        dlg.destroy()

    def get_selected_packages(self):
        return [row[1] for row in self.pkg_store if row[0]]

    def get_selected_installed_packages(self):
        return [row[1] for row in self.pkg_store if row[0] and row[3]]

    def on_install_clicked(self, button):
        choice = self.world_combo.get_active_text()
        if choice == "--sync":
           self.installer.sync_tree()
        elif choice != "Brak":
           flags = choice.split()
           self.installer.world_update(flags)
        else:
           pkgs = self.get_selected_packages()
           if not pkgs:
               self.show_info("No package has been selected.")
               return
           self.installer.install_packages(pkgs)

    def on_uninstall_clicked(self, button):
        pkgs = self.get_selected_installed_packages()
        if pkgs:
            self.installer.uninstall_packages(pkgs)
        else:
            self.installer.depclean_packages()

