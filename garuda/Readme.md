## Requiremets

1. First install needed packages: `sudo pacman -S vim ansible uv visual-studio-code-bin`
1. Then add localhost as default host
`sudo mkdir -p /etc/ansible && echo "localhost ansible_connection=local" | sudo tee -a /etc/ansible/hosts`
1. install ansible requiremnts: `ansible-galaxy collection install -r requirements.yaml`
1. run playbooks like `ansible-playbook basis.yaml -K`
1. list added timers: `sudo systemctl list-timers`


### Security
After installing the security tools dont forget to regularly fix vulnerabilities `sudo lynis audit system`.
Also look into `/var/log/lynis.log`


### Kernel Tunning

#### Custom Kernel Build
check local version `uname -r`
check remote version:
`curl -s "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=linux-cachyos" | grep '^_minor'`

#### Boot Params
Edit /etc/default/grub and append your kernel options between the quotes in the GRUB_CMDLINE_LINUX_DEFAULT line:
> GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"

##### Intel
Kernel Params: `mitigatons=off intel_pstate=active amd_iommu=off i915.enable_rc6=1 i915.enable_psr=1 i915.enable_fbc=1`

##### AMD GPU
Kenel Params:
* amdgpu.gttsize=<full ram capacity in bytes>
* ttm.pages_limit=<Calculate as (desired_bytes / 4096); for example, to match 16 GB VRAM/GTT: 16 * 1024 * 1024 * 1024 / 4096 = 4194304. Scale to 75-90% of total system RAM or VRAM on AMD APUs (e.g., Strix Halo, MI300A) for unified memory—use 134217728 for 512 GB across devices.>
* amdttm.page_pool_size=<same value as above>
You can use something like: `lsmem -b --summary=only | sed -ne '/online/s/.* //p'`

And then automatically re-generate the grub.cfg file with:
> # grub-mkconfig -o /boot/grub/grub.cfg


