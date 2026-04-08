"""
Patch Cassiopee/KCore/installBase.py to update the win64 entry.
Targets the main branch which uses named-key dicts.
"""
import sys

PATH = r"C:/cassiopee/Cassiopee/KCore/installBase.py"

# We also need to check where config.py reads these keys from,
# since the key names changed from positional list to dict.
# From the file: keys are 'f77compiler', 'f90compiler', 'Cppcompiler',
# 'CppAdditionalOptions', 'f77AdditionalOptions', 'useOMP', 'static',
# 'additionalIncludePaths', 'additionalLibs', 'additionalLibPaths',
# 'useCuda', 'NvccAdditionalOptions'

NEW_WIN64 = """\
    'win64': {
        'description': 'Windows win64+msys2',
        'f77compiler': 'gfortran',
        'f90compiler': 'gfortran',
        'Cppcompiler': 'gcc',
        'CppAdditionalOptions': ['-DMS_WIN64', '-D__USE_MINGW_ANSI_STDIO=1', '-Wno-attributes'],
        'f77AdditionalOptions': [],
        'useOMP': False,
        'static': False,
        'additionalIncludePaths': [
            'C:/Python38/include',
            'C:/Python38/Lib/site-packages/numpy/core/include',
        ],
        'additionalLibs': ['python38', 'gfortran'],
        'additionalLibPaths': ['C:/Python38/libs'],
        'useCuda': False,
        'NvccAdditionalOptions': [],
    },"""

txt = open(PATH, encoding="utf-8").read()

# Find the win64 block
start_marker = "'win64': {"
start = txt.find(start_marker)
if start == -1:
    print("ERROR: 'win64': { not found in installBase.py")
    sys.exit(1)

print("Found 'win64' block at position {}".format(start))

# Walk forward to find the matching closing brace
brace_start = txt.index("{", start)
depth = 0
pos = brace_start
while pos < len(txt):
    if txt[pos] == "{":
        depth += 1
    elif txt[pos] == "}":
        depth -= 1
        if depth == 0:
            break
    pos += 1

# Include trailing comma if present
end = pos + 1
if end < len(txt) and txt[end] == ",":
    end += 1

print("--- Replacing ---")
print(txt[start:end][:200])
print("...")

txt2 = txt[:start] + NEW_WIN64 + txt[end:]
open(PATH, "w", encoding="utf-8").write(txt2)
print("Patch written.")

# Verify
txt3 = open(PATH, encoding="utf-8").read()
if "'win64': {" in txt3 and "C:/Python38/libs" in txt3:
    print("Verification OK")
else:
    print("ERROR: verification failed")
    sys.exit(1)