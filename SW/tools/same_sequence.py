#!/usr/bin/python -u
# vim: fileencoding=utf-8:nomodified:nowrap:textwidth=0:foldmethod=marker:foldcolumn=4:ruler:showcmd:lcs=tab\:|- list:tabstop=8:noexpandtab:nosmarttab:softtabstop=0:shiftwidth=0



import sys
import argparse
import re
from collections import Counter


def parse_range(value: str):
	"""
	Will parse:
		5	-> [5]
		5..10	-> [5,6,7,8,9,10]
		5-10	-> dtto
		5,10	-> dtto
		5asdf10	-> dtto
	If two numbers are not found will use one number or default 5.
	"""
	nums = list(map(int, re.findall(r"\d+", value)))
	if not nums:
		return [5]
	if len(nums) == 1:
		return [nums[0]]
	start, end = nums[0], nums[1]
	if start > end:
		start, end = end, start
	return list(range(start, end + 1))


def normalize_line(line: str):
	"""
	- remove ';' and all after
	- trim from left and right
	- sequence of whitespaces -> one space
	"""
	line = line.split(";", 1)[0]
	line = line.strip()
	line = re.sub(r"\s+", " ", line)
	return line


def read_lines(fileobj):
	return [
		normalize_line(line)
		for line in fileobj
		if normalize_line(line)
	]


def find_repeats(lines, n):
	seqs = Counter(
		tuple(lines[i:i+n])
		for i in range(len(lines) - n + 1)
	)
	return [(cnt, seq) for seq, cnt in seqs.items() if cnt > 1]


def main():
	parser = argparse.ArgumentParser(
		description="Search same sequences of line (subrutine candidates).",
		add_help=True
	)

	parser.add_argument(
		"file",
		nargs="?",
		help="Input file (default stdin)"
	)

	parser.add_argument(
		"-r", "--range",
		dest="range_",
		help="Range of sequence lengths (eg. 5..10, 5-10, 5,10, 7)",
		default="5"
	)

	parser.add_argument(
		"-n", "--separator",
		help="Separator of lines in output",
		default="\n"
	)

	parser.add_argument(
		"-i", "--intro",
		help="Intro string before count",
		default="Count: "
	)

	parser.add_argument(
		"--min-count",
		type=int,
		default=2,
		help="Minimal number of occurrences (default: 2)"
	)

	parser.add_argument(
		"--max-count",
		type=int,
		help="Maximum number of occurrences (default: unlimited)"
	)

	args = parser.parse_args()

	Ns = parse_range(args.range_)

	# vstup
	if args.file:
		with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
			lines = read_lines(f)
	else:
		lines = read_lines(sys.stdin)

	for n in Ns:
		results = find_repeats(lines, n)
		if not results:
			continue

		print(f"{'=' * 40} sequence: {n} {'=' * 40}")

		for cnt, seq in sorted(results, reverse=True):

			if cnt < args.min_count:
				continue
			if args.max_count is not None and cnt > args.max_count:
				continue
			print(f"{args.intro}{cnt}")
			print(args.separator.join(seq))
			print("-" * 40)


if __name__ == "__main__":
	main()
