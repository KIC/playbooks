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

if not running on localhost:
```bash
ansible-playbook basis.yaml -kK --extra-vars "_host_=localhost"
```

## Ather config
 * privoxy add mail.google.com under the {fragile} tag in /etc/privoxy/user.action
   then add privoxy as http and https proxy to system network settings on port 8118
   test if everything works by browsing to http:/p.p/


## Other software
 * Obsidian Notes: https://obsidian.md/download
 * Huawai Tehming Studio: https://developer.huawei.com/consumer/en/doc/Tools-Library/theme_download-0000001050424897
 * --13ft ladder: https://github.com/wasi-master/13ft--
   * https://gitlab.com/adamkb263/bypass-paywalls-chrome-clean
 * Realtime Speech to Text: https://github.com/KoljaB/RealtimeSTT


# Optimizations
 * firefox: make use less cpu: https://www.makeuseof.com/how-to-reduce-firefox-cpu-usage/

# Notes on Installed software
## pipx
if we install jupyter-lab with pipx we get isolated servers where we can have different version of pandas and co.
If an application installed by pipx requires additional packages, you can add them with pipx inject. For example, 
if you have ipython installed and want to add the matplotlib package to it, you would use:

`pipx inject ipython matplotlib`


