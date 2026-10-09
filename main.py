#!/usr/bin/env python3
"""Dry-run-first file organizer. Moves only regular non-symlink root files."""
import argparse
import json
from pathlib import Path
import shutil

GROUPS = {
    'Images': {'.jpg', '.png', '.jpeg', '.svg', '.ico', '.gif', '.webp', '.heic'},
    'Docs': {'.txt', '.docx', '.doc', '.pdf', '.md', '.xlsx', '.csv', '.pptx'},
    'Media': {'.mp3', '.mp4', '.ogg', '.flv', '.mkv', '.wav', '.mov'},
    'Archives': {'.zip', '.gz', '.7z', '.rar', '.tar'},
    'Code': {'.asm', '.c', '.cpp', '.css', '.html', '.js', '.json', '.py', '.xml', '.php', '.rb', '.ts', '.tsx', '.jsx', '.yml', '.yaml'},
}

def category(name):
    ext = Path(name).suffix.lower()
    return next((group for group, extensions in GROUPS.items() if ext in extensions), 'Others')

def plan(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Choose a directory')
    reserved = set()
    result = []
    for source in sorted(root.iterdir()):
        if source.is_symlink() or not source.is_file() or source.name.startswith('.') or source.resolve() == Path(__file__).resolve():
            continue
        folder = root / category(source.name)
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            raise ValueError(f'Unsafe destination folder: {folder.name}')
        target = folder / source.name
        index = 1
        while target.exists() or target.is_symlink() or target in reserved:
            target = folder / f'{source.stem} ({index}){source.suffix}'
            index += 1
        reserved.add(target)
        result.append((source, target))
    return result

def apply(moves):
    for source, target in moves:
        if source.is_symlink() or not source.is_file() or target.parent.is_symlink():
            raise ValueError('Source or destination changed; stop and review again')
        target.parent.mkdir(exist_ok=True)
        # Exclusive creation: never replace an existing file, including races.
        created = False
        try:
            with target.open('xb') as out:
                created = True
                with source.open('rb') as inp:
                    shutil.copyfileobj(inp, out)
            shutil.copystat(source, target, follow_symlinks=False)
            source.unlink()
        except Exception:
            if created:
                target.unlink(missing_ok=True)
            raise

def cli():
    parser = argparse.ArgumentParser(description='Preview file organization. Back up files before --apply.')
    parser.add_argument('directory', help='Directory containing files to organize')
    parser.add_argument('--apply', action='store_true', help='Apply the displayed moves; default is preview only')
    args = parser.parse_args()
    try:
        moves = plan(args.directory)
        print(json.dumps([{'from': str(s), 'to': str(t)} for s, t in moves], indent=2))
        if args.apply:
            apply(moves)
            print(f'Organized {len(moves)} files.')
        else:
            print('Dry run only. No files changed. Review and back up before --apply.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')

if __name__ == '__main__':
    cli()
