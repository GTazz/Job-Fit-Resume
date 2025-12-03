from pathlib import Path

scripts_dir = Path(__file__).resolve().parent.parent
module_names = [f.stem for f in scripts_dir.glob("[!_]*.py")]

content = "# Auto-generated imports by __generate_imports.py\n\n"
for name in module_names:
    content += f"from .{name} import {name}\n"

imports_file = scripts_dir / "__imports.py"
with imports_file.open("w", encoding="utf-8") as f:
    f.write(content)

# open __init__.py and verify if __imports import exists, if not, add it at the top
init_file = scripts_dir / "__init__.py"    
with init_file.open("r+", encoding="utf-8") as f:
    content = f.read()
    if "__imports" not in content:
        f.seek(0, 0)
        f.write("from .__imports import *\n" + content)
        
print(f"✓ Generated {imports_file} with {len(module_names)} exports")
