<h1 align="center">
Baldur's Gate 3 Substance Painter DDS Exporter
</h1>


A Substance Painter DDS export plugin to automate the PNG to DDS conversion.

It's originally Starfield plugin I remade to fit Baldur's Gate 3 textures format.

# Installation:
Extract the bg3-dds-exporter.py into your Substance Painter Plugin folder:
<pre>
C:\Users\username\Documents\Adobe\Adobe Substance 3D Painter\python\plugins
</pre>

(Can also be found using the Python > Plugins Folder button in the top row)

Export your textures in .tga format with correct suffixes in a file name ("BM", "NM", "HMVY", "CLEA", "MSKA", "PM", "MSK", "GM")

## Enable the BG3-DDS-Exporter under the Python menu
First time running the plugin it will ask you what folder the Texconv.exe is located in via a UI pop-up. This will create a BG3-DDS-Exporter-PluginSettings.ini in the plugin folder with the settings saved.

## Export preset:
Move the BaldursGate3_Props.spexp and BaldursGate3_Skin.spexp to this folder:

C:\Users\username\Documents\Adobe\Adobe Substance 3D Painter\assets\export-presets

Add additional channels in Texture set settings like below:

For props (horns, outfits):

![image](https://github.com/Aloija/BG3-Substance-Painter-DDS-Exporter/assets/50318910/7abfedef-a8a0-4a84-bf79-d63b1e215629)

For skin: 

![image](https://github.com/Aloija/BG3-Substance-Painter-DDS-Exporter/assets/50318910/b620c377-2f6f-4997-8be0-6d0e3f9a0ec0)

# Dependencies:
Microsoft Texconv (Download and extract to whatever folder you want)

https://github.com/Microsoft/DirectXTex/wiki/Texconv

# Compatibility
Developed and tested with Substance Painter 9.1.1 (2023)

## Support
For support, please use this repository's GitHub Issues tracking service.

Copyright (c) 2023 Emil Eldstål, Aloija
