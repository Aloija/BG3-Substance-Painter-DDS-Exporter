__author__ = "Emil Eldstål"
__copyright__ = "Copyright 2023, Emil Eldstål"
__version__ = "0.1.1"

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

import substance_painter.ui
import substance_painter.event

import os
import configparser
import subprocess
from pathlib import Path


def config_ini(overwrite):
    # Get the path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the StarfieldPluginSettings.ini file
    ini_file_path = os.path.join(script_dir, "BG3-DDS-Exporter-PluginSettings.ini")
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Check if the INI file exists
    if os.path.exists(ini_file_path):
        # Read the INI file
        config.read(ini_file_path)
        
        # Check if the section and key exist
        if 'General' in config and 'TexConvDirectory' in config['General']:
            # Check if the value is empty
            if not config['General']['TexConvDirectory']:
                # Let's the user choose where TexConv is if not configured
                config['General']['TexConvDirectory'] = choose_texconv_folder()
            if overwrite:
                # Let's the user choose where TexConv is if using overwrite button
                config['General']['TexConvDirectory'] = choose_texconv_folder()

            # Assign the TexConvDirectory value to the TexConvPath variable
            TexConvPath = config['General']['TexConvDirectory']
        else:
            TexConvPath = choose_texconv_folder()
            # If the section or key doesn't exist, create it and set the value
            config['General'] = {}
            config['General']['TexConvDirectory'] = TexConvPath
            print("BG3 DDS Exporter Plugin: TexConvDirectory value set or updated in BG3PluginSettings.ini")

        # Write the updated configuration back to the INI file
        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        TexConvPath = choose_texconv_folder()
        # If the INI file doesn't exist, create it and set the value
        with open(ini_file_path, 'w') as configfile:
            config['General'] = {}
            config['General']['TexConvDirectory'] = TexConvPath
            config.write(configfile)

    return TexConvPath


def choose_texconv_folder():
    path = QtWidgets.QFileDialog.getExistingDirectory(
    substance_painter.ui.get_main_window(),"Choose Texconv directory")
    return path +"/texconv.exe"


def convert_png_to_dds(texconvPath, sourcePNG, overwrite):
    # Replace backslashes with forward slashes in the provided paths
    texconvPath = texconvPath.replace('\\', '/')
    sourceFolder = os.path.dirname(sourcePNG)
    sourceFolder = sourceFolder.replace('\\', '/')
    outputFolder = sourceFolder + "/DDS/"

    isExist = os.path.exists(outputFolder)
    if not isExist:
        # Create the DDS directory if it does not exist
        os.makedirs(outputFolder)
        print("Created DDS subfolder")

    # for filename in os.listdir(sourceFolder):
    filename = sourcePNG
    if filename.endswith(".tga"):
        sourceFile = os.path.splitext(filename)[0]
        suffix = sourceFile.split('_')[-1]
        suffix = suffix.rstrip('_')

        outputFile = sourceFile + ".DDS"

        if suffix in ["BM", "NM", "HMVY", "CLEA"]:
            format_option = "BC3_UNORM"
        elif suffix in ["PM", "MSK", "GM"]:
            format_option = "BC1_UNORM"
        # If for some reason it's using some other suffix that's not supported
        else:
            format_option = "BC1_UNORM"

        format_option = format_option.rstrip('"')
        if overwrite:
            overwrite_option = "-y"
        else:
            overwrite_option = ""

        if outputFile:
            texconv_cmd = [
                texconvPath,
                "-nologo", overwrite_option,
                "-o", outputFolder,
                "-f", format_option,
                os.path.join(sourceFolder, filename)
            ]
            texconv_cmd_str = subprocess.list2cmdline(texconv_cmd)
            print(texconv_cmd_str)
            try:
                subprocess.run(texconv_cmd_str, shell=True, check=True)
                print(f"Successfully converted {filename} to {outputFile}")
            except subprocess.CalledProcessError:
                print(f"Failed to convert {filename}")

            convert_to_DDS(outputFolder)


