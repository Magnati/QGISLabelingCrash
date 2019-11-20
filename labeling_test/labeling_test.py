"""
/***************************************************************************
 Threader
                                 A QGIS plugin
 Bug example for threading crash on disco/qt5.12
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-15
        git sha              : $Format:%H$
        copyright            : (C) 2019 by F. Meckel
        email                : friedrich.meckel@ambrosys.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import pathlib

import PyQt5.QtGui
import qgis.core
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .dialog import Dialog
from .resources import *  # noqa
# Initialize Qt resources from file resources.py
# Import the code for the dialog


class LabelingTest:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.registry = qgis.core.QgsProject().instance()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = "LabelingTest"

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/threader/icon.png'
        self.add_action(
            icon_path,
            text='Threading Bug Example',
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                'LabelingTest',
                action)
            self.iface.removeToolBarIcon(action)

    def get_style_file(self, style_file):
        file_path = pathlib.Path(__file__).parent / style_file
        if file_path.is_file():
            return str(file_path)
        return None

    def _style_layer(self, layer, node, pos, style_file_name):
        style_path = self.get_style_file(style_file_name)
        node.insertChildNode(pos, qgis.core.QgsLayerTreeLayer(layer))
        if style_path:
            layer.loadNamedStyle(style_path)
        return layer

    def _add_layer_by_uri(
        self, uri_str, name, source, node, pos, style_file_name, constructor=None
    ):
        constructor = constructor or qgis.core.QgsVectorLayer
        print("_add_layer_by_uri: %s_uri: %s" % (name, uri_str))
        layer = constructor(uri_str, name, source)
        return self._style_layer(layer, node, pos, style_file_name)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start is True:
            self.first_start = False
            self.dlg = Dialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            root = self.registry.layerTreeRoot()
            shape_file = "matching.qml"
            layer = self._add_layer_by_uri(
                f"LineString?crs=EPSG:4326",
                "matching",
                "memory",
                root,
                0,
                shape_file,
            )
            color = PyQt5.QtGui.QColor(255, 0, 0)
            # changing the renderer works !
            layer.renderer().symbol().setColor(color)
            # But here it crashes
            layer.labeling().settings().format().background().setFillColor(color)
            self.registry.addMapLayer(layer, False)
            self.iface.layerTreeView().refreshLayerSymbology(layer.id())
