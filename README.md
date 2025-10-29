# playbooks
run playbooks locally with arguments 

```bash
## install ansible
sudo apt install ansible

## install general purpose basis software, disable ipv6, disable spectre, etc
ansible-playbook basis.yaml -K

## restart
shutdown -r now

## install development tools
ansible-playbook development.yaml -K --extra-vars "_token_=geheim"

```

## install custom kernel
Note that the playbook installs the custom kernel as an optional boot entry and
you have 3 seconds to select it manually on boot. If the kernel works as expected
you can make it the default and kernelstub managed by executing the tags

`sudo ansible-playbook custom-kernel.yaml --tags "make-default" --extra-vars "when=true"`


if not running on localhost:
```bash
ansible-playbook basis.yaml -kK --extra-vars "_host_=localhost"
```

Later, ask AI if there is something we could adopt from Zen/liquorix kernel


## Multiple Screen with different/fractional scaling
currently only possible with wayland and breezy desktop


## Ather config
 * privoxy add mail.google.com under the {fragile} tag in /etc/privoxy/user.action
   then add privoxy as http and https proxy to system network settings on port 8118
   test if everything works by browsing to http://p.p/
   follow the ad blocking list: https://github.com/Andrwe/privoxy-blocklist


## Other software
 * Obsidian Notes: https://obsidian.md/download
 * Huawai Tehming Studio: https://developer.huawei.com/consumer/en/doc/Tools-Library/theme_download-0000001050424897
 * --13ft ladder: https://github.com/wasi-master/13ft--
   * https://gitlab.com/adamkb263/bypass-paywalls-chrome-clean
 * Realtime Speech to Text: https://github.com/KoljaB/RealtimeSTT
 * popsicle to make bootable USB drives

# Optimizations
 * firefox: make use less cpu: https://www.makeuseof.com/how-to-reduce-firefox-cpu-usage/

# Notes on Installed software
## pipx
if we install jupyter-lab with pipx we get isolated servers where we can have different version of pandas and co.
If an application installed by pipx requires additional packages, you can add them with pipx inject. For example, 
if you have ipython installed and want to add the matplotlib package to it, you would use:

`pipx inject ipython matplotlib`

# Add to playbook later
* battop https://github.com/svartalf/rust-battop/releases
* onlyoffice from flathub https://flathub.org/apps/org.onlyoffice.desktopeditors


# Wayland
* enable wayland in gdm conf: `sudo nano /etc/gdm3/custom.conf`
  - `WaylandEnable=true`
* then disable gdm rules for auto disabling nvidia `sudo ln -s /dev/null /etc/udev/rules.d/61-gdm.rules`
* add kernel boot parameter `nvidia-drm.modeset=1`

Like create a seperate boot entry:
* Copy the existing loader entry from `/boot/efi/loader/entries/Pop_OS-current.conf` to a new file, e.g. `/boot/efi/loader/entries/Pop_OS-nvidia-modeset.conf`
* Edit the new .conf file to add or modify the kernel command line to include nvidia-drm.modeset=1 in the options line.
* On boot, systemd-boot will show both entries. You can select the new one to boot with the NVIDIA modeset option enabled.

# Nvidia Test
snap install gpu-burn

# Pipewire
check for problems in the log `journalctl --user-unit=pipewire -f` change the pipewire default.quantum parameters
```
sudo mkdir -p /etc/pipewire
sudo cp /usr/share/pipewire/*.conf /etc/pipewire/
sudo vim /etc/pipewire/pipewire.conf
```

then change / uncomment
```
default.clock.quantum = 2048
default.clock.min-quantum = 1024
default.clock.max-quantum = 4096
```
