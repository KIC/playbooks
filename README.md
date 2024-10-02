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


## Other software
 * Obsidian Notes: https://obsidian.md/download
 * Huawai Tehming Studio: https://developer.huawei.com/consumer/en/doc/Tools-Library/theme_download-0000001050424897
 * 13ft ladder: https://github.com/wasi-master/13ft
 * Realtime Speech to Text: https://github.com/KoljaB/RealtimeSTT


# Optimizations
 * firefox: make use less cpu: https://www.makeuseof.com/how-to-reduce-firefox-cpu-usage/
