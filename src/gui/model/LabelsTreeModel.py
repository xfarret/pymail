from PyQt5.QtCore import (
    QAbstractItemModel, QModelIndex
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from OpenGL import GL

from manager.folder_manager import FolderManager


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        if isinstance(self.itemData, object):
            return 1
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class LabelsTreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(LabelsTreeModel, self).__init__(parent)

        self.rootItem = TreeItem(data, None)
        self.setup_model_data(data, self.rootItem)

    def setup_model_data(self, data, parent):
        """
        :param data:
        :param parent:
        :return:
        """
        labels = FolderManager.get_labels(data)
        for label in labels:
            parent.appendChild(TreeItem(label.name, parent))

    def rowCount(self, parent=None, *args, **kwargs):
        """
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=None, *args, **kwargs):
        """
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def index(self, row, column, parent):
        """
        :param row:
        :param column:
        :param parent:
        :return:
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index=None):
        """
        :param index:
        :return:
        """
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)
