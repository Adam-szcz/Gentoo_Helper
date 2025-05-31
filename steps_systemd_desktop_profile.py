# steps_systemd_desktop_profile.py
# Definition of the installation steps sequence for a **systemd** Stage3 Desktop profile
# Gentoo 23.0 desktop profile already selected in the Stage3 tarball.

from i18n import MESSAGES


def get_systemd_steps(wizard, env_data, programy):
    """Return list[(label, command)] for a systemd install.

    Mirrors the OpenRC variant but swaps only init‑specific parts and
    makes sure a rootless X session works out‑of‑the‑box.
    """

    steps = [
        (
            f"{MESSAGES['step_export_vars']}  [systemd]",  # ← etykieta kroku
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
EOF"""),
        (MESSAGES["step_eselect_locale"],
         f"locale-gen && eselect locale set {wizard.LOCALE}.utf8"),

        # ── 3. First sync ──────────────────────────────────────────────────
        (MESSAGES["step_sync_portage"],
         'env-update && source /etc/profile && emerge --sync'),

        # ── 4. make.conf tuned for systemd + X ─────────────────────────────
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
INPUT_DEVICES="libinput"
USE="alsa pulseaudio vulkan opengl systemd udev dbus -gpm"
ACCEPT_LICENSE="*"
ACCEPT_KEYWORDS="~amd64"
LC_MESSAGES="pl_PL.UTF-8"
LINGUAS="pl"
GENTOO_MIRRORS="http://ftp.vectranet.pl/gentoo/ https://mirror.init7.net/gentoo/"
EOF"""),

        # ── 5. Extra C*FLAGS env for packages built outside emerge ────────
        (MESSAGES["step_extra_cflags"],
         f"export EXTRA_CFLAGS=\"-march={wizard.NASZMARCH} -mtune={wizard.NASZMTUNE} -O3 -pipe -flto\" && "
         f"export EXTRA_CXXFLAGS=\"-march={wizard.NASZMARCH} -mtune={wizard.NASZMTUNE} -O3 -pipe -flto\""),

        # ── 6. Kernel & genkernel ─────────────────────────────────────────
        (MESSAGES["step_install_kernel"],
         'emerge sys-kernel/gentoo-sources sys-kernel/genkernel'),
        (MESSAGES["step_microcode"],
         """cat <<'EOF' >>/etc/genkernel.conf
MICROCODE="intel"
SANDBOX="yes"
MAKEOPTS="$(portageq envvar MAKEOPTS)"
EOF"""),
        (MESSAGES["step_link_linux"], 'ln -sf /usr/src/linux-* /usr/src/linux'),
        (MESSAGES["step_genkernel"],   'genkernel all'),
        (MESSAGES["step_env_update"],  'env-update && source /etc/profile'),

        # ── 7. Portage overlays & @world update ───────────────────────────
        (MESSAGES["step_repo"],          'emerge app-eselect/eselect-repository'),
        (MESSAGES["step_eselect"],       'eselect repository enable guru steam-overlay'),
        (MESSAGES["step_sync_overlays"], 'emerge --sync'),
        (MESSAGES["step_update_world2"], 'env-update && source /etc/profile && emerge --update --deep --newuse @world'),

        # ── 8. Xorg metapackages ──────────────────────────────────────────
        ("Install Xorg", 'emerge --noreplace x11-base/xorg-drivers x11-base/xorg-server x11-apps/xinit xterm'),

        # ── 9. Extra user software (unchanged) ────────────────────────────
        (MESSAGES["step_install_programs"],
 lambda: wizard._auto_emerge(' '.join(programy)) if False else wizard._auto_emerge(' '.join(programy))
),

        # ── 10. User & autostart ──────────────────────────────────────────
#        (MESSAGES["step_useradd"], f'useradd -m -G wheel,audio,video,input,tty -s /bin/bash {wizard.NASZUSER}'),
#        (MESSAGES["step_autostart_x"], f"""cat <<'EOF' >> /home/{wizard.NASZUSER}/.bash_profile
#if [ -z \"$DISPLAY\" ] && [ \"$(tty)\" = \"/dev/tty1\" ]; then
#    exec startx
#fi
#EOF"""),
        *([(
                MESSAGES["step_set_desktop_env"],
                f"""cat <<'EOF' >/home/{wizard.NASZUSER}/.xinitrc
{env_data['start_cmd']}
EOF"""
        )] if env_data.get("start_cmd") else []),

        # ── 11. Sudoers & history ─────────────────────────────────────────
        (MESSAGES["step_sudoers"], f"""echo '{wizard.NASZUSER} ALL=(ALL:ALL) ALL' >> /etc/sudoers"""),
        (MESSAGES["step_history"], f"touch /home/{wizard.NASZUSER}/.bash_history && chown {wizard.NASZUSER}:{wizard.NASZUSER} /home/{wizard.NASZUSER}/.bash_history"),

        # ── 12. GRUB tweak (timeout) ──────────────────────────────────────
        (MESSAGES["step_grub_time"], "sed -i 's/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT=0/' /etc/default/grub"),

        # ── 13. Enable core services ─────────────────────────────────────
        (MESSAGES["step_dbus"],           'systemctl enable --now dbus-broker.socket'),
        (MESSAGES["step_networkmanager"], 'systemctl enable --now NetworkManager.service'),

        # ── 14. Autologin drop‑in with runtime‑dir + xorg dirs ────────────
        (MESSAGES["step_autologin"], f"""mkdir -p /etc/systemd/system/getty@tty1.service.d && cat <<'EOF' >/etc/systemd/system/getty@tty1.service.d/autologin.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin {wizard.NASZUSER} --noclear %I $TERM
EOF
systemctl daemon-reload && systemctl restart getty@tty1
"""),
        # ── 15. Gentoo Helper script -------------------------------------
        ("Install Gentoo Helper", 'bash /gento_helper/install.sh'),
    ]

    # ── 16. i915 work‑arounds (optional) ─────────────────────────────────
    steps.append(("Add i915 kernel params", "sed -i 's@^GRUB_CMDLINE_LINUX=\"@&i915.enable_psr=0 i915.enable_dp_mst=0 video=DP-2:d @' /etc/default/grub && grub-mkconfig -o /boot/grub/grub.cfg"))

    # ── 17. GRUB install step (EFI/BIOS) ---------------------------------
    if wizard.efi_choice:
        steps.append((MESSAGES["step_install_grub_uefi"],
                      'grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=Gentoo && grub-mkconfig -o /boot/grub/grub.cfg'))
    else:
        steps.append((MESSAGES["step_install_grub_bios"],
                      f'grub-install --target=i386-pc {wizard.selected_disk} && grub-mkconfig -o /boot/grub/grub.cfg'))

    return steps
