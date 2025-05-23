#!/bin/bash
set -e

# Katalog instalacyjny
DEST="/opt/Gento_Helper"

# Tworzenie katalogu
sudo mkdir -p "$DEST"
sudo cp -r assets languages prog disk_utils.py main.py wizard.py "$DEST/"

# PolicyKit
sudo cp com.gento.helper.policy /usr/share/polkit-1/actions/

# Skrót .desktop
sudo cp GentooHelper.desktop /usr/share/applications/
# ---------- ikona + drugi skrót uruchamiający pakietowy interfejs ----------
sudo install -Dm644 assets/splashicon.png /usr/share/pixmaps/gento-helper.png

cat <<'EOF' | sudo tee /usr/share/applications/GentooHelperInstaller.desktop >/dev/null
[Desktop Entry]
Type=Application
Name=Gento Helper Installer
Comment=Gentoo Helper – zarządzaj pakietami po instalacji
Exec=python3 /opt/Gento_Helper/prog/main.py
Icon=gento-helper
Terminal=false
Categories=System;
EOF

sudo gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true

echo "Zainstalowano Gentoo Helper!"
echo "Znajdziesz program w menu aplikacji lub przez wyszukiwanie: Gentoo Helper"
