#!/usr/bin/python -u
# vim: fileencoding=utf-8:nomodified:nowrap:textwidth=0:foldmethod=marker:foldcolumn=4:ruler:showcmd:lcs=tab\:|- list:tabstop=8:noexpandtab:nosmarttab:softtabstop=0:shiftwidth=0

import string
import yaml

labels = []
base_x = 100
base_y = 50
dx = 5
dy = 2

name='MHF_001.kicad_sch'

for col, letter in enumerate(string.ascii_uppercase[:12]):	# A-L
	for row in range(8):
		label = {
			'symbol_text': {
				'value': f'P{letter}{row}',
				'at': [base_x + col * dx, base_y + row * dy, 0],
				'effects': {
					'font': {'size': [1.27, 1.27]}
				},
				'stroke': {
					'width': 0.15
				},
				'shape': 'label'
			}
		}
		labels.append(label)

# Vložení do existujícího .kicad_sch:
with open(name, 'r') as f:
	sch = yaml.safe_load(f)

# Najdi vhodné místo ve stromu
# POZOR: přizpůsob si dle struktury tvého souboru!
sch['sheet']['drawings'].extend(labels)

# Ulož zpět
with open('name', 'w') as f:
	yaml.dump(sch, f, sort_keys=False)
