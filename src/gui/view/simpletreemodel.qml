import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQml.Models 2.2

Rectangle {
    width: 480
    height: 640

    TreeView {
        id: treeView
        anchors.fill: parent
        anchors.margins: 6
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter

        model: treemodel

        TableViewColumn {
            title: "Label"
            role: "LabelRole"
            resizable: true
        }
    }
}