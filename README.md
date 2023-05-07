# playbooks
run playbooks locally with arguments 

```bash
# install ansible
sudo apt install ansible

# install general purpose basis software, disable ipv6, disable spectre, etc
ansible-playbook basis.yaml -K

# restart
shutdown -r now

# install development tools
ansible-playbook development.yaml -K --extra-vars "_token_=geheim"


```

if not running on localhost:
```bash
ansible-playbook basis.yaml -kK --extra-vars "_host_=localhost"
```

