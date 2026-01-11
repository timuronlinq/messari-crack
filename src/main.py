import sys
from pathlib import Path

_SRC_DIR = str(Path(__file__).resolve().parent)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
from injector import CodeInjector, create_injector, quick_inject
injector = create_injector(auto_inject=True)
status = injector.get_status()
print(f"   Status: {status['context']['context_id']}")
print(f"   Injections: {status['injection_count']}\n")

def main():
    from injector_app import InjectorApp
    app = InjectorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
