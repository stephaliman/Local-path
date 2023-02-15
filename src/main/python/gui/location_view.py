# import os
from copy import copy

from PyQt5.QtCore import (
    Qt,
    # QAbstractListModel,
    QAbstractTableModel,
    pyqtSignal,
    # QModelIndex,
    # QItemSelectionModel,
    QSortFilterProxyModel,
    QDateTime,
    QRectF
)

from PyQt5.Qt import (
    QStandardItem,
    QStandardItemModel
)

from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import (
    # QWidget,
    # QLabel,
    # QLineEdit,
    QListView,
    QHeaderView,
    QTableView,
    # QVBoxLayout,
    QComboBox,
    # QTreeView,
    # QStyle,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem
)

from lexicon.module_classes import delimiter, LocationType, userdefinedroles as udr
from lexicon.module_classes2 import AddedInfo

# radio button vs checkbox
rb = "radio button"  # ie mutually exclusive in group / at this level
cb = "checkbox"  # ie not mutually exlusive

# editable vs fixed
ed = "editable" 
fx = "fixed"  # ie not editable

# in subgroup?
subgroup = "subgroup"

# checked vs unchecked
c = True  # checked
u = False  # unchecked

# location type (and types of surfaces, subareas, bones/joints, etc) is either nonhand or hand
h = "hand"
n = "nonhand"

# allow surface, subarea, and/or bone/joint specification?
allow = True
disallow = False

# if surface, subarea, and/or bone/joint specification is allowed, are there any exceptions to which ones?
no_exceptions = ()


anterior = "Anterior"
posterior = "Posterior"
lateral = "Lateral"
medial = "Medial"
top = "Top"
bottom = "Bottom"
contra_half = "Contra half"
upper_half = "Upper half"
whole = "Whole"
centre = "Centre"
lower_half = "Lower half"
ipsi_half = "Ipsi half"
back = "Back"
friction = "Friction"
radial = "Radial"
ulnar = "Ulnar"
metacarpophalangeal_joint = "Metacarpophalangeal joint"
proximal_bone = "Proximal bone"
proximal_interphalangeal_joint = "Proximal interphalangeal joint"
medial_bone = "Medial bone"
distal_interphalangeal_joint = "Distal interphalangeal joint"
distal_bone = "Distal bone"
tip = "Tip"

surfaces_nonhand_default = [anterior, posterior, lateral, medial, top, bottom]
subareas_nonhand_default = [contra_half, upper_half, whole, centre, lower_half, ipsi_half]
surfaces_hand_default = [back, friction, radial, ulnar]
bonejoint_hand_default = [metacarpophalangeal_joint, proximal_bone, proximal_interphalangeal_joint,
                         medial_bone, distal_interphalangeal_joint, distal_bone, tip]

surface_label = "Surface"
subarea_label = "Sub-area"
bonejoint_label = "Bone/joint"


