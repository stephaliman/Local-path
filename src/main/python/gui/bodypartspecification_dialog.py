from copy import deepcopy

from PyQt5.QtWidgets import (
    QFrame,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QDialogButtonBox,
    QLabel,
    QPushButton
)

from PyQt5.QtCore import (
    pyqtSignal
)

from gui.modulespecification_widgets import AddedInfoPushButton
from gui.locationspecification_view import LocationOptionsSelectionPanel
from models.location_models import BodypartTreeModel
from lexicon.module_classes import AddedInfo, delimiter, BodypartInfo
from constant import HAND, ARM, LEG
from serialization_classes import LocationTreeSerializable

bodypartpairs = {}
for part in [HAND, ARM, LEG]:
    for n in [1, 2]:
        bodypartpairs[part + str(n)] = part + str(3-n)


class BodypartSpecificationPanel(QFrame):
    copybutton_clicked = pyqtSignal()

    def __init__(self, bodypart, label, bodyparttype, bodypartinfotoload=None, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = self.parent().mainwindow
        self.bodyparttype = bodyparttype

        main_layout = QVBoxLayout()

        treemodel = BodypartTreeModel(bodyparttype=self.bodyparttype)
        treemodel.populate(treemodel.invisibleRootItem())
        addedinfo = AddedInfo()
        if bodypartinfotoload is not None and isinstance(bodypartinfotoload, BodypartInfo):
            # make a copy, so that the module is not being edited directly via this layout
            # (otherwise "cancel" doesn't actually revert to the original contents)
            if bodypartinfotoload.bodyparttreemodel is not None:
                treemodel = BodypartTreeModel(bodyparttype=self.bodyparttype, serializedlocntree=LocationTreeSerializable(bodypartinfotoload.bodyparttreemodel))
            addedinfo = deepcopy(bodypartinfotoload.addedinfo)

        # create layout with bodypart title and added info button
        title_and_addedinfo_layout = self.create_title_layout(bodypart, label, addedinfo)
        main_layout.addLayout(title_and_addedinfo_layout)

        # create panel containing search box, visual location selection (if applicable), list of selected options, and details table
        self.locationoptionsselectionpanel = LocationOptionsSelectionPanel(treemodeltoload=treemodel, displayvisualwidget=False, parent=self)
        main_layout.addWidget(self.locationoptionsselectionpanel)

        self.setLayout(main_layout)
        self.setEnabled(label is not None and label != "")

    def create_title_layout(self, bodypart, label, addedinfo):
        addedinfo = addedinfo or AddedInfo()

        title_and_addedinfo_layout = QHBoxLayout()

        in_brackets = label if (label is not None and label != "") else "not selected"
        title = bodypart + " (" + in_brackets + ")"

        title_label = QLabel(title)
        title_and_addedinfo_layout.addWidget(title_label)

        self.copy_button = QPushButton("Copy from " + bodypartpairs[bodypart])
        self.copy_button.clicked.connect(self.handle_copybutton_clicked)
        title_and_addedinfo_layout.addWidget(self.copy_button)

        title_and_addedinfo_layout.addStretch()
        self.addedinfobutton = AddedInfoPushButton("Notes")
        self.addedinfobutton.addedinfo = addedinfo
        title_and_addedinfo_layout.addWidget(self.addedinfobutton)
        # title_and_addedinfo_layout.setAlignment(addedinfobutton, Qt.AlignTop)

        return title_and_addedinfo_layout

    def handle_copybutton_clicked(self):
        self.copybutton_clicked.emit()

    def getbodypartinfo(self):
        return BodypartInfo(bodyparttype=self.bodyparttype, bodyparttreemodel=self.locationoptionsselectionpanel.treemodel, addedinfo=self.addedinfobutton.addedinfo)

    def setbodypartinfo(self, bodypartinfotoload):
        addedinfo = AddedInfo()
        if bodypartinfotoload is not None and isinstance(bodypartinfotoload, BodypartInfo):
            # make a copy, so that the module is not being edited directly via this layout
            # (otherwise "cancel" doesn't actually revert to the original contents)
            treemodel = BodypartTreeModel(bodyparttype=self.bodyparttype, serializedlocntree=LocationTreeSerializable(bodypartinfotoload.bodyparttreemodel))
            addedinfo = deepcopy(bodypartinfotoload.addedinfo)
        else:
            treemodel = BodypartTreeModel(bodyparttype=self.bodyparttype)
            treemodel.populate(treemodel.invisibleRootItem())

        # TODO KV this seems like too much detail to be handling at this level
        self.locationoptionsselectionpanel.treemodel = treemodel
        self.locationoptionsselectionpanel.refresh_listproxies()
        self.locationoptionsselectionpanel.update_detailstable()
        self.addedinfobutton.addedinfo = addedinfo

    def clear(self):
        treemodel = BodypartTreeModel(bodyparttype=self.bodyparttype)
        treemodel.populate(treemodel.invisibleRootItem())
        self.locationoptionsselectionpanel.treemodel = treemodel
        self.locationoptionsselectionpanel.refresh_listproxies()
        self.locationoptionsselectionpanel.clear_details()


class BodypartSelectorDialog(QDialog):
    bodyparts_saved = pyqtSignal(BodypartInfo, BodypartInfo)

    def __init__(self, bodyparttype, bodypart1label=None, bodypart2label=None, bodypart1infotoload=None, bodypart2infotoload=None, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = self.parent().mainwindow
        self.bodyparttype = bodyparttype

        main_layout = QVBoxLayout()
        hands_layout = QHBoxLayout()

        self.bodypart1_panel = BodypartSpecificationPanel(self.bodyparttype+'1', bodypart1label, bodyparttype=self.bodyparttype, bodypartinfotoload=bodypart1infotoload, parent=self)
        self.bodypart2_panel = BodypartSpecificationPanel(self.bodyparttype+'2', bodypart2label, bodyparttype=self.bodyparttype, bodypartinfotoload=bodypart2infotoload, parent=self)
        self.bodypart1_panel.copybutton_clicked.connect(lambda: self.bodypart1_panel.setbodypartinfo(self.bodypart2_panel.getbodypartinfo()))
        self.bodypart2_panel.copybutton_clicked.connect(lambda: self.bodypart2_panel.setbodypartinfo(self.bodypart1_panel.getbodypartinfo()))

        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)

        hands_layout.addWidget(self.bodypart1_panel)
        hands_layout.addWidget(vertical_line)
        hands_layout.addWidget(self.bodypart2_panel)
        main_layout.addLayout(hands_layout)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(horizontal_line)

        buttons = QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons, parent=self)
        self.button_box.clicked.connect(self.handle_button_click)

        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        # self.setMinimumSize(QSize(500, 700))
        # # self.setMinimumSize(modulelayout.desiredwidth(), modulelayout.desiredheight())
        # self.setMinimumSize(QSize(modulelayout.rect().width(), modulelayout.rect().height()))
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.adjustSize()

    def handle_button_click(self, button):
        standard = self.button_box.standardButton(button)

        if standard == QDialogButtonBox.Cancel:
            self.reject()

        elif standard == QDialogButtonBox.Save:

            # save info and then close dialog
            self.bodyparts_saved.emit(self.bodypart1_panel.getbodypartinfo(), self.bodypart2_panel.getbodypartinfo())
            self.accept()

        elif standard == QDialogButtonBox.RestoreDefaults:
            # TODO KV -- where should the "defaults" be defined?
            self.bodypart1_panel.clear()
            self.bodypart2_panel.clear()
