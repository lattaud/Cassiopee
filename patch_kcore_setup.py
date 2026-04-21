import pathlib, shutil

src = pathlib.Path("C:/cassiopee/Cassiopee/KCore")
dst = pathlib.Path("C:/cassiopee/Cassiopee/KCore/KCore")

for f in ["Dist.py", "installBase.py", "installPath.py"]:
    shutil.copy2(src / f, dst / f)
    print(f"Copied {f} -> KCore/KCore/{f}")

# setup.py — ajouter package_data
setup_path = src / "setup.py"
txt = setup_path.read_text(encoding="utf-8")
old = "    packages=['KCore'],"
new = "    packages=['KCore'],\n    package_data={'KCore': ['Dist.py', 'installBase.py', 'installPath.py']},"
txt = txt.replace(old, new)
setup_path.write_text(txt, encoding="utf-8")
print("setup.py patché OK")