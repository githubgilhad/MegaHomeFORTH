#!/usr/bin/python -u
# vim: fileencoding=utf-8:nomodified:nowrap:textwidth=0:foldmethod=marker:foldcolumn=4:ruler:showcmd:lcs=tab\:|- list:tabstop=8:noexpandtab:nosmarttab:softtabstop=0:shiftwidth=0
#!/usr/bin/env python3
import sys
import re

ESC = '\x1b'
csi_g_re = re.compile(r'\x1b\[([0-9]+)G')

def process_line(line):
    out = []
    col = 1  # terminálové sloupce jsou 1-based
    i = 0

    while i < len(line):
        if line[i] == ESC and line[i:i+2] == ESC + '[':
            m = csi_g_re.match(line, i)
            if m:
                target = int(m.group(1))
                if target > col:
                    spaces = target - col
                    out.append(' ' * spaces)
                    col = target
                else:
                    out.append('\t')
                i = m.end()
                continue
        ch = line[i]
        out.append(ch)
        if ch == '\n':
            col = 1
        elif ch == '\r':
            col = 1
        elif ch == '\t':
            tab = 8 - ((col - 1) % 8)
            col += tab
        else:
            col += 1
        i += 1

    return ''.join(out)

def main():
    for line in sys.stdin:
        sys.stdout.write(process_line(line))

if __name__ == "__main__":
    main()

