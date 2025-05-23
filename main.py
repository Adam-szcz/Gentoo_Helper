#!/usr/bin/env python3
"""
main.py
--------
Entry point for Gentoo Helper installer.
Shows a splash screen, then launches the setup wizard.
"""

# ——— Standard library ———
import os
import signal
import subprocess
import sys

# ——— Third-party ———
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

# ——— Local modules ———
from wizard import SetupWizardWindow

# ── włączamy globalnie dymki tool-tipów ──
settings = Gtk.Settings.get_default()
if settings is not None:
    settings.set_property("gtk-enable-tooltips", True)


class SplashScreen(Gtk.Window):
    """
    Simple splash screen that closes on click or Enter key
    and then calls the provided callback.
    """
    def __init__(self, image_path: str, on_continue):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        img = Gtk.Image.new_from_file(image_path)
        self.add(img)

        # Close on Enter key
        self.connect("key-press-event", self._on_key)
        # Close on mouse click
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self._on_click)

        self._on_continue = on_continue
        self.show_all()

    def _on_key(self, _widget, event):
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            self.destroy()
            self._on_continue()

    def _on_click(self, _widget, _event):
        self.destroy()
        self._on_continue()


def main():
    """
    Set up signal handlers to unmount Gentoo mounts on exit,
    then show splash and launch the setup wizard.
    """
    def quit_gracefully(_signum=None, _frame=None):
        # Unmount /mnt/gentoo/boot and /mnt/gentoo if mounted
        for mount_point in ("/mnt/gentoo/boot", "/mnt/gentoo"):
            if os.path.ismount(mount_point):
                subprocess.call(
                    ["umount", "-l", mount_point],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        Gtk.main_quit()

    # Handle SIGHUP, SIGINT, SIGTERM
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGHUP,  quit_gracefully)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT,  quit_gracefully)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, quit_gracefully)

    def start_wizard():
        # Launch the installer wizard
        win = SetupWizardWindow()
        win.connect("destroy", quit_gracefully)
        win.show_all()

    # Show splash, then wizard
    ASSET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/splash.png")
    SplashScreen(ASSET_PATH, start_wizard)
    Gtk.main()


if __name__ == "__main__":
    # Must run as root
    if os.geteuid() != 0:
        print("Please run as root (sudo)", file=sys.stderr)
        sys.exit(1)
    main()
