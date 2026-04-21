"""
Patch Cassiopee/KCore/Dist.py to fix writeInstallPath() and createFortranBuilder() on Windows.
"""
import sys, os, re

DIST_PATH = r"C:/cassiopee/Cassiopee/KCore/Dist.py"
CASSIOPEE = "C:/cassiopee/Cassiopee"

txt = open(DIST_PATH, encoding="utf-8").read()

# -----------------------------------------------------------------------
# 1. Patch writeInstallPath() — inchangé, un seul chemin dans includePath
# -----------------------------------------------------------------------
start_marker = "def writeInstallPath():"
start = txt.find(start_marker)
if start == -1:
    print("ERROR: writeInstallPath() not found"); sys.exit(1)

rest = txt[start + len(start_marker):]
next_def = re.search(r'\ndef \w', rest)
end = start + len(start_marker) + next_def.start() + 1 if next_def else len(txt)

new_write = (
    "def writeInstallPath():\n"
    "    import os\n"
    "    cassiopee = os.environ.get('CASSIOPEE', '" + CASSIOPEE + "')\n"
    "    cassiopee = cassiopee.replace('\\\\', '/')\n"
    "    prod = os.environ.get('ELSAPROD', 'win64')\n"
    "    f = open('installPath.py', 'w')\n"
    "    f.write(\"installPath = '%s'\\n\" % cassiopee)\n"
    "    f.write(\"libPath = '%s/KCore/build/%s'\\n\" % (cassiopee, prod))\n"
    "    f.write(\"includePath = '%s/KCore/build/%s/KCore'\\n\" % (cassiopee, prod))\n"
    "    f.close()\n"
    "\n"
)

txt = txt[:start] + new_write + txt[end:]
print("Patch 1 writeInstallPath OK")

# -----------------------------------------------------------------------
# 2. Patch createFortranBuilder() pour ajouter KCore/KCore source aux -I
#    C'est là que Def/, Nuga/, etc. vivent mais ne sont pas copiés dans build/
# -----------------------------------------------------------------------
old_fortran = "def createFortranBuilder(env, dirs=[], additionalPPArgs='', additionalFortranArgs=[]):\n    import SCons\n    from SCons.Builder import Builder\n    # Pre-processing\n    path = ''\n    for i in dirs: path += '\"" + "%s\" -I'%i"

# On cherche juste le début de la fonction
fortran_marker = "def createFortranBuilder(env, dirs=[], additionalPPArgs='', additionalFortranArgs=[]):"
fortran_start = txt.find(fortran_marker)
if fortran_start == -1:
    print("ERROR: createFortranBuilder() not found"); sys.exit(1)

# On cherche la ligne "path = ''"
path_marker = "    path = ''\n    for i in dirs: path +="
path_pos = txt.find(path_marker, fortran_start)
if path_pos == -1:
    print("ERROR: path = '' not found in createFortranBuilder"); sys.exit(1)

# On insère le code d'ajout des chemins source juste avant "path = ''"
extra_dirs_code = (
    "    # WIN64 FIX: add KCore source dir so Fortran preprocessor finds\n"
    "    # Def/DefFortranConst.h, Nuga/include/zone_t.hxx, etc.\n"
    "    import os as _os\n"
    "    _cassiopee = _os.environ.get('CASSIOPEE', '').replace('\\\\', '/')\n"
    "    if _cassiopee:\n"
    "        _kcore_src = _cassiopee + '/KCore/KCore'\n"
    "        if _os.path.exists(_kcore_src) and _kcore_src not in dirs:\n"
    "            dirs = list(dirs) + [_kcore_src]\n"
)

txt = txt[:path_pos] + extra_dirs_code + txt[path_pos:]
print("Patch 2 createFortranBuilder OK")

# -----------------------------------------------------------------------
# Écriture finale
# -----------------------------------------------------------------------
open(DIST_PATH, "w", encoding="utf-8").write(txt)
print("Patch written.")

# Vérification
txt3 = open(DIST_PATH, encoding="utf-8").read()
if "WIN64 FIX" in txt3 and "writeInstallPath" in txt3:
    print("Verification OK")
else:
    print("ERROR: verification failed"); sys.exit(1)