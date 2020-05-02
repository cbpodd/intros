#!/usr/bin/env python3

import json
import sys
import os

ACADEMICS = 'academics'
PROFESSIONAL = 'professional'
PERSONAL = 'personal'
PURPOSE = 'purpose'
LINKS = 'links'
TYPES = [ ACADEMICS, PROFESSIONAL, PERSONAL, PURPOSE ]

MICROSOFT = 'microsoft'
LINKEDIN = 'linkedin'
GENERAL = 'general'
OUTPUTS = { MICROSOFT, LINKEDIN, GENERAL }

CONTENT = 'content'

IN_DIR = 'data'
OUT_DIR = 'build'

SRC_FILE = 'intros.json'
OUT_TYPE = '.md'

def main():
    with open(os.path.join(IN_DIR, SRC_FILE)) as f:
        data = json.load(f)

        output = dict()
        for name in OUTPUTS:
            output[name] = ''

        for t in TYPES:
            part = data[t]
            content = data[t][CONTENT]
            for name in OUTPUTS:
                if name in part:
                    i = part[name]
                    content = part[CONTENT][i]
                    output[name] += content

        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        for out in output:
            with open(os.path.join(OUT_DIR, (out + OUT_TYPE)), 'w') as out_file:
                lines = [ '# ', out.title(), '\n\n', output[out] ]
                out_file.writelines(lines)
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
