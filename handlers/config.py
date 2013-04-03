
from config_tmpl import page
from navigation_tmpl import top
from cgi import parse_qs
import os

def ConfigPage(env):
	d = parse_qs(env['QUERY_STRING'])
	if 'seeds' in d:
		seeds = d['seeds'][0]
		try:
			with open("seeds.txt", "w") as f:
				print >>f, seeds
		except:
			print "Unable to save seeds :("

	seeds = "\n".join(line.strip() for line in open("seeds.txt", "r"))

	return top + page.format(seeds=seeds)