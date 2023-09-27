# try:
#     from PyQt6 import QtWidgets, QtCore, QtGui, Qt, QtWebEngineWidgets
#     from PyQt6.QtGui import QAction
# except ImportError as e:
#     print("error importing from PyQt6:")
#     print(e)
#     print("importing from PyQt5 instead")
#     from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtWebEngineWidgets
#     from PyQt5.QtWidgets import QAction

try:
    from PyQt6.QtCore import (
        Qt,
        QSize,
        QSettings,
        QPoint,
        pyqtSignal,
        QItemSelectionModel,
        QSortFilterProxyModel,
        QDateTime,
        QEvent,
        QAbstractTableModel,
        QRectF,
        QUrl,
        pyqtSlot,
        QMimeData,
        QParallelAnimationGroup,
        QPropertyAnimation,
        QAbstractAnimation,
        QRect,
        QAbstractListModel,
    )
    from PyQt6.QtWidgets import (
        QFileDialog,
        QMainWindow,
        QToolBar,
        QStatusBar,
        QScrollArea,
        QMessageBox,
        QUndoStack,
        QMdiArea,
        QMdiSubWindow,
        QWidget,
        QDialog,
        QGridLayout,
        QToolButton,
        QFrame,
        QDialogButtonBox,
        QLabel,
        QLineEdit,
        QListView,
        QVBoxLayout,
        QHBoxLayout,
        QComboBox,
        QWidget,
        QWidgetAction,
        QLineEdit,
        QHBoxLayout,
        QMenu,
        QCheckBox,
        QPushButton,
        QLabel,
        QComboBox,
        QBoxLayout,
        QButtonGroup,
        QRadioButton,
        QGroupBox,
        QSpacerItem,
        QSizePolicy,
        QAbstractButton,
        QGraphicsView,
        QAbstractItemView,
        QGraphicsRectItem,
        QGraphicsScene,
        QGraphicsEllipseItem,
        QTreeView,
        QCompleter,
        QStyledItemDelegate,
        QStyle,
        QStyleOptionButton,
        QApplication,
        QHeaderView,
        QStyleOptionFrame,
        QTableView,
        QGraphicsPixmapItem,
        QStackedWidget,
        QSlider,
        QTabWidget,
        QUndoCommand,
        QTabBar,
        QSpinBox,
        QGraphicsPolygonItem,
        QGraphicsTextItem,
        QColorDialog,
        QTableWidget,
        QTableWidgetItem,
        QFormLayout,
        QPlainTextEdit,
    )
    from PyQt6.QtGui import (
        QIcon,
        QKeySequence,
        QStandardItemModel,
        QStandardItem,
        QBrush,
        QColor,
        QPen,
        QTextOption,
        QPixmap,
        QDrag,
        QImage,
        QPainter,
        QPolygonF
    )
    from PyQt6.QtWebEngineWidgets import QWebEngineView


except ImportError as e:
    print("error importing from PyQt6:")
    print(e)
    print("importing from PyQt5 instead")
    
    from PyQt5.QtCore import (
        Qt,
        QSize,
        QSettings,
        QPoint,
        pyqtSignal,
        QItemSelectionModel,
        QSortFilterProxyModel,
        QDateTime,
        QEvent,
        QAbstractTableModel,
        QRectF,
        QUrl,
        pyqtSlot,
        QMimeData,
        QParallelAnimationGroup,
        QPropertyAnimation,
        QAbstractAnimation,
        QRect,
        QAbstractListModel,
    )
    from PyQt5.QtWidgets import (
        QFileDialog,
        QMainWindow,
        QToolBar,
        QStatusBar,
        QAction,
        QScrollArea,
        QMessageBox,
        QUndoStack,
        QMdiArea,
        QMdiSubWindow,
        QWidget,
        QDialog,
        QGridLayout,
        QToolButton,
        QFrame,
        QDialogButtonBox,
        QLabel,
        QLineEdit,
        QListView,
        QVBoxLayout,
        QHBoxLayout,
        QComboBox,
        QWidgetAction,
        QLineEdit,
        QFrame,
        QHBoxLayout,
        QMenu,
        QCheckBox,
        QPushButton,
        QLabel,
        QComboBox,
        QBoxLayout,
        QButtonGroup,
        QRadioButton,
        QGroupBox,
        QSpacerItem,
        QSizePolicy,
        QAbstractButton,
        QGraphicsView,
        QAbstractItemView,
        QGraphicsRectItem,
        QGraphicsScene,
        QGraphicsEllipseItem,
        QTreeView,
        QCompleter,
        QStyledItemDelegate,
        QStyle,
        QStyleOptionButton,
        QApplication,
        QHeaderView,
        QStyleOptionFrame,
        QTableView,
        QGraphicsPixmapItem,
        QStackedWidget,
        QSlider,
        QTabWidget,
        QUndoCommand,
        QTabBar,
        QSpinBox,
        QGraphicsPolygonItem,
        QGraphicsTextItem,
        QColorDialog,
        QTableWidget,
        QTableWidgetItem,
        QFormLayout,
        QPlainTextEdit,
    )
    from PyQt5.QtGui import (
        QIcon,
        QKeySequence,
        QStandardItemModel,
        QStandardItem,
        QBrush,
        QColor,
        QPen,
        QTextOption,
        QPixmap,
        QDrag,
        QImage,
        QPainter,
        QPolygonF
    )
    from PyQt5.QtWebEngineWidgets import QWebEngineView

