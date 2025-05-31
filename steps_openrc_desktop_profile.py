# steps_openrc_desktop_profile.py
# Definition of the installation steps sequence for OpenRC Desktop Profile

from i18n import MESSAGES

# Returns a list of steps (label, cmd) to be executed during an OpenRC Desktop Profile installation
def get_openrc_steps(wizard, env_data, programy):
    steps = [
        (
            f"{MESSAGES['step_export_vars']}  [OpenRC]",   # ← etykieta kroku
            (
                f'export NASZUSER="{wizard.NASZUSER}" '
                f'export NASZMARCH="{wizard.NASZMARCH}" '
                f'export NASZMTUNE="{wizard.NASZMTUNE}" '
                f'export COR="{wizard.NASZCOR}" '
                f'export NASZINTEL="{wizard.NASZINTEL}" '
                f'export NASZNVIDIA="{wizard.NASZNVIDIA}" '
                f'export NASZAMD="{wizard.NASZAMD}" '
                f'export NASZINTELIRIS="{wizard.NASZINTELIRIS}"'
            )
        ),
        (MESSAGES["step_generate_locales"],
         f"""cat <<'EOF'>> /etc/locale.gen
{wizard.LOCALE}.UTF-8 UTF-8
en_US.UTF-8 UTF-8
EOF"""
        ),
        (MESSAGES["step_eselect_locale"],
         f"locale-gen && eselect locale set {wizard.LOCALE}.utf8"
        ),
        (MESSAGES["step_sync_portage"],
         'env-update && source /etc/profile && emerge --sync'
        ),
        (MESSAGES["step_config_makeconf_final"],
         f"""cat <<'EOF' >/etc/portage/make.conf
CHOST="x86_64-pc-linux-gnu"
COMMON_FLAGS="-march={wizard.NASZMARCH} -mtune={wizard.NASZMTUNE} -O3 -pipe -flto"
CFLAGS="${{COMMON_FLAGS}}"
CXXFLAGS="${{COMMON_FLAGS}}"
FCFLAGS="${{COMMON_FLAGS}}"
FFLAGS="${{COMMON_FLAGS}}"
MAKEOPTS="-j{wizard.NASZCOR}"
VIDEO_CARDS="{wizard.NASZINTEL} {wizard.NASZNVIDIA} {wizard.NASZAMD} {wizard.NASZINTELIRIS}"
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
        (MESSAGES["step_extra_cflags"],
         f"export EXTRA_CFLAGS=\"-march={wizard.NASZMARCH} -mtune={wizard.NASZMTUNE} -O3 -pipe -flto\" && \
export EXTRA_CXXFLAGS=\"-march={wizard.NASZMARCH} -mtune={wizard.NASZMTUNE} -O3 -pipe -flto\""
        ),
        (MESSAGES["step_install_kernel"],
         'emerge sys-kernel/gentoo-sources sys-kernel/genkernel'
        ),
        (MESSAGES["step_microcode"],
         f"""cat <<'EOF' >>/etc/genkernel.conf
MICROCODE="intel"
SANDBOX="yes"
MAKEOPTS="$(portageq envvar MAKEOPTS)"
EOF"""
        ),
        (MESSAGES["step_link_linux"],
         'ln -sf /usr/src/linux-* /usr/src/linux'
        ),
        (MESSAGES["step_genkernel"], 'genkernel all'),
        (MESSAGES["step_env_update"], 'env-update && source /etc/profile'),
        (MESSAGES["step_repo"], 'emerge app-eselect/eselect-repository'),
        (MESSAGES["step_eselect"], 'eselect repository enable guru steam-overlay'),
        (MESSAGES["step_sync_overlays"], 'emerge --sync'),
        (MESSAGES["step_update_world2"],
         'env-update && source /etc/profile && emerge --update --deep --newuse @world'
        ),
        (MESSAGES["step_install_programs"], wizard._auto_emerge(' '.join(programy))),
        (MESSAGES["step_useradd"],
         f'useradd -m -G wheel,audio,video,input,tty -s /bin/bash {wizard.NASZUSER}'
        ),
        (MESSAGES["step_autostart_x"],
         f"""cat <<'EOF' >> /home/{wizard.NASZUSER}/.bash_profile
if [ -z \"$DISPLAY\" ] && [ \"$(tty)\" = \"/dev/tty1\" ]; then
    sleep 5
    exec startx
fi
EOF"""
        ),
        # .xinitrc tylko gdy jest start_cmd
        *([
            (
                MESSAGES["step_set_desktop_env"],
                f"""cat <<'EOF' >/home/{wizard.NASZUSER}/.xinitrc
{env_data["start_cmd"]}
EOF"""
            ),
        ] if env_data["start_cmd"] else []),
        (MESSAGES["step_sudoers"],
         f"""cat <<'EOF' >>/etc/sudoers
{wizard.NASZUSER} ALL=(ALL:ALL) ALL
EOF"""
        ),
        (MESSAGES["step_history"],
         f"""cat <<'EOF' >/home/{wizard.NASZUSER}/.bash_history
sudo env-update && source /etc/profile && sudo emerge --update --deep --newuse @world &&
sudo env-update && source /etc/profile && sudo emerge x11-drivers/xf86-video-intel x11-drivers/nvidia-drivers
sudo nmtui
sudo nano /etc/portage/make.conf
sudo ccache -M 100G
sudo ccache -s
EOF"""
        ),
        (MESSAGES["step_history_chown"],
         f"chown {wizard.NASZUSER}:{wizard.NASZUSER} /home/{wizard.NASZUSER}/.bash_history"
        ),
        (MESSAGES["step_grub_time"],
         f"""cat <<'EOF' >>/etc/default/grub
GRUB_TIMEOUT=0
GRUB_TIMEOUT_STYLE=hidden
EOF"""
        ),
        (MESSAGES["step_dbus"], 'rc-update add dbus default'),
        (MESSAGES["step_networkmanager"], 'rc-update add NetworkManager default'),
        (MESSAGES["step_autologin"],
         f'sed -i "s|^c1:.*agetty.*|c1:12345:respawn:/sbin/agetty --noclear -a {wizard.NASZUSER} 38400 tty1 linux|" /etc/inittab'
        ),
        ("Install Gentoo Helper",
         'bash /gento_helper/install.sh'
        ),
    ]

    # --- EFI / BIOS → GRUB step appended dynamically (same logic as OpenRC) ---
    if wizard.efi_choice:
        steps.append((MESSAGES["step_install_grub_uefi"],
                       'grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=Gentoo && grub-mkconfig -o /boot/grub/grub.cfg'))
    else:
        steps.append((MESSAGES["step_install_grub_bios"],
                       f'grub-install --target=i386-pc {wizard.selected_disk} && grub-mkconfig -o /boot/grub/grub.cfg'))

    return steps

