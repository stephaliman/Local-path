import re
import logging
from copy import copy

from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel,
    QDateTime
)

from PyQt5.Qt import (
    QStandardItem,
    QStandardItemModel
)

# TODO KV should we have a GUI element in this class??
from PyQt5.QtWidgets import (
    QMessageBox
)

from lexicon.module_classes import userdefinedroles as udr, delimiter, AddedInfo

# for backwards compatibility
specifytotalcycles_str = "Specify total number of cycles"
numberofreps_str = "Number of repetitions"

rb = "radio button"  # ie mutually exclusive in group / at this level
cb = "checkbox"  # ie not mutually exlusive
ed_1 = "editable level 1"  # ie value is editable but restricted to numbers that are >= 1 and multiples of 0.5
ed_2 = "editable level 2"  # ie value is editable but restricted to numbers
ed_3 = "editable level 3"  # ie value is editable and unrestricted
fx = "fixed"  # ie value is not editable
subgroup = "subgroup"

c = True  # checked
u = False  # unchecked

orientOptionsDict = {
    
}