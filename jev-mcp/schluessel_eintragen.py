"""Fragt den TypeSafe-Schlüssel verdeckt ab und speichert ihn in ~/.typesafe_api_key."""

import getpass
import os
import pathlib
import sys

ziel = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / ".typesafe_api_key"
schluessel = getpass.getpass("TypeSafe-Schlüssel einfügen (bleibt unsichtbar), dann Enter: ").strip()
if not schluessel or any(c.isspace() for c in schluessel):
    print("Leer oder mit Leerzeichen. Nichts gespeichert.")
    sys.exit(1)
ziel.write_text(schluessel, encoding="utf-8")
try:
    os.chmod(ziel, 0o600)
except OSError:
    pass
print(f"Gespeichert: {ziel}")
