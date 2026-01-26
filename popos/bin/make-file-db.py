#!/bin/env python3

import pandas as pd
import subprocess
import hashlib
import click
import os

from multiprocessing.pool import Pool, ThreadPool
from functools import partial
from datetime import datetime
from pathlib import Path

DEFAULT_OUT = Path(os.environ["HOME"]).joinpath(".cache", "allfiles.sqlite.db").absolute()

@click.command()
@click.option("-t", "--tag", default=datetime.now().isoformat(), help="Tag")
@click.option("-e", "--if-exists", default='fail', help='if db already exists: fail|replace|append, default fail')
@click.option("-o", "--db-file", default=str(DEFAULT_OUT), help=f'outfile ({DEFAULT_OUT})')
@click.option("-v", "--verbose", default=False, is_flag=True, help=f'be verbose')
@click.argument("path", default='.')
def cli(tag: str, if_exists: str, db_file: str, verbose: bool, path: str, ):
    if Path(db_file).exists and if_exists == 'fail':
        raise ValueError(f"{db_file} already exists")

    print(f"start scanning files in {path} ...")

    files = [f for f in Path(path).glob("**/*") if f.exists() and f.is_file() and not f.is_socket()]
    df = pd.DataFrame(
        ThreadPool().map(
            partial(get_file_info, tag=tag, verbose=verbose), 
            [f for f in files]
        )
    )

    #print(df)
    df.to_sql(name='files', con=f'sqlite:///{db_file}', if_exists=if_exists, index=False)
    print(f"saved result to {db_file}")

def get_file_info(f, tag, verbose):
    if verbose: print(str(f))
    try:
        return {
            "tag": str(tag),
            "file": str(f.name),
            "path": str(f.absolute().parent), 
            "size": int(f.stat().st_size),
            "created": datetime.fromtimestamp(f.stat().st_ctime),
            "hash": hashfile(str(f)),
        }
    except Exception as e:
        print(e)
        return {
            "tag": str(tag),
            "file": str(f.name),
            "path": str(f.absolute().parent),
        }


def hashfile(file):
    try:
        fhash = subprocess.run(['sha256sum', str(file), '-bz'], stdout=subprocess.PIPE)
        if fhash.returncode != 0: return None
        
        fhash = fhash.stdout.decode('utf-8').split(" ")[0]
        
        #print(fhash)
        return fhash
    except Exception as e:
        print(e)
        return None

def _hashfile(file):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    try:
        with open(file, 'rb') as f:         
            while True:
                data = f.read(BUF_SIZE)
                if not data: break
                sha256.update(data)
    
        return sha256.hexdigest()
    except Exception as e:
        print(e)
        return None
    

if __name__ == '__main__':
    cli()
