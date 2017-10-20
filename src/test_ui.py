from PyQt5.QtCore import (
    QUrl
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from OpenGL import GL

from db.engine import DbEngine
from gui.model.LabelsTreeModel import LabelsTreeModel
from manager.account_manager import AccountManager
from manager.folder_manager import FolderManager

import sys

session = DbEngine.get_session()
account = AccountManager.get_instance().get(1)

app = QGuiApplication(sys.argv)
view = QQuickView()

labelsTreeModel = LabelsTreeModel(account)

root_context = view.rootContext().setContextProperty('treemodel', labelsTreeModel)
view.setSource(QUrl.fromLocalFile('gui/view/simpletreemodel.qml'))
view.show()
sys.exit(app.exec_())

