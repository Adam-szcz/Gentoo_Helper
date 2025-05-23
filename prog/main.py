#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
if not Gtk.init_check()[0]:    # ← dodaj tę linijkę
    raise SystemExit("Gtk init failed — brak DISPLAY?")
from gui_main import GentooHelperApp

def main():
    # Utworzenie i wyświetlenie głównego okna
    app = GentooHelperApp()
    app.show_all()
    # Start pętli GTK
    Gtk.main()

if __name__ == "__main__":
    main()

