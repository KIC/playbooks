# playbooks
run playbooks locally with arguments 

```bash
# install ansible
sudo apt install ansible

# install general purpose basis software, disable ipv6, disable spectre, etc
ansible-playbook basis.yaml -K


```

if not running on localhost:
```bash
ansible-playbook basis.yaml -kK --extra-vars "_host_=loalhost _token_=geheim"
```