### Unbund Hardening
Here is what each setting in your Unbound configuration does, in plain language. [redhat](https://www.redhat.com/en/blog/forwarding-dns-2)

***

#### Interfaces and access control

- `interface: 0.0.0.0`  
  Listen for DNS queries on all IPv4 addresses on this machine (every IPv4 interface). [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `interface: ::0`  
  Listen for DNS queries on all IPv6 addresses on this machine (every IPv6 interface). [redhat](https://www.redhat.com/en/blog/forwarding-dns-2)

- `access-control: 192.168.42.0/24 allow`  
  Allow clients in the IPv4 subnet 192.168.42.0–192.168.42.255 to use this resolver. [docs.redhat](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/managing_networking_infrastructure_services/assembly_setting-up-an-unbound-dns-server_networking-infrastructure-services)

- `access-control: 127.0.0.0 allow`  
  Allow queries from localhost (loopback). Typically this is written as `127.0.0.0/8 allow`, meaning 127.0.0.0–127.255.255.255. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `access-control: 2001:db8:dead:beef::/48 allow`  
  Allow clients in this IPv6 prefix to query the resolver. [docs.redhat](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/managing_networking_infrastructure_services/assembly_setting-up-an-unbound-dns-server_networking-infrastructure-services)

These `access-control` lines together define which networks are permitted to use your DNS server and will be refused by default from others if not explicitly allowed. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

***

#### Performance / optimisation settings

These tune how many threads Unbound uses and how it caches and buffers data. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `num-threads: 4`  
  Run Unbound with 4 worker threads, letting it process multiple queries in parallel on multi‑core CPUs. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `msg-cache-slabs: 16`  
  Split the message cache (stores full DNS replies) into 16 separate “slabs” to reduce lock contention in multithreaded operation; must be a power of two. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `rrset-cache-slabs: 16`  
  Split the RRset cache (stores resource record sets, e.g. all A records for a name) into 16 slabs for the same reason. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `infra-cache-slabs: 16`  
  Split the infrastructure cache (stores info about upstream servers like RTT, failures) into 16 slabs to scale better with threads. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `key-cache-slabs: 16`  
  Split the DNSSEC key cache into 16 slabs, again improving concurrency with several threads. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `outgoing-range: 206`  
  Limit the number of simultaneous outstanding upstream queries per thread (i.e. parallel lookups Unbound can have in flight). [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `so-rcvbuf: 4m`  
  Set the kernel socket receive buffer size to 4 megabytes for Unbound’s sockets, helping with bursts of traffic. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `so-sndbuf: 4m`  
  Set the socket send buffer size to 4 megabytes, allowing larger or more numerous responses to queue efficiently. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `so-reuseport: yes`  
  Allow multiple threads/processes to bind to the same UDP/TCP port, improving parallelism and load distribution on multicore systems. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `rrset-cache-size: 100m`  
  Allocate roughly 100 MB of memory for the RRset cache (resource record sets). [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `msg-cache-size: 50m`  
  Allocate roughly 50 MB of memory for the message cache (full DNS responses). [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

***

#### Protocol and transport settings

These control which IP families and transports Unbound uses. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `do-ip4: yes`  
  Enable sending and answering DNS queries over IPv4. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `do-ip6: yes`  
  Enable sending and answering DNS queries over IPv6. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `do-udp: yes`  
  Enable UDP transport for DNS queries (the normal/default for DNS). [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `do-tcp: yes`  
  Enable TCP transport for DNS queries (used for large replies, DNSSEC, and fall‑back when UDP fails). [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

***

#### Caching behaviour and privacy

These control how long results are cached and what information the server exposes. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `cache-max-ttl: 86400`  
  Cap the maximum time (TTL) that Unbound will keep records in cache to 86 400 seconds (24 hours), even if upstream TTLs are higher. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `cache-min-ttl: 3600`  
  Enforce a minimum TTL of 3 600 seconds (1 hour) for positive answers, so commonly used records stick around at least that long. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `hide-identity: yes`  
  Do not answer special queries (like `id.server` or `hostname.bind`) that reveal this server’s identity/hostname. [github](https://github.com/dnstap/unbound/blob/master/doc/example.conf.in)

- `hide-version: yes`  
  Do not answer special queries (like `version.bind`) that reveal the Unbound version. [github](https://github.com/dnstap/unbound/blob/master/doc/example.conf.in)

- `minimal-responses: yes`  
  Only include the data strictly required in answers (no extra records), reducing bandwidth and information leakage. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `prefetch: yes`  
  When cached entries near expiry are queried, refresh them proactively in the background so future queries are faster. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `use-caps-for-id: yes`  
  Enable “0x20” case randomization: Unbound randomizes uppercase/lowercase in query names to add entropy as an extra anti‑spoofing measure. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `verbosity: 1`  
  Set logging verbosity to a low (but not silent) level; mainly errors plus minimal info are logged. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

***

#### Hardening / security

These options improve protection against some DNS attacks and ensure validation. [manpages.ubuntu](https://manpages.ubuntu.com/manpages/xenial/man5/unbound.conf.5.html)

- `harden-glue: yes`  
  Be strict about glue records in referrals, ignoring glue that does not match the zone being delegated to prevent cache poisoning. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `harden-dnssec-stripped: yes`  
  Detect and reject answers where DNSSEC data appears to have been stripped when it should be present, protecting against downgrade attacks. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

***

#### Root hints and local/private zones

These configure how Unbound finds the DNS root and how it treats internal addresses and names. [github](https://github.com/dnstap/unbound/blob/master/doc/example.conf.in)

- `root-hints: "/var/lib/unbound/root.hints"`  
  Use the specified file as the list of root DNS servers (root hints) which Unbound uses to start recursive resolution. [github](https://github.com/dnstap/unbound/blob/master/doc/example.conf.in)

- `private-domain: "company.lan"`  
  Treat `company.lan` as a private/internal domain; this suppresses certain DNSSEC or DNS‑over‑public‑Internet behaviours that do not make sense for internal names and can prevent leakage. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `private-address: 192.168.42.0/24`  
  Mark this IPv4 subnet as containing private addresses so Unbound will not, for example, send these in upstream responses or treat them as public routable space. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

- `private-address: 2001:db8:dead:beef::/48`  
  Same as above, but for the internal IPv6 prefix. [wiki.ircnow](https://wiki.ircnow.org/index.php?n=Unbound.LAN)

***

#### Local static records

These create fixed DNS records served directly by Unbound, without querying upstream. [docs.opnsense](https://docs.opnsense.org/manual/unbound.html)

- `local-data: "server.company.lan. IN A 192.168.42.254"`  
  Define a static A record: `server.company.lan` resolves to IPv4 address 192.168.42.254. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `local-data-ptr: "192.168.42.254 server.company.lan"`  
  Define the corresponding reverse (PTR) record so that a lookup of 192.168.42.254 returns `server.company.lan`. [docs.opnsense](https://docs.opnsense.org/manual/unbound.html)

- `local-data: "server.company.lan. IN AAAA 2001:db8:dead:beef::254"`  
  Define a static AAAA record: `server.company.lan` resolves to IPv6 address 2001:db8:dead:beef::254. [unbound.docs.nlnetlabs](https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html)

- `local-data-ptr: "2001:db8:dead:beef::254 server.company.lan"`  
  Define the reverse PTR for that IPv6 address, mapping it back to `server.company.lan`. [docs.opnsense](https://docs.opnsense.org/manual/unbound.html)

If you want, paste any other Unbound options you are considering and I can tell you how they interact with this setup and whether they are sensible for a small LAN resolver.
