from modules.data.JsonSettings import SettingsMain as _SettingsMain, SettingsJson as _SettingsJson
from modules.data.Sheets import MainSheet as _MainSheet, \
    FilterSheet as _FilterSheet, PlansSheet as _PlansSheet, ErrorsSheetBase as _ErrorsSheetBase, \
    ErrorsSheetCollect as _ErrorsSheetCollect
from modules.data.Log import Log as _Log


Log = _Log

SettingsMain = _SettingsMain()
SettingsJson = _SettingsJson

MainSheet = _MainSheet()
FilterSheet = _FilterSheet()
PlansSheet = _PlansSheet()
ErrorsSheetBase = _ErrorsSheetBase()
ErrorsSheetCollect = _ErrorsSheetCollect()
