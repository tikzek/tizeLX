# tizeLX
Installing TizeLX on Kali Linux

First, open a terminal (Ctrl + Alt + T). Ensure your system is updated with sudo apt update && sudo apt upgrade -y.

Clone the TizeLX repository using:
git clone https://github.com/tu_usuario/tizelx.git

Navigate into the folder:
cd tizelx

Make the installer executable and run it:
chmod +x install.sh && sudo ./install.sh

Once installed, launch TizeLX by simply typing tizelx in your terminal. The application will start with its graphical interface by default (use tizelx --cli for command-line mode).

To uninstall, run the included removal script:
sudo /opt/tizelx/uninstall.sh

This tool requires Python 3 and works best on Kali Linux but may also function on other Debian-based distributions. For troubleshooting, check the project's GitHub wiki or submit an issue
Usage:tizelx(GUI)ortizelx--cli(command-line).Browse/applythemes,customizecolors/fonts,editprompt,managealiases.Seechangesinstantly.Use"SaveProfile"tokeepchanges.tizelx--helpforoptions.Autobackupsin~/.config/tizelx/backups/.(298chars)

Or even more compressed:

Use:Runtizelx,picktheme,adjustsettings,saveprofile.tizelx--cliforterminalmode.Changesapplylive.--helpformore.(149chars)

