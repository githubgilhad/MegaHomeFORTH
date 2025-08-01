#!/usr/bin/python -u
# vim: fileencoding=utf-8:nomodified:nowrap:textwidth=0:foldmethod=marker:foldcolumn=4:ruler:showcmd:lcs=tab\:|- list:tabstop=8:noexpandtab:nosmarttab:softtabstop=0:shiftwidth=0

import string

base_x = 100
base_y = 50
dx = 5
dy = 2

for col, letter in enumerate(string.ascii_uppercase[:12]):	# A–L
	for row in range(8):
		name = f"P{letter}{row}"
		x = base_x + col * dx
		y = base_y + row * dy
		print(f'''	(global_label "{name}" (shape input) (at  {x} {y} 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left))) ''')

