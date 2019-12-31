#!/usr/bin/env python3
import sys
from pathlib import Path

md_exec = Path(sys.argv[0]).resolve()
if (md_exec.parent / 'macrodeck').is_dir():
	sys.path.insert(0, str(md_exec.parent))

from macrodeck import macrodeck

if __name__ == '__main__':
	sys.exit(macrodeck.main())
