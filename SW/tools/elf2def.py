#!/usr/bin/python -u
# vim: fileencoding=utf-8:nomodified:nowrap:textwidth=0:foldmethod=marker:foldcolumn=4:ruler:showcmd:lcs=tab\:|- list:tabstop=8:noexpandtab:nosmarttab:softtabstop=0:shiftwidth=0
import subprocess
import sys
import re

if len(sys.argv) < 3:
	print("Použití: elf2def.py vstup.elf vystup.def")
	print("	vygeneruje makra address_of_<symbol> pro kazdy symbol z elf")
	sys.exit(1)

input_elf = sys.argv[1]
output_inc = sys.argv[2]

# Použij avr-objdump -t ke zjištění symbolů
try:
	result = subprocess.run(
		["avr-objdump", "-t", input_elf],
		capture_output=True,
		text=True,
		check=True
	)
except subprocess.CalledProcessError as e:
	print("Chyba při spouštění avr-objdump:", e.stderr)
	sys.exit(2)

# Regulární výraz pro symboly
#symbol_re = re.compile(r"^([0-9a-fA-F]{8})\s+g\s+\w+\s+\S+\s+[0-9a-fA-F]+\s+(\w+)$")
symbol_re = re.compile(r"^([0-9a-fA-F]{8})\s+.*\s+(\w+)$")

symbols = []

for line in result.stdout.splitlines():
	match = symbol_re.match(line.strip())
	if match:
		address_hex, label = match.groups()
		address = int(address_hex, 16)
		symbols.append((label, address))

# Zapsání do .inc souboru
with open(output_inc, "w") as f:
	for label, addr in symbols:
		lo = addr & 0xFF
		hi = (addr >> 8) & 0xFF
		b3 = (addr >> 16) & 0xFF
		f.write(f"#define address_of_{label:32}	.byte 0x{lo:02X}, 0x{hi:02X}, 0x{b3:02X}\n")

print(f"Vygenerováno: {output_inc}")

