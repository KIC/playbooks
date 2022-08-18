# playbooks
run playbooks locally with arguments 

```bash
ansibple-playbook basis.yaml -K --extra-vars "_token_=geheim"
```

if not running on localhost:
```bash
ansibple-playbook basis.yaml -kK --extra-vars "_host_=loalhost _token_=geheim"
```