# TODO KV: should be able to get rid of "fx" and "subgroup" (and maybe other?) options here...
# TODO KV - check specific exceptions etc for each subarea & surface
# unless we're going to reference the same code (as for moevment) for building the tree & list models
locn_options_body = {
    # ("No movement", fx, rb, u): {},
    ("Head", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {
        ("Back of head", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
        ("Top of head", fx, rb, u, n, disallow, no_exceptions, allow, (upper_half, lower_half)): {},
        ("Side of face", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
            ("Side of face - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
            ("Side of face - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
        },
        ("Face", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {
            ("Temple", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                ("Temple - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                ("Temple - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
            },
            ("Above forehead (hairline)", fx, rb, u, n, disallow, no_exceptions, allow, (upper_half, lower_half)): {},
            ("Forehead", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
            ("Eyebrow", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                ("Eyebrow - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                ("Eyebrow - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                ("Between eyebrows", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
            },
            ("Eye", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                ("Eye - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                ("Eye - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                ("Outer corner of eye", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Outer corner of eye - contra", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {},
                    ("Outer corner of eye - ipsi", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {}
                },
                ("Upper eyelid", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Upper eyelid - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Upper eyelid - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Lower eyelid", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Lower eyelid - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Lower eyelid - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                }
            },
            ("Cheek/nose", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {
                ("Cheek", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Cheek - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Cheek - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Maxillary process of zygomatic", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Maxillary process of zygomatic - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Maxillary process of zygomatic - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Zygomatic process of temporal bone", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Zygomatic process of temporal bone - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Zygomatic process of temporal bone - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Nose", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {
                    ("Nose root", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Nose ridge", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Nose tip", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},  # TODO KV resolve question mark from locations spreadsheet
                    ("Septum", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
                }
            },
            ("Below nose / philtrum", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
            ("Mouth", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {
                ("Lips", fx, rb, u, n, disallow, no_exceptions, allow, (upper_half, lower_half)): {
                    ("Upper lip", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Lower lip", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Corner of mouth - contra", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {},
                ("Corner of mouth - ipsi", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {},
                ("Teeth", fx, rb, u, n, disallow, no_exceptions, allow, (upper_half, lower_half)): {
                    ("Upper teeth", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
                    ("Lower teeth", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
                },
                ("Tongue", fx, rb, u, n, allow, tuple([s for s in surfaces_nonhand_default if s not in [anterior, top, bottom]]), allow, (upper_half, lower_half)): {},  # TODO KV resolve question mark from locations spreadsheet
            },
            ("Ear", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                ("Ear - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                ("Ear - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                ("Mastoid process", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Mastoid process - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                    ("Mastoid process - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
                },
                ("Earlobe", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                    ("Earlobe - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                    ("Earlobe - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
                }
            },
            ("Jaw", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
                ("Jaw - contra", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {},
                ("Jaw - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {}
            },
            ("Chin", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
            ("Under chin", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {}
        },
    },
    ("Neck", fx, rb, u, n, allow, tuple([s for s in surfaces_nonhand_default if s not in [anterior, posterior]]), allow, no_exceptions): {},  # TODO KV resolve question mark from locations spreadsheet
    ("Torso", fx, rb, u, n, allow, (medial, top, bottom), allow, no_exceptions): {
        ("Shoulder", fx, rb, u, n, allow, (medial, bottom), allow, (contra_half, ipsi_half)): {
            ("Shoulder - contra", fx, rb, u, n, allow, (medial, bottom), allow, no_exceptions): {},
            ("Shoulder - ipsi", fx, rb, u, n, allow, (medial, bottom), allow, no_exceptions): {}
        },
        ("Armpit", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {
            ("Armpit - contra", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {},
            ("Armpit - ipsi", fx, rb, u, n, disallow, no_exceptions, disallow, no_exceptions): {}
        },
        ("Sternum/clavicle area", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
        ("Chest/breast area", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
        ("Abdominal/waist area", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
        ("Pelvis area", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
        ("Hip", fx, rb, u, n, allow, (medial, top, bottom), allow, (contra_half, ipsi_half)): {
            ("Hip - contra", fx, rb, u, n, allow, (medial, top, bottom), allow, no_exceptions): {},
            ("Hip - ipsi", fx, rb, u, n, allow, (medial, top, bottom), allow, no_exceptions): {}
        },
        ("Groin", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},  # TODO KV resolve question mark from locations spreadsheet
        ("Buttocks", fx, rb, u, n, disallow, no_exceptions, allow, (contra_half, ipsi_half)): {
            ("Buttocks - contra", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {},
            ("Buttocks - ipsi", fx, rb, u, n, disallow, no_exceptions, allow, no_exceptions): {}
        }
    },
    ("Arm (contralateral)", fx, rb, u, n, allow, (top, bottom), disallow, no_exceptions): {
        ("Upper arm", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {
            ("Upper arm above biceps", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {},
            ("Biceps", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {}
        },
        ("Elbow", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {},
        ("Forearm", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {},
        ("Wrist", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {}
    },
    ("Legs and feet", fx, rb, u, n, allow, no_exceptions, allow, (contra_half, ipsi_half)): {
        ("Upper leg", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {
            ("Upper leg - contra", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {},
            ("Upper leg - ipsi", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {}
        },
        ("Knee", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {
            ("Knee - contra", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {},
            ("Knee - ipsi", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {}
        },
        ("Lower leg", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {
            ("Lower leg - contra", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {},
            ("Lower leg - ipsi", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {}
        },
        ("Ankle", fx, rb, u, n, allow, (top, bottom), allow, (contra_half, ipsi_half)): {
            ("Ankle - contra", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {},
            ("Ankle - ipsi", fx, rb, u, n, allow, (top, bottom), allow, no_exceptions): {}
        },
        ("Foot", fx, rb, u, n, allow, no_exceptions, allow, (contra_half, ipsi_half)): {
            ("Foot - contra", fx, rb, u, n, allow, no_exceptions, allow, (upper_half, lower_half)): {},
            ("Foot - ipsi", fx, rb, u, n, allow, no_exceptions, allow, (upper_half, lower_half)): {}
        }
    },
    ("Other hand", fx, rb, u, h, allow, no_exceptions, disallow, no_exceptions): {
        ("Whole hand", fx, rb, u, h, allow, no_exceptions, disallow, no_exceptions): {},
        ("Hand minus fingers", fx, rb, u, h, allow, no_exceptions, disallow, no_exceptions): {},
        ("Heel of hand", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Thumb", fx, rb, u, h, allow, no_exceptions, allow, (proximal_interphalangeal_joint, medial_bone)): {},
        ("Fingers", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Selected fingers", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Selected fingers and Thumb", fx, rb, u, h, allow, no_exceptions, allow, (proximal_interphalangeal_joint, medial_bone)): {},
        ("Finger 1", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Finger 2", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Finger 3", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Finger 4", fx, rb, u, h, allow, no_exceptions, allow, no_exceptions): {},
        ("Between Thumb and Finger 1", fx, rb, u, h, allow, tuple([s for s in surfaces_hand_default if s not in [back, friction]]), disallow, no_exceptions): {},
        ("Between Fingers 1 and 2", fx, rb, u, h, allow, tuple([s for s in surfaces_hand_default if s not in [back, friction]]), disallow, no_exceptions): {},
        ("Between Fingers 2 and 3", fx, rb, u, h, allow, tuple([s for s in surfaces_hand_default if s not in [back, friction]]), disallow, no_exceptions): {},
        ("Between Fingers 3 and 4", fx, rb, u, h, allow, tuple([s for s in surfaces_hand_default if s not in [back, friction]]), disallow, no_exceptions): {},
    }
}

# TODO KV: should be able to get rid of "fx" and "subgroup" (and maybe other?) options here...
# unless we're going to reference the same code (as for moevment) for building the tree & list models
locn_options_purelyspatial = {
    # ("No movement", fx, rb, u): {},
    ("Vertical axis", fx, cb, u, None, None, None, None, None): {
        ("High", fx, rb, u, None, None, None, None, None): {},
        ("Mid", fx, rb, u, None, None, None, None, None): {},
        ("Low", fx, rb, u, None, None, None, None, None): {},
    },
    ("Sagittal axis", fx, cb, u, None, None, None, None, None): {
        ("In front", fx, rb, u, None, None, None, None, None): {
            ("Far", fx, rb, u, None, None, None, None, None): {},
            ("Med.", fx, rb, u, None, None, None, None, None): {},
            ("Close", fx, rb, u, None, None, None, None, None): {},
        },
        ("Behind", fx, rb, u, None, None, None, None, None): {
            ("Far", fx, rb, u, None, None, None, None, None): {},
            ("Med.", fx, rb, u, None, None, None, None, None): {},
            ("Close", fx, rb, u, None, None, None, None, None): {},
        },
    },
    ("Horizontal axis", fx, cb, u, None, None, None, None, None): {
        ("Ipsi", fx, rb, u, None, None, None, None, None): {
            ("Far", fx, rb, u, None, None, None, None, None): {},
            ("Med.", fx, rb, u, None, None, None, None, None): {},
            ("Close", fx, rb, u, None, None, None, None, None): {},
        },
        ("Central", fx, rb, u, None, None, None, None, None): {},
        ("Contra", fx, rb, u, None, None, None, None, None): {
            ("Far", fx, rb, u, None, None, None, None, None): {},
            ("Med.", fx, rb, u, None, None, None, None, None): {},
            ("Close", fx, rb, u, None, None, None, None, None): {},
        },
    },
}


class LocationTreeItem(QStandardItem):

    def __init__(self, txt="", listit=None, mutuallyexclusive=False, ishandloc=False,
                 allowsurfacespec=True, allowsubareaspec=True, addedinfo=None,
                 surface_exceptions=None, subarea_exceptions=None, serializedlocntreeitem=None):
        super().__init__()

        if serializedlocntreeitem:
            self.setEditable(serializedlocntreeitem['editable'])
            self.setText(serializedlocntreeitem['text'])
            self.setCheckable(serializedlocntreeitem['checkable'])
            self.setCheckState(serializedlocntreeitem['checkstate'])
            self.setUserTristate(serializedlocntreeitem['usertristate'])
            self.setData(serializedlocntreeitem['selectedrole'], Qt.UserRole + udr.selectedrole)
            self.setData(serializedlocntreeitem['texteditrole'], Qt.UserRole + udr.texteditrole)
            self.setData(serializedlocntreeitem['timestamprole'], Qt.UserRole + udr.timestamprole)
            self.setData(serializedlocntreeitem['mutuallyexclusiverole'], Qt.UserRole + udr.mutuallyexclusiverole)
            self.setData(serializedlocntreeitem['displayrole'], Qt.DisplayRole)
            self._addedinfo = serializedlocntreeitem['addedinfo']
            self._ishandloc = serializedlocntreeitem['ishandloc']
            # self._allowsurfacespec = serializedlocntreeitem['allowsurfacespec']
            # self._allowsubareaspec = serializedlocntreeitem['allowsubareaspec']
            self.detailstable = LocationTableModel(serializedtablemodel=serializedlocntreeitem['detailstable'])
            self.listitem = LocationListItem(serializedlistitem=serializedlocntreeitem['listitem'])
            self.listitem.treeitem = self
        else:
            self.setEditable(False)
            self.setText(txt)
            self.setCheckable(True)
            self.setCheckState(Qt.Unchecked)
            self.setUserTristate(False)
            self.setData(False, Qt.UserRole + udr.selectedrole)
            self.setData(False, Qt.UserRole + udr.texteditrole)
            self.setData(QDateTime.currentDateTimeUtc(), Qt.UserRole + udr.timestamprole)
            self._addedinfo = addedinfo if addedinfo is not None else AddedInfo()
            self._ishandloc = ishandloc
            # self._allowsurfacespec = allowsurfacespec
            # self._allowsubareaspec = allowsubareaspec
            self.detailstable = LocationTableModel(
                loctext=txt,
                ishandloc=ishandloc,
                allowsurfacespec=allowsurfacespec,
                allowsubareaspec=allowsubareaspec,
                surface_exceptions=surface_exceptions,
                subarea_exceptions=subarea_exceptions
            )

            if mutuallyexclusive:
                self.setData(True, Qt.UserRole + udr.mutuallyexclusiverole)
            else:
                self.setData(False, Qt.UserRole + udr.mutuallyexclusiverole)

            self.listitem = listit
            if listit is not None:
                self.listitem.treeitem = self

    def __repr__(self):
        return '<LocationTreeItem: ' + repr(self.text()) + '>'

    def serialize(self):
        return {
            'editable': self.isEditable(),
            'text': self.text(),
            'checkable': self.isCheckable(),
            'checkstate': self.checkState(),
            'usertristate': self.isUserTristate(),
            'timestamprole': self.data(Qt.UserRole + udr.timestamprole),
            'selectedrole': self.data(Qt.UserRole + udr.selectedrole),
            'texteditrole': self.data(Qt.UserRole + udr.texteditrole),
            'mutuallyexclusiverole': self.data(Qt.UserRole + udr.mutuallyexclusiverole),
            'ishandloc': self._ishandloc,
            'displayrole': self.data(Qt.DisplayRole),
            'addedinfo': self._addedinfo,
            # 'allowsurfacespec': self._allowsurfacespec,
            # 'allowsubareaspec': self._allowsubareaspec,
            'detailstable': LocationTableSerializable(self.detailstable)
            # 'listitem': self.listitem.serialize()  TODO KV why not? the constructor uses it...
        }

    # @property
    # def allowsurfacespec(self):
    #     return self._allowsurfacespec
    #
    # @allowsurfacespec.setter
    # def allowsurfacespec(self, allowsurfacespec):
    #     self._allowsurfacespec = allowsurfacespec
    #
    # @property
    # def allowsubareaspec(self):
    #     return self._allowsubareaspec
    #
    # @allowsubareaspec.setter
    # def allowsubareaspec(self, allowsubareaspec):
    #     self._allowsubareaspec = allowsubareaspec

    @property
    def ishandloc(self):
        return self._ishandloc

    @ishandloc.setter
    def ishandloc(self, ishandloc):
        self._ishandloc = ishandloc

    @property
    def addedinfo(self):
        return self._addedinfo

    @addedinfo.setter
    def addedinfo(self, addedinfo):
        self._addedinfo = addedinfo if addedinfo is not None else AddedInfo()

    def updatelistdata(self):
        if self.parent() and "Specify total number of cycles" in self.parent().data():
            previouslistitemtext = self.listitem.text()
            parentname = self.parent().text()
            updatetextstartindex = previouslistitemtext.index(parentname) + len(parentname + delimiter)
            if delimiter in previouslistitemtext[updatetextstartindex:]:
                updatetextstopindex = previouslistitemtext.index(delimiter, updatetextstartindex)
            else:
                updatetextstopindex = len(previouslistitemtext) + 1
            selftext = self.text()
            self.listitem.updatetext(
                previouslistitemtext[:updatetextstartindex] + selftext + previouslistitemtext[updatetextstopindex:])

    def check(self, fully=True):
        self.setCheckState(Qt.Checked if fully else Qt.PartiallyChecked)
        self.listitem.setData(fully, Qt.UserRole + udr.selectedrole)
        if fully:
            self.setData(QDateTime.currentDateTimeUtc(), Qt.UserRole + udr.timestamprole)
            self.listitem.setData(QDateTime.currentDateTimeUtc(), Qt.UserRole + udr.timestamprole)
        self.checkancestors()

        # gather siblings in order to deal with mutual exclusivity (radio buttons)
        siblings = self.collectsiblings()

        # if this is a radio button item, make sure none of its siblings are checked
        if self.data(Qt.UserRole + udr.mutuallyexclusiverole):
            for sib in siblings:
                sib.uncheck(force=True)
        else:  # or if it has radio button siblings, make sure they are unchecked
            for me_sibling in [s for s in siblings if s.data(Qt.UserRole + udr.mutuallyexclusiverole)]:
                me_sibling.uncheck(force=True)

    def collectsiblings(self):

        siblings = []
        parent = self.parent()
        if not parent:
            parent = self.model().invisibleRootItem()
        numsiblingsincludingself = parent.rowCount()
        for snum in range(numsiblingsincludingself):
            sibling = parent.child(snum, 0)
            if sibling.index() != self.index():  # ie, it's actually a sibling
                siblings.append(sibling)

        mysubgroup = self.data(Qt.UserRole + udr.subgroupnamerole)
        subgrouporgeneralsiblings = [sib for sib in siblings if
                                     sib.data(Qt.UserRole + udr.subgroupnamerole) == mysubgroup or not sib.data(
                                         Qt.UserRole + udr.subgroupnamerole)]
        subgroupsiblings = [sib for sib in siblings if sib.data(Qt.UserRole + udr.subgroupnamerole) == mysubgroup]

        # if I'm ME and in a subgroup, collect siblings from my subgroup and also those at my level but not in any subgroup
        if self.data(Qt.UserRole + udr.mutuallyexclusiverole) and mysubgroup:
            return subgrouporgeneralsiblings
        # if I'm ME and not in a subgroup, collect all siblings from my level (in subgroups or no)
        elif self.data(Qt.UserRole + udr.mutuallyexclusiverole):
            return siblings
        # if I'm *not* ME but I'm in a subgroup, collect all siblings from my subgroup
        elif not self.data(Qt.UserRole + udr.mutuallyexclusiverole) and mysubgroup:
            return subgroupsiblings
        # if I'm *not* ME and not in a subgroup, collect all siblings from my level (in subgroups or no)
        elif not self.data(Qt.UserRole + udr.mutuallyexclusiverole):
            return siblings

    def checkancestors(self):
        if self.checkState() == Qt.Unchecked:
            self.setCheckState(Qt.PartiallyChecked)
        if self.parent() is not None:
            self.parent().checkancestors()

    def uncheck(self, force=False):
        name = self.data()

        self.listitem.setData(False, Qt.UserRole + udr.selectedrole)
        self.setData(False, Qt.UserRole + udr.selectedrole)

        # TODO KV - can't just uncheck a radio button... or can we?

        if force:  # force-clear this item and all its descendants - have to start at the bottom?
            # self.forceuncheck()
            # force-uncheck all descendants
            if self.hascheckedchild():
                for r in range(self.rowCount()):
                    for c in range(self.columnCount()):
                        ch = self.child(r, c)
                        if ch is not None:
                            ch.uncheck(force=True)
            self.setCheckState(Qt.Unchecked)
        elif self.hascheckedchild():
            self.setCheckState(Qt.PartiallyChecked)
        else:
            self.setCheckState(Qt.Unchecked)
            if self.parent() is not None:
                self.parent().uncheckancestors()

        if self.data(Qt.UserRole + udr.mutuallyexclusiverole):
            pass
            # TODO KV is this relevant? shouldn't be able to uncheck anyway
        elif True:  # has a mutually exclusive sibling
            pass
            # might one of those sibling need to be checked, if none of the boxes are?

    def uncheckancestors(self):
        if self.checkState() == Qt.PartiallyChecked and not self.hascheckedchild():
            self.setCheckState(Qt.Unchecked)
            if self.parent() is not None:
                self.parent().uncheckancestors()

    def hascheckedchild(self):
        foundone = False
        numrows = self.rowCount()
        numcols = self.columnCount()
        r = 0
        while not foundone and r < numrows:
            c = 0
            while not foundone and c < numcols:
                child = self.child(r, c)
                if child is not None:
                    foundone = child.checkState() in [Qt.Checked, Qt.PartiallyChecked]
                c += 1
            r += 1
        return foundone


class TreeSearchComboBox(QComboBox):
    item_selected = pyqtSignal(LocationTreeItem)

    def __init__(self, parentlayout=None):
        super().__init__()
        self.refreshed = True
        self.lasttextentry = ""
        self.lastcompletedentry = ""
        self.parentlayout = parentlayout

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        if key == Qt.Key_Right:  # TODO KV and modifiers == Qt.NoModifier:

            if self.currentText():
                # self.parentlayout.treedisplay.collapseAll()
                itemstoselect = gettreeitemsinpath(self.parentlayout.treemodel, self.currentText(), delim=delimiter)
                for item in itemstoselect:
                    if item.checkState() == Qt.Unchecked:
                        item.setCheckState(Qt.PartiallyChecked)
                    # self.parentlayout.treedisplay.setExpanded(item.index(), True)
                itemstoselect[-1].setCheckState(Qt.Checked)
                self.item_selected.emit(itemstoselect[-1])
                self.setCurrentIndex(-1)

        if key == Qt.Key_Period and modifiers == Qt.ControlModifier:
            if self.refreshed:
                self.lasttextentry = self.currentText()
                self.refreshed = False

            if self.lastcompletedentry:
                # cycle to first line of next entry that starts with the last-entered text
                foundcurrententry = False
                foundnextentry = False
                i = 0
                while self.completer().setCurrentRow(i) and not foundnextentry:
                    completionoption = self.completer().currentCompletion()
                    if completionoption.lower().startswith(self.lastcompletedentry.lower()):
                        foundcurrententry = True
                    elif foundcurrententry and self.lasttextentry.lower() in completionoption.lower() and not completionoption.lower().startswith(self.lastcompletedentry.lower()):
                        foundnextentry = True
                        if delimiter in completionoption[len(self.lasttextentry):]:
                            self.setEditText(
                                completionoption[:completionoption.index(delimiter, len(self.lasttextentry)) + 1])
                        else:
                            self.setEditText(completionoption)
                        self.lastcompletedentry = self.currentText()
                    i += 1
            else:
            # if not self.lastcompletedentry:
                # cycle to first line of first entry that starts with the last-entered text
                foundnextentry = False
                i = 0
                while self.completer().setCurrentRow(i) and not foundnextentry:
                    completionoption = self.completer().currentCompletion()
                    if completionoption.lower().startswith(self.lasttextentry.lower()):
                        foundnextentry = True
                        if delimiter in completionoption[len(self.lasttextentry):]:
                            self.setEditText(
                                completionoption[:completionoption.index(delimiter, len(self.lasttextentry)) + 1])
                        else:
                            self.setEditText(completionoption)
                        self.lastcompletedentry = self.currentText()
                    i += 1

        else:
            self.refreshed = True
            self.lasttextentry = ""
            self.lastcompletedentry = ""
            super().keyPressEvent(event)


# This class is a serializable form of the class LocationTreeModel, which is itself not pickleable.
# Rather than being based on QStandardItemModel, this one uses dictionary structures to convert to
# and from saveable form.
class LocationTreeSerializable:

    def __init__(self, locntreemodel):

        # creates a full serializable copy of the location tree, eg for saving to disk
        treenode = locntreemodel.invisibleRootItem()

        self.numvals = {}
        self.checkstates = {}
        self.detailstables = {}
        self.addedinfos = {}

        self.collectdata(treenode)

        self.locationtype = copy(locntreemodel.locationtype)

    def collectdata(self, treenode):
        if treenode is not None:
            for r in range(treenode.rowCount()):
                treechild = treenode.child(r, 0)
                if treechild is not None:
                    pathtext = treechild.data(Qt.UserRole + udr.pathdisplayrole)
                    checkstate = treechild.checkState()
                    locntable = treechild.detailstable
                    addedinfo = treechild.addedinfo
                    self.addedinfos[pathtext] = copy(addedinfo)
                    self.detailstables[pathtext] = LocationTableSerializable(locntable)
                    editable = treechild.isEditable()
                    if editable:
                        pathsteps = pathtext.split(delimiter)
                        parentpathtext = delimiter.join(pathsteps[:-1])
                        numericstring = pathsteps[-1]  # pathtext[lastdelimindex + 1:]
                        self.numvals[parentpathtext] = numericstring

                    self.checkstates[pathtext] = checkstate
                self.collectdata(treechild)

    def getLocationTreeModel(self):
        locntreemodel = LocationTreeModel()
        locntreemodel.locationtype = self.locationtype
        rootnode = locntreemodel.invisibleRootItem()
        locntreemodel.populate(rootnode)
        makelistmodel = locntreemodel.listmodel  # TODO KV   what is this? necessary?
        self.setvalues(rootnode)
        return locntreemodel

    def setvalues(self, treenode):
        if treenode is not None:
            for r in range(treenode.rowCount()):
                treechild = treenode.child(r, 0)
                if treechild is not None:
                    pathtext = treechild.data(Qt.UserRole+udr.pathdisplayrole)
                    parentpathtext = treenode.data(Qt.UserRole+udr.pathdisplayrole)
                    if parentpathtext in self.numvals.keys():
                        treechild.setText(self.numvals[parentpathtext])
                        treechild.setEditable(True)
                        pathtext = parentpathtext + delimiter + self.numvals[parentpathtext]
                    treechild.setCheckState(self.checkstates[pathtext])
                    treechild.detailstable = LocationTableModel(serializedtablemodel=self.detailstables[pathtext])
                    treechild.addedinfo = copy(self.addedinfos[pathtext])
                    self.setvalues(treechild)


# TODO KV implement this base class; refactor children (eg LocationModuleSerializable) to inherit as much as possible
class ParameterModuleSerializable:

    def __init__(self, parammod):
        self.hands = parammod.hands


# This class is a serializable form of the class LocationTreeModel, which is itself not pickleable.
# Rather than being based on QStandardItemModel, this one uses dictionary structures to convert to
# and from saveable form.
class LocationModuleSerializable:

    def __init__(self, locnmodule):

        # creates a full serializable copy of the location module, eg for saving to disk
        self.hands = locnmodule.hands
        self.timingintervals = locnmodule.timingintervals
        self.phonlocs = locnmodule.phonlocs
        self.addedinfo = locnmodule.addedinfo

        locntreemodel = locnmodule.locationtreemodel
        self.locationtree = LocationTreeSerializable(locntreemodel)


class LocationTreeModel(QStandardItemModel):

    def __init__(self, **kwargs):  #  movementparameters=None,
        super().__init__(**kwargs)
        self._listmodel = None  # LocationListModel(self)
        self.itemChanged.connect(self.updateCheckState)
        self.dataChanged.connect(self.updatelistdata)
        self._locationtype = LocationType()

    def tempprintcheckeditems(self):
        treenode = self.invisibleRootItem()
        self.printhelper(treenode)

    def tempprinthelper(self, treenode):
        for r in range(treenode.rowCount()):
            treechild = treenode.child(r, 0)
            if treechild is not None:
                pathtext = treechild.data(Qt.UserRole + udr.pathdisplayrole)
                checkstate = treechild.checkState()
                locntable = treechild.detailstable
                addedinfo = treechild.addedinfo

                if checkstate == Qt.Checked:
                    print(pathtext)
                    checkedlocations = []
                    for col in locntable.col_contents:
                        for it in col:
                            if it[1]:
                                checkedlocations.append(it[0])
                    print("detailed locations selected:", checkedlocations)
                    print(addedinfo)
            self.tempprinthelper(treechild)

    def updatelistdata(self, topLeft, bottomRight):
        startitem = self.itemFromIndex(topLeft)
        startitem.updatelistdata()

    def updateCheckState(self, item):
        thestate = item.checkState()
        if thestate == Qt.Checked:
            # TODO KV then the user must have checked it,
            #  so make sure to partially-fill ancestors and also look at ME siblings
            item.check(fully=True)
        elif thestate == Qt.PartiallyChecked:
            # TODO KV then the software must have updated it based on some other user action
            # make sure any ME siblings are unchecked
            item.check(fully=False)
        elif thestate == Qt.Unchecked:
            # TODO KV then either...
            # (1) the user unchecked it and we have to uncheck ancestors and look into ME siblings, or
            # (2) it was unchecked as a (previously partially-checked) ancestor of a user-unchecked node, or
            # (3) it was force-unchecked as a result of ME/sibling interaction
            item.uncheck(force=False)
        # if thestate in [Qt.Checked, Qt.PartiallyChecked]:
        #     item.check(thestate == Qt.Checked)
        # else:
        #     item.uncheck()

    def populate(self, parentnode, structure={}, pathsofar="", issubgroup=False, isfinalsubgroup=True, subgroupname=""):
        if structure == {} and pathsofar != "":
            # base case (leaf node); don't build any more nodes
            pass
        elif structure == {} and pathsofar == "":
            # no parameters; build a tree from the default structure
            # TODO KV define a default structure somewhere (see constant.py)
            if self.locationtype.usesbodylocations():
                self.populate(parentnode, structure=locn_options_body, pathsofar="")
            elif self.locationtype.purelyspatial:
                self.populate(parentnode, structure=locn_options_purelyspatial, pathsofar="")
        elif structure != {}:
            # internal node with substructure
            numentriesatthislevel = len(structure.keys())
            for idx, labelclassifierchecked_tuple in enumerate(structure.keys()):
                label = labelclassifierchecked_tuple[0]
                editable = labelclassifierchecked_tuple[1]
                classifier = labelclassifierchecked_tuple[2]
                checked = labelclassifierchecked_tuple[3]
                ishandloc = labelclassifierchecked_tuple[4] == h  # hand vs nonhand
                allowsurfacespec = labelclassifierchecked_tuple[5]
                surface_exceptions = labelclassifierchecked_tuple[6]
                allowsubareaspec = labelclassifierchecked_tuple[7]  # sub area or bone/joint
                subarea_exceptions = labelclassifierchecked_tuple[8]
                ismutuallyexclusive = classifier == rb
                iseditable = editable == ed
                if label == subgroup:

                    # make the tree items in the subgroup and whatever nested structure they have
                    isfinal = False
                    if idx + 1 >= numentriesatthislevel:
                        # if there are no more items at this level
                        isfinal = True
                    self.populate(parentnode, structure=structure[labelclassifierchecked_tuple], pathsofar=pathsofar, issubgroup=True, isfinalsubgroup=isfinal, subgroupname=subgroup + "_" + pathsofar + "_" + (str(classifier)))

                else:
                    # parentnode.setColumnCount(1)
                    thistreenode = LocationTreeItem(label, ishandloc=ishandloc, allowsurfacespec=allowsurfacespec, allowsubareaspec=allowsubareaspec, mutuallyexclusive=ismutuallyexclusive, surface_exceptions=surface_exceptions, subarea_exceptions=subarea_exceptions)
                    # thistreenode.setData(False, Qt.UserRole+udr.selectedrole)  #  moved to MovementTreeItem.__init__()
                    thistreenode.setData(pathsofar + label, role=Qt.UserRole+udr.pathdisplayrole)
                    thistreenode.setEditable(iseditable)
                    thistreenode.setCheckState(Qt.Checked if checked else Qt.Unchecked)
                    if issubgroup:
                        thistreenode.setData(subgroupname, role=Qt.UserRole+udr.subgroupnamerole)
                        if idx + 1 == numentriesatthislevel:
                            thistreenode.setData(True, role=Qt.UserRole+udr.lastingrouprole)
                            thistreenode.setData(isfinalsubgroup, role=Qt.UserRole+udr.finalsubgrouprole)
                    self.populate(thistreenode, structure=structure[labelclassifierchecked_tuple], pathsofar=pathsofar + label + delimiter)
                    parentnode.appendRow([thistreenode])

    @property
    def listmodel(self):
        if self._listmodel is None:
            self._listmodel = LocationListModel(self)
        return self._listmodel

    @listmodel.setter
    def listmodel(self, listmod):
        self._listmodel = listmod

    @property
    def locationtype(self):
        return self._locationtype

    @locationtype.setter
    def locationtype(self, locationtype):  # LocationType class
        self._locationtype = locationtype


class LocationTableView(QTableView):
    def __init__(self, locationtreeitem=None, **kwargs):
        super().__init__(**kwargs)

        # set the table model
        locntablemodel = LocationTableModel(parent=self)
        self.setModel(locntablemodel)
        self.horizontalHeader().resizeSections(QHeaderView.Stretch)


# This class is a serializable form of the class LocationTableModel, which is itself not pickleable.
# Rather than being based on QAbstractTableModel, this one uses the underlying lists from the
# LocationTableModel to convert to and from saveable form.
class LocationTableSerializable:

    def __init__(self, locntablemodel):
        # creates a full serializable copy of the location table, eg for saving to disk
        self.col_labels = locntablemodel.col_labels
        self.col_contents = locntablemodel.col_contents


class LocationTableModel(QAbstractTableModel):

    def __init__(self, loctext="", ishandloc=False, allowsurfacespec=True, allowsubareaspec=True,
                 serializedtablemodel=None, surface_exceptions=None, subarea_exceptions=None, **kwargs):
        super().__init__(**kwargs)

        if serializedtablemodel is not None:  # from saved table
            self.col_labels = serializedtablemodel.col_labels
            self.col_contents = serializedtablemodel.col_contents

        else:  # brand new
            self.col_labels = ["", ""]
            self.col_contents = [[], []]
            # self.col_checkstates = [[], []]

            if loctext == "":  # no location yet
                return

            if allowsurfacespec:
                self.col_labels[0] = surface_label
                if surface_exceptions is None:
                    surface_exceptions = []
                col_texts = surfaces_hand_default if ishandloc else surfaces_nonhand_default
                col_texts = [t for t in col_texts if t not in surface_exceptions]
                self.col_contents[0] = [[txt, False] for txt in col_texts]

            if allowsubareaspec:
                self.col_labels[1] = bonejoint_label if ishandloc else subarea_label
                if subarea_exceptions is None:
                    subarea_exceptions = []
                col_texts = bonejoint_hand_default if ishandloc else subareas_nonhand_default
                col_texts = [t for t in col_texts if t not in subarea_exceptions]
                self.col_contents[1] = [[txt, False] for txt in col_texts]

    # must implement! abstract parent doesn't define this behaviour
    def rowCount(self, parent=None, *args, **kwargs):
        return max([len(col) for col in self.col_contents])

    # must implement! abstract parent doesn't define this behaviour
    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.col_contents)

    # must implement! abstract parent doesn't define this behaviour
    def data(self, index, role=Qt.DisplayRole):
        # TODO KV make sure to deal with other potential roles as well
        if not index.isValid():
            return None
        try:
            if role == Qt.DisplayRole:
                return self.col_contents[index.column()][index.row()][0]
            elif role == Qt.CheckStateRole:
                checked = self.col_contents[index.column()][index.row()][1]
                return Qt.Checked if checked else Qt.Unchecked
        except IndexError:
            return None

    def setData(self, index, value, role=Qt.DisplayRole):
        if not index.isValid():
            return False
        if role == Qt.DisplayRole:
            self.col_contents[index.column()][index.row()][0] = value
        elif role == Qt.CheckStateRole:
            checked = value == Qt.Checked
            self.col_contents[index.column()][index.row()][1] = checked
        return True

    # TODO KV are all of these true?
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

    # must implement! abstract parent doesn't define this behaviour
    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.col_labels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None


class LocationListItem(QStandardItem):

    def __init__(self, pathtxt="", nodetxt="", treeit=None, serializedlistitem=None):
        super().__init__()

        if serializedlistitem:
            self.setEditable(serializedlistitem['editable'])
            self.setText(serializedlistitem['text'])
            self.setData(serializedlistitem['nodedisplayrole'], Qt.UserRole+udr.nodedisplayrole)
            self.setData(serializedlistitem['timestamprole'], Qt.UserRole+udr.timestamprole)
            self.setCheckable(serializedlistitem['checkable'])
            self.setData(serializedlistitem['selectedrole'], Qt.UserRole+udr.selectedrole)
        else:
            self.setEditable(False)
            self.setText(pathtxt)
            self.setData(nodetxt, Qt.UserRole+udr.nodedisplayrole)
            self.setData(QDateTime.currentDateTimeUtc(), Qt.UserRole+udr.timestamprole)
            self.setCheckable(False)
            self.treeitem = treeit
            if treeit is not None:
                self.treeitem.listitem = self
            self.setData(False, Qt.UserRole+udr.selectedrole)

    # def serialize(self):
    #     serialized = {
    #         'editable': self.isEditable(),
    #         'text': self.text(),
    #         'nodedisplayrole': self.data(Qt.UserRole+udr.nodedisplayrole),
    #         'timestamprole': self.data(Qt.UserRole+udr.timestamprole),
    #         'checkable': self.isCheckable(),
    #         'selectedrole': self.data(Qt.UserRole+udr.selectedrole)
    #     }
    #     return serialized

    def __repr__(self):
        return '<LocationListItem: ' + repr(self.text()) + '>'

    def updatetext(self, txt=""):
        self.setText(txt)

    def unselectpath(self):
        self.treeitem.uncheck()

    def selectpath(self):
        self.treeitem.check(fully=True)


class LocationPathsProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None, wantselected=None):
        super(LocationPathsProxyModel, self).__init__(parent)
        self.wantselected = wantselected
        self.setSortCaseSensitivity(Qt.CaseInsensitive)

    def filterAcceptsRow(self, source_row, source_parent):
        if self.wantselected is None:
            source_index = self.sourceModel().index(source_row, 0, source_parent)
            text = self.sourceModel().index(source_row, 0, source_parent).data()
            return True
        else:
            source_index = self.sourceModel().index(source_row, 0, source_parent)
            isselected = source_index.data(role=Qt.UserRole+udr.selectedrole)
            path = source_index.data(role=Qt.UserRole+udr.pathdisplayrole)
            text = self.sourceModel().index(source_row, 0, source_parent).data()
            return self.wantselected == isselected

    def updatesorttype(self, sortbytext=""):
        if "alpha" in sortbytext and "path" in sortbytext:
            self.setSortRole(Qt.DisplayRole)
            self.sort(0)
        elif "alpha" in sortbytext and "node" in sortbytext:
            self.setSortRole(Qt.UserRole+udr.nodedisplayrole)
            self.sort(0)
        elif "tree" in sortbytext:
            self.sort(-1)  # returns to sort order of underlying model
        elif "select" in sortbytext:
            self.setSortRole(Qt.UserRole+udr.timestamprole)
            self.sort(0)


class LocationGraphicsView(QGraphicsView):

    def __init__(self, app_ctx, frontorback='front', parent=None, viewer_size=400, specificpath=""):
        super().__init__(parent=parent)

        self.viewer_size = viewer_size

        self._scene = QGraphicsScene(parent=self)
        imagepath = app_ctx.default_location_images['body_hands_' + frontorback]
        if specificpath != "":
            imagepath = specificpath
        self._pixmap = QPixmap(imagepath)
        self._photo = QGraphicsPixmapItem(self._pixmap)
        # self._photo.setPixmap(QPixmap("gui/upper_body.jpg"))
        self._scene.addItem(self._photo)
        # self._scene.addPixmap(QPixmap("./body_hands_front.png"))
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.fitInView()

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            scenerect = self.transform().mapRect(rect)
            factor = min(self.viewer_size / scenerect.width(), self.viewer_size / scenerect.height())
            self.factor = factor
            # viewrect = self.viewport().rect()
            # factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
            self.scale(factor, factor)


class LocationListModel(QStandardItemModel):

    def __init__(self, treemodel=None):
        super().__init__()
        self.treemodel = treemodel
        if self.treemodel is not None:
            # build this listmodel from the treemodel
            treeparentnode = self.treemodel.invisibleRootItem()
            self.populate(treeparentnode)
            self.treemodel.listmodel = self

    # def serialize(self):
    #     serialized = []
    #     for rownum in range(self.rowCount()):
    #         serialized.append(self.item(rownum, 0).serialize())
    #     return serialized

    def populate(self, treenode):
        # colcount = 1  # TODO KV treenode.columnCount()
        for r in range(treenode.rowCount()):
            # for colnum in range(colcount):
            treechild = treenode.child(r, 0)
            if treechild is not None:
                pathtext = treechild.data(role=Qt.UserRole+udr.pathdisplayrole)
                nodetext = treechild.data(Qt.DisplayRole)
                listitem = LocationListItem(pathtxt=pathtext, nodetxt=nodetext, treeit=treechild)  # also sets treeitem's listitem
                self.appendRow(listitem)
                self.populate(treechild)

    def setTreemodel(self, treemod):
        self.treemodel = treemod


class TreeListView(QListView):

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        key = event.key()
        # modifiers = event.modifiers()

        if key == Qt.Key_Delete:
            indexesofselectedrows = self.selectionModel().selectedRows()
            selectedlistitems = []
            for itemindex in indexesofselectedrows:
                listitemindex = self.model().mapToSource(itemindex)
                listitem = self.model().sourceModel().itemFromIndex(listitemindex)
                selectedlistitems.append(listitem)
            for listitem in selectedlistitems:
                listitem.unselectpath()
            # self.model().dataChanged.emit()


def gettreeitemsinpath(treemodel, pathstring, delim="/"):
    pathlist = pathstring.split(delim)
    pathitemslists = []
    for level in pathlist:
        pathitemslists.append(treemodel.findItems(level, Qt.MatchRecursive))
    validpathsoftreeitems = findvaliditemspaths(pathitemslists)
    return validpathsoftreeitems[0]


def findvaliditemspaths(pathitemslists):
    validpaths = []
    if len(pathitemslists) > 1:  # the path is longer than 1 level
        # pathitemslistslotohi = pathitemslists[::-1]
        for lastitem in pathitemslists[-1]:
            for secondlastitem in pathitemslists[-2]:
                if lastitem.parent() == secondlastitem:
                    higherpaths = findvaliditemspaths(pathitemslists[:-2]+[[secondlastitem]])
                    for higherpath in higherpaths:
                        if len(higherpath) == len(pathitemslists)-1:  # TODO KV
                            validpaths.append(higherpath + [lastitem])
    elif len(pathitemslists) == 1:  # the path is only 1 level long (but possibly with multiple options)
        for lastitem in pathitemslists[0]:
            # if lastitem.parent() == .... used to be if topitem.childCount() == 0:
            validpaths.append([lastitem])
    else:
        # nothing to add to paths - this case shouldn't ever happen because base case is length==1 above
        # but just in case...
        validpaths = []

    return validpaths
