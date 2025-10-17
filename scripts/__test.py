import sys
import subprocess
from pathlib import Path

class Main():
    def __init__(self):

        self.scripts = self.get_scripts()

        while True:
            self.display_menu()

            try:
                choice = input("\nSelect a script to run (number): ").strip()

                if not choice.isdigit():
                    print("Please enter a valid number.")
                    continue

                choice = int(choice)

                if choice == len(self.scripts) + 1:
                    raise KeyboardInterrupt

                if 1 <= choice <= len(self.scripts):
                    script_name = self.scripts[choice - 1]
                    self.run_script(script_name)
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
    
    def get_scripts(self):
        """Get list of Python scripts in the scripts directory."""
        # Always use the scripts directory relative to the project root
        project_root = Path(__file__).resolve().parent.parent
        scripts_dir = project_root / "scripts"

        scripts = []
        for file in scripts_dir.glob("*.py"):
            if not file.name.startswith("__"):
                scripts.append(file.name)

        return sorted(scripts)


    def display_menu(self):
        """Display the menu with available scripts."""
        print("\n" + "=" * 50)
        print("Available Scripts")
        print("=" * 50)

        for i, script in enumerate(self.scripts, 1):
            print(f"{i}. {script}")

        print(f"{len(self.scripts) + 1}. Exit")
        print("=" * 50)


    def run_script(self, script_name):
        """Run the selected script from the project root."""
        project_root = Path(__file__).resolve().parent.parent
        module_name = script_name.replace(".py", "")

        print(f"\n{'='*50}")
        print(f"Running: {script_name} as module")
        print(f"{'='*50}\n")

        try:
            # Run the script as a module from the project root
            subprocess.run(
                [sys.executable, "-m", f"scripts.{module_name}"],
                cwd=str(project_root),
                check=False,
            )

            print(f"\n{'='*50}")
            print(f"✓ {script_name} completed")
            print(f"{'='*50}")

        except (OSError, subprocess.SubprocessError) as e:
            print(f"\n{'='*50}")
            print(f"✗ Error running {script_name}: {e}")
            print(f"{'='*50}")

if __name__ == "__main__":
    Main()
