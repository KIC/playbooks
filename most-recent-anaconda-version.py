#!/bin/python

import os
import pandas as pd

df = pd.read_html("https://repo.anaconda.com/archive/")[0].set_index("Last Modified").sort_index()
url = "https://repo.anaconda.com/archive/" + df[df["Filename"].str.contains("inux") & df["Filename"].str.contains("x86") & df["Filename"].str.contains("64")].iloc[-1, 0]
os.system(f"""wget -c --read-timeout=5 --tries=0 "{url}" -O /tmp/Anaconda3-Linux-x86_64.sh """)
