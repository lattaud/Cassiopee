import sys

PATH = r"C:/cassiopee/Cassiopee/KCore/installBase.py"

NEW_WIN64 = (
    "    'win64': {\n"
    "        'description': 'Windows win64+msys2',\n"
    "        'f77compiler': 'gfortran',\n"
    "        'f90compiler': 'gfortran',\n"
    "        'Cppcompiler': 'gcc',\n"
    "        'CppAdditionalOptions': ['-DMS_WIN64', '-D__USE_MINGW_ANSI_STDIO=1', '-Wno-attributes'],\n"
    "        'f77AdditionalOptions': [],\n"
    "        'useOMP': False,\n"
    "        'static': False,\n"
    "        'additionalIncludePaths': [\n"
    "            'C:/Python38/include',\n"
    "            'C:/Python38/Lib/site-packages/numpy/core/include',\n"
    "            'C:/cassiopee/Cassiopee/KCore/build/win64/KCore',\n"
    "            'C:/cassiopee/Cassiopee/KCore/build/win64',\n"
    "            'C:/cassiopee/Cassiopee/KCore',\n"
    "        ],\n"
    "        'additionalLibs': ['python38', 'gfortran'],\n"
    "        'additionalLibPaths': [\n"
    "            'C:/Python38/libs',\n"
    "            'C:/cassiopee/Cassiopee/KCore/build/win64',\n"
    "        ],\n"
    "        'useCuda': False,\n"
    "        'NvccAdditionalOptions': [],\n"
    "    },"
)

txt = open(PATH, encoding="utf-8").read()

start_marker = "'win64': {"
start = txt.find(start_marker)
if start == -1:
    print("ERROR: 'win64': { not found in installBase.py")
    sys.exit(1)

print("Found 'win64' block at position {}".format(start))

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

end = pos + 1
if end < len(txt) and txt[end] == ",":
    end += 1

txt2 = txt[:start] + NEW_WIN64 + txt[end:]
open(PATH, "w", encoding="utf-8").write(txt2)
print("Patch written.")

txt3 = open(PATH, encoding="utf-8").read()
if "'win64': {" in txt3 and "C:/cassiopee/Cassiopee/KCore'" in txt3:
    print("Verification OK")
else:
    print("ERROR: verification failed")
    sys.exit(1)