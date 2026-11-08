Name:       harbour-hydroxide
Version:    1.0.2
Release:    0
Summary:    Local Proton Mail bridge (IMAP/SMTP) for Sailfish OS, with CAPTCHA support
License:    MIT
URL:        https://github.com/DanteCpp/hydroxide
Group:      Applications/Internet
Source0:    hydroxide
Source1:    hydroxide.service

Requires:   systemd-user-session-targets

# Prebuilt static Go binary: skip debuginfo, stripping and dependency scanning.
%global debug_package %{nil}
%global __os_install_post %{nil}
AutoReqProv: no

%description
Hydroxide provides a local IMAP/SMTP bridge for Proton Mail by communicating
with Proton's API. This build includes human verification (CAPTCHA) support
and installs a systemd user-session service.

The bridge listens only on localhost (127.0.0.1).

%prep
# nothing to unpack

%build
# binary package only

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/usr/lib/systemd/user/user-session.target.wants
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/hydroxide
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/user/hydroxide.service
ln -s ../hydroxide.service \
    %{buildroot}/usr/lib/systemd/user/user-session.target.wants/hydroxide.service

%post
# Best effort: the user manager may not be available during install.
USER_NAME=""
if id defaultuser >/dev/null 2>&1; then
    USER_NAME="defaultuser"
elif id nemo >/dev/null 2>&1; then
    USER_NAME="nemo"
fi

if [ -n "$USER_NAME" ]; then
    su - "$USER_NAME" -c 'systemctl --user daemon-reload >/dev/null 2>&1 || :'
    su - "$USER_NAME" -c 'systemctl --user start hydroxide.service >/dev/null 2>&1 || :'
    # On upgrade, a running service keeps the old binary until restarted.
    if [ "$1" -ge 2 ]; then
        su - "$USER_NAME" -c 'systemctl --user try-restart hydroxide.service >/dev/null 2>&1 || :'
    fi
fi

%preun
if [ "$1" -eq 0 ]; then
    USER_NAME=""
    if id defaultuser >/dev/null 2>&1; then
        USER_NAME="defaultuser"
    elif id nemo >/dev/null 2>&1; then
        USER_NAME="nemo"
    fi

    if [ -n "$USER_NAME" ]; then
        su - "$USER_NAME" -c 'systemctl --user stop hydroxide.service >/dev/null 2>&1 || :'
    fi
fi

%postun
USER_NAME=""
if id defaultuser >/dev/null 2>&1; then
    USER_NAME="defaultuser"
elif id nemo >/dev/null 2>&1; then
    USER_NAME="nemo"
fi

if [ -n "$USER_NAME" ]; then
    su - "$USER_NAME" -c 'systemctl --user daemon-reload >/dev/null 2>&1 || :'
fi

%files
%{_bindir}/hydroxide
/usr/lib/systemd/user/hydroxide.service
/usr/lib/systemd/user/user-session.target.wants/hydroxide.service
