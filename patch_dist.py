"""
Patch Cassiopee/KCore/Dist.py to fix writeInstallPath() on Windows.
"""
import sys, os, re

DIST_PATH = r"C:/cassiopee/Cassiopee/KCore/Dist.py"
CASSIOPEE = "C:/cassiopee/Cassiopee"

txt = open(DIST_PATH, encoding="utf-8").read()

# Print all installPath usages
print("=== All installPath attribute usages ===")
for m in re.finditer(r'installPath\.(\w+)', txt):
    line_start = txt.rfind('\n', 0, m.start()) + 1
    line_end = txt.find('\n', m.end())
    print("  .%s  =>  %s" % (m.group(1), txt[line_start:line_end].strip()))

# Print full checkModuleCassiopee
cm_start = txt.find("def checkModuleCassiopee(")
if cm_start != -1:
    rest = txt[cm_start + len("def checkModuleCassiopee("):]
    next_def = re.search(r'\ndef \w', rest)
    cm_end = cm_start + len("def checkModuleCassiopee(") + (next_def.start() + 1 if next_def else len(rest))
    print("\n=== checkModuleCassiopee ===")
    print(txt[cm_start:cm_end])

# Patch writeInstallPath
start_marker = "def writeInstallPath():"
start = txt.find(start_marker)
if start == -1:
    print("ERROR: writeInstallPath() not found")
    sys.exit(1)

rest = txt[start + len(start_marker):]
next_def = re.search(r'\ndef \w', rest)
end = start + len(start_marker) + next_def.start() + 1 if next_def else len(txt)

print("\n=== Current writeInstallPath() ===")
print(txt[start:end])

# Write installPath.py with all needed attributes.
# includePath: checkModuleCassiopee reads this and uses it directly as -I flag.
# Set it to the dir containing kcore.h = CASSIOPEE/KCore/build/win64/KCore
new_func = (
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

txt2 = txt[:start] + new_func + txt[end:]
open(DIST_PATH, "w", encoding="utf-8").write(txt2)
print("Patch written.")

txt3 = open(DIST_PATH, encoding="utf-8").read()
if "includePath = '%s/KCore/build" in txt3:
    print("Verification OK")
else:
    print("ERROR: verification failed")
    sys.exit(1)