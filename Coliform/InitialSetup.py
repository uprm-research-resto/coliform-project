#!/usr/bin/env python3
#
# This is the dependencies and shortcut installer for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)

# Imports
import os  # used for os operations and 'sending' commands through terminal
from time import sleep  # used for delays


def installDependencies():  # function installs dependencies for Coliform library in raspberry pi
    print('Checking linux distribution...')
    os.system('lsb_release -a > ' + os.path.join(os.path.expanduser('~pi'), 'linux-release.txt'))  # checks linux distribution by searching the release file

    print('Updating Raspberry Pi...')
    os.system('sudo apt-get update')  # updates all installed packages
    os.system('sudo apt-get --yes --force-yes dist-upgrade')  # updates linux distribution

    # def firwareUpdate():
    #     def start():
    #         fupdate = input('Do you want to update Raspberry Pi firmware, this will take more time?(y/n)')
    #         if fupdate in ['y', 'Y']:
    #             print('Updating Raspberry Pi firmware...')
    #             os.system('sudo rpi-update')
    #         elif fupdate in ['n', 'N']:
    #             pass
    #         else:
    #             print('Please type "y" or "n"')
    #             start()
    #     start()
    #
    # firwareUpdate()

    print('Loading installed packages...')
    os.system('apt list --installed > ' + os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))  # looks for debian installed packages and adds to file 'installed-packages.txt'
    os.system('pip3 list > ' + os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))  # looks for pip installed packages and adds to file 'pip-installed-packages.txt'

    f = open(os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))  # opens debian installed packages file, which was created previously at line 39
    fpip = open(os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))  # opens pip installed packages file, which was created previously at line 40
    flist = f.read()  # reads debian packages files and adds to list variable
    fpiplist = fpip.read()  # reads pip list files and adds to list variable
    f.close()  # close debian packages list file
    fpip.close()  # close pip list file
    print('Installing missing dependencies...')
    if 'pyqt5' not in flist:  # searches for 'pyqt5' in list and installs if not found
        print('Installing pyqt5...')
        os.system('sudo apt-get --yes --force-yes install python3-pyqt5 python3-pyqt5.qtopengl')  # send install command

    if 'numpy' not in flist:  # searches for 'numpy' in debian installed modules list variable and installs if not found
        if 'numpy' not in fpiplist:  # searches for 'numpy' in pip installed modules list variable, and install if not found
            print('Installing numpy...')
            os.system('sudo apt-get --yes --force-yes install python3-numpy')  # send intall command

    if 'matplotlib' not in flist:  # searches for 'matplotlib' in debian installed modules list variable and installs if not found
        if 'matplotlib' not in fpiplist:  # searches for 'matplotlib' in pip installed modules list variable, and install if not found
            print('Installing matplotlib...')
            os.system('sudo apt-get --yes --force-yes install python3-matplotlib')  # send install command

    if 'cairocffi' not in flist:  # searches for 'cairoffci' in debian installed modules list variable and installs if not found
        if 'cairocffi' not in fpiplist:  # searches for 'cairoffci' in pip installed modules list variable, and install if not found
            print('Installing cairocffi...')
            os.system('sudo apt-get --yes --force-yes install python3-cairocffi')  # send install command

    if 'scipy' not in flist:  # searches for 'scipy' in debian installed modules list variable and installs if not found
        if 'scipy' not in fpiplist:  # searches for 'scipy' in pip installed modules list variable, and install if not found
            print('Installing scipy...')
            os.system('sudo apt-get --yes --force-yes install python3-scipy')  # send install command

    if 'pyserial' not in flist:  # searches for 'pyserial' in debian installed modules list variable and installs if not found
        if 'pyserial' not in fpiplist:  # searches for 'pyserial' in pip installed modules list variable, and install if not found
            print('Installing pyserial...')
            os.system('sudo apt-get --yes --force-yes install python3-serial')  # send install command
    if 'Adafruit_TCS34725' not in flist:  # searches for 'Adafruit_TCS34725' in debian installed modules list variable and installs if not found
        if 'Adafruit_TCS34725' not in fpiplist:  # searches for 'Adafruit_TCS34725' in pip installed modules list variable, and install if not found
            print('Installing Adafruit_TCS34725...')
            os.system('sudo pip3 install Adafruit_TCS34725')  # sends install command

    print('Finished installing dependencies!')

    print('Removing temporary files...')
    # These remove temporary files created during installation
    os.remove(os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))
    os.remove(os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))
    os.remove(os.path.join(os.path.expanduser('~pi'), 'linux-release.txt'))

    print('System will now attempt ot reboot, if its stuck on reboot, please disconnect and reconnect to power soruce.')
    print('System will reboot in 5 seconds...')
    sleep(5)  # program waits for 5 seconds
    os.system('sudo reboot')  # sends reboot command


