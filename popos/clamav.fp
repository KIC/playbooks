sigtool --md5 /usr/share/nmap/scripts/http-vuln-cve2012-1823.nse | sudo tee -a /var/lib/clamav/false-positives.fp
sigtool --md5 /usr/local/maldetect/sigs.old/rfxn.yara | sudo tee -a /var/lib/clamav/false-positives.fp
sigtool --md5 /usr/local/maldetect/clean/gzbase64.inject.unclassed | sudo tee -a /var/lib/clamav/false-positives.fp
sigtool --md5 /usr/local/maldetect/sigs/rfxn.yara | sudo tee -a /var/lib/clamav/false-positives.fp
sigtool --md5 /var/lib/clamav/rfxn.yara | sudo tee -a /var/lib/clamav/false-positives.fp