def convert_to_DDS(path):

    export_folder = Path(path)

    for file in export_folder.iterdir():
        path = Path(file)
        path.rename(path.with_suffix('.DDS'))


class BG3DDSPlugin:
    def __init__(self):
        # Export boolean whether to add DDS creation or not
        self.export = True
        # Overwrites existing DDS files if checked
        self.overwrite = True
        # Plugin Version
        self.version = "0.1.1"

        # Create a dock widget to report plugin activity.
        self.log = QtWidgets.QTextEdit()
        self.window = QtWidgets.QWidget()
        self.TexConvPath = config_ini(False)

        layout = QtWidgets.QVBoxLayout()
        sub_layout = QtWidgets.QHBoxLayout()

        checkbox = QtWidgets.QCheckBox("Export DDS files")
        checkbox.setChecked(True)
        checkbox_overwrite = QtWidgets.QCheckBox("Overwrite DDS files")
        checkbox_overwrite.setChecked(True)
        button_texconv = QtWidgets.QPushButton("Choose Texconv location")
        button_clear = QtWidgets.QPushButton("Clear Log")

        version_label = QtWidgets.QLabel("Version: {}".format(self.version))

        # Adds buttons to sub-layout
        sub_layout.addWidget(checkbox)
        sub_layout.addWidget(checkbox_overwrite)
        sub_layout.addWidget(button_texconv)
        sub_layout.addWidget(button_clear)

        # Adds all widgets to main layout
        layout.addLayout(sub_layout)
        layout.addWidget(self.log)
        layout.addWidget(version_label)

        self.window.setLayout(layout)
        self.window.setWindowTitle("BG3 DDS Auto Converter")

        self.log.setReadOnly(True)

        # Connects buttons to click events
        checkbox.stateChanged.connect(self.checkbox_export_change)
        checkbox_overwrite.stateChanged.connect(self.checkbox_overwrite_change)
        button_texconv.clicked.connect(self.button_texconv_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)

        # Adds Qt as dockable widget to Substance Painter
        substance_painter.ui.add_dock_widget(self.window)

        self.log.append("TexConv Path: {}".format(self.TexConvPath))

        connections = {
            substance_painter.event.ExportTexturesEnded: self.on_export_finished
        }
        for event, callback in connections.items():
            substance_painter.event.DISPATCHER.connect(event, callback)

    def button_texconv_clicked(self):
        self.TexConvPath = config_ini(True)
        self.log.append("New TexConv Path: {}".format(self.TexConvPath))

    def button_clear_clicked(self):
        self.log.clear()

    def checkbox_export_change(self,state):
        if state == Qt.Checked:
            self.export = True
        else:
            self.export = False

    def checkbox_overwrite_change(self,state):
        if state == Qt.Checked:
            self.overwrite = True
        else:
            self.overwrite = False

    def __del__(self):
        # Remove all added UI elements.
        substance_painter.ui.delete_ui_element(self.log)
        substance_painter.ui.delete_ui_element(self.window)

    def on_export_finished(self, res):
        if(self.export):
            self.log.append(res.message)
            self.log.append("Exported files:")
            for file_list in res.textures.values():
                for file_path in file_list:
                    self.log.append("  {}".format(file_path))
                    
            self.log.append("Converting to DDS files:")
            for file_list in res.textures.values():
                for file_path in file_list:
                    convert_png_to_dds(self.TexConvPath,file_path,self.overwrite)
                    file_path = file_path[:-3]+"DDS"
                    self.log.append("  {}".format(file_path))

    def on_export_error(self, err):
        self.log.append("Export failed.")
        self.log.append(repr(err))


BG3_DDS_PLUGIN = None


def start_plugin():
    """This method is called when the plugin is started."""
    print ("BG3 DDS Exporter Plugin Initialized")
    global BG3_DDS_PLUGIN
    BG3_DDS_PLUGIN = BG3DDSPlugin()


def close_plugin():
    """This method is called when the plugin is stopped."""
    print ("BG3 DDS Exporter Plugin Shutdown")
    global BG3_DDS_PLUGIN
    del BG3_DDS_PLUGIN

if __name__ == "__main__":
    start_plugin()
