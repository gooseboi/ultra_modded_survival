from pathlib import Path
import sys
import pytoml
import os


def has_side(fpath, toml):
    if 'side' not in toml:
        print(f'WARN: file {fpath} has no side attribute')


def good_filename(fpath, toml):
    filename = toml['filename']
    if not filename.endswith('.jar') and not filename.endswith('.zip'):
        print(f'WARN: file {fpath} has invalid filename {filename}')


def check_metafile(fpath: Path):
    with open(fpath, 'r') as f:
        obj = pytoml.load(f)

    has_side(fpath, obj)
    good_filename(fpath, obj)


if __name__ == '__main__':
    this = sys.argv[0]
    dirname = os.path.dirname(this)
    if dirname:
        os.chdir(dirname)

    pack_dir = Path('..')
    pack_toml = pack_dir / 'pack.toml'
    with open(pack_toml, 'r') as f:
        obj = pytoml.load(f)

    index_toml = pack_dir / obj['index']['file']
    with open(index_toml, 'r') as f:
        obj = pytoml.load(f)

    files = obj['files']
    for f in files:
        if not f['metafile']:
            print(f'Skipping checking {f['file']}, not a metafile')
            continue

        fpath = pack_dir / f['file']
        check_metafile(fpath)
