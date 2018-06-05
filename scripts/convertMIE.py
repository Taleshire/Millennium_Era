import os
from collections import defaultdict


replacements = [
	('#textdomain wesnoth-millennium-era','#textdomain wesnoth-Ageless_Era'),

	('[unit_type]','''[unit_type]
    description={AE_MIE_UNIT_NOTICE}'''), # Needs to be changed once a single unit has actual unit description, then all without should use NO_DESCR_AVAILABLE or similar
	# ("""
    # description= _ ""","""
    # description={AE_MIE_UNIT_NOTICE}+ _ """),
	# ("""
    # description=_ ""","""
    # description={AE_MIE_UNIT_NOTICE}+ _ """),
	# ("""
    # description=_""","""
    # description={AE_MIE_UNIT_NOTICE}+ _ """),
	# ("""
    # description={NO_DESCR_AVAILABLE}""","""
    # description={AE_MIE_UNIT_NOTICE}+{NO_DESCR_AVAILABLE}"""),
	("__DUMMY__","__DUMMY__")
]

def getAgelessPath(dname, fname):
	if "factions" in dname:
		return os.path.join(".","Ageless_Era","factions","MiE",fname)
	if "units" in dname:
		basename = os.path.basename(dname)
		if basename == "units":
			basename = ""
		return os.path.join(".","Ageless_Era","units","MiE_units",basename,fname)
	if "utils" in dname:
		return os.path.join(".","Ageless_Era","data","MiE_data",fname)
	raise Exception("Unhandled folder {}".format(dname))

eras = defaultdict(str)
for dname, dirs, files in os.walk(".."):
	if "factions" not in dname and "units" not in dname and "utils" not in dname:
		continue
	if "Ageless_Era" in dname or "images" in dname:
		continue
	print(dname)
	for fname in files:
		fpath = os.path.join(dname, fname)
		afpath = getAgelessPath(dname, fname)
		# print(fpath, afpath)
		with open(fpath,encoding="utf8") as f:
			s = f.read()
		for (find, replace) in replacements:
			s = s.replace(find, replace)
		if "factions" in dname:
			s = s.replace('name= _', 'name= "MiE - " + _')
			if "default" in fname:
				eras["default"] += s
				eras["default"] += "\n"
			elif "aoh" in fname:
				eras["heroes"] += s
				eras["heroes"] += "\n"
			elif "rpg" in fname:
				eras["RPG"] += s
				eras["RPG"] += "\n"
		else:
			os.makedirs(os.path.dirname(afpath), exist_ok=True)
			with open(afpath, "w", encoding="utf8") as f:
				f.write(s)

with open("Ageless_Era/units/MiE_units/_main.cfg", "a", encoding="utf8") as f:
	f.write("""

{GET_AE_UNITS MiE_units/centaurs}
{GET_AE_UNITS MiE_units/cornurs}
{GET_AE_UNITS MiE_units/faeries}
{GET_AE_UNITS MiE_units/human-outlaws}
{GET_AE_UNITS MiE_units/human-thelians}
{GET_AE_UNITS MiE_units/spirits}
{GET_AE_UNITS MiE_units/treefolk}
{GET_AE_UNITS MiE_units/vampires}
{GET_AE_UNITS MiE_units/wolves}
""")

# factions to file
for era in eras:
	os.makedirs(os.path.dirname("Ageless_Era/factions/{}/".format(era)), exist_ok=True)
	with open("Ageless_Era/factions/{}/{}-MiE.cfg".format(era, era), "w", encoding="utf8") as f:
		f.write(eras[era])
