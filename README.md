

This is a reproduction example for the [issue 32970](https://github.com/qgis/QGIS/issues/32970).


### Run QGIS with installed plugin - on Ubuntu

If qgis is installed it might be sufficiant to execute 
```bash
QGIS_PLUGINPATH=$(pwd)/ qgis
```
from within the repository.

Then go to the plugin menu and install `Labeling Test` and execute the plugin from the appearing icon in the toolbar.

If the PyQt libraries cannot be found it might be solved by starting qgis with the following command instead. 
```bash
PATH=/usr/bin:${PATH} QGIS_PLUGINPATH=$(pwd)/ qgis
```

The [PluginBuilder](https://plugins.qgis.org/plugins/pluginbuilder/) was used as a base start for this example.