def addShortcuts():  # adds gui shortcuts to desktop
    print('Checking for executables...')
    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables')):  # checks if executables directory is created
        os.mkdir(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables'))  # creates directory if not found

    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'GUIExecutables', 'RunGUI.py')):  # Checks if python executable exists
        print('Creating heater and pump control GUI executable...')
        exf1 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py'), 'w')  # creates python executable if not found
        # write to shortcut file
        exf1.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startGUI()\n')
        exf1.close()  # closes shortcut file
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py'))  # marks file as executable

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py')):  # Checks if python executable exists
        print('Creating camera control GUI executable...')
        exf2 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py'), 'w')  # creates python executable if not found
        exf2.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startCameraGUI()\n')
        exf2.close()  # closes shortcut file
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py'))  # marks file as executable

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py')):  # Checks if python executable exists
        print('Creating RGB sensor GUI executable...')
        exf3 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py'), 'w')  # creates python executable if not found
        exf3.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startRGBSensorGUI()\n')
        exf3.close()  # closes shortcut file
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py'))  # marks file as executable

    print('Finished creating executables...')

    print('Checking for desktop shortcuts...')
    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'gui.desktop')):  # Checks if shortcut exists
        print('Creating control GUI desktop shortcut...')
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py')  # adds path to executable to variable
        dshort1 = open(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'gui.desktop'), 'w')  # create desktop shortcut file
        # Write to desktop shortcut file
        dshort1.write('[Desktop Entry]\n'
                      'Name=Control GUI\n'
                      'Comment=Pump and heater control GUI\n'
                      'TryExec=' + path + '\n'
                      'Exec=' + path + '\n'
                      'Terminal=false\n'
                      'Type=Application\n'
                      'StartupNotify=true\n'
                      'Icon=/usr/share/pixmaps/idle3.xpm\n'
                      'Categories=Application;Development;\n')
        dshort1.close()  # close shortcut file

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'cameragui.desktop')):  # Checks if shortcut exists
        print('Creating camera interface GUI desktop shortcut...')
        dshort2 = open(os.path.join(os.path.expanduser('~'), 'Desktop', 'cameragui.desktop'), 'w')  # create desktop shortcut file
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py')  # adds executable to variable
        # writes to desktop shortcut file
        dshort2.write('[Desktop Entry]\n'
                      'Name=Camera Interface GUI\n'
                      'Comment=Camera interface control GUI\n'
                      'TryExec=' + path + '\n'
                      'Exec=' + path + '\n'
                      'Terminal=false\n'
                      'Type=Application\n'
                      'StartupNotify=true\n'
                      'Icon=/usr/share/pixmaps/idle3.xpm\n'
                      'Categories=Application;Development;\n')
        dshort2.close()  # closes desktop shortcut file

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'rgbsensorgui.desktop')):  # Checks if shortcut exists
        print('Creating RGB sensor GUI desktop shortcut...')
        dshort3 = open(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'rgbsensorgui.desktop'), 'w')  # create desktop shortcut file
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py')  # adds executable to variable
        # writes to desktop shortcut file
        dshort3.write('[Desktop Entry]\n'
                      'Name=RGB Sensor GUI\n'
                      'Comment=RGB Sensor GUI interfase\n'
                      'TryExec=' + path + '\n'
                      'Exec=' + path + '\n'
                      'Terminal=false\n'
                      'Type=Application\n'
                      'StartupNotify=true\n'
                      'Icon=/usr/share/pixmaps/idle3.xpm\n'
                      'Categories=Application;Development;\n')
        dshort3.close()  # close desktop shortcut file

    print('Shortcuts added to desktop!')
