import math
import string
from pcbnew import FromMM  # i když jsme v eeschema, někdy se hodí
import eeschema
import wx

# Získání reference na aktuální projekt a schéma
app = eeschema.GetApp()
schematic = app.GetSchematic()
sheet = schematic.GetCurrentSheet()
drawings = sheet.GetDrawings()

# Výchozí pozice
base_x = 10000000  # v nm (např. 10 mm)
base_y = 10000000  # v nm
dx = 2000000       # vzdálenost mezi sloupci (např. 2 mm)
dy = 1000000       # vzdálenost mezi řádky (1 mm)

# Generuj labely
for col, letter in enumerate(string.ascii_uppercase[:12]):  # A–L
    for row in range(8):  # 0–7
        name = f"P{letter}{row}"
        x = base_x + col * dx
        y = base_y + row * dy
        label = eeschema.SCHText()
        label.SetText(name)
        label.SetPosition(wx.Point(x, y))
        label.SetShape(eeschema.SCH_TEXT_SHAPE::NET_LABEL)  # síťový popisek
        sheet.Add(label)

# Obnovit zobrazení
app.Refresh()
