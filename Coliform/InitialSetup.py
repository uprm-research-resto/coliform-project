#!/usr/bin/env python3
#
# This is the dependencies and shortcut installer for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)


import os
from time import sleep


def installDependencies():
    print('Checking linux distribution...')
    os.system('lsb_release -a > ' + os.path.join(os.path.expanduser('~pi'), 'linux-release.txt'))

    print('Updating Raspberry Pi...')
    os.system('sudo apt-get update')
    os.system('sudo apt-get --yes --force-yes dist-upgrade')

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
    os.system('apt list --installed > ' + os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))
    os.system('pip3 list > ' + os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))

    f = open(os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))
    fpip = open(os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))
    flist = f.read()
    fpiplist = fpip.read()
    f.close()
    fpip.close()
    print('Installing missing dependencies...')
    if 'pyqt5' not in flist:
        print('Installing pyqt5...')
        os.system('sudo apt-get --yes --force-yes install python3-pyqt5 python3-pyqt5.qtopengl')

    if 'numpy' not in flist:
        if 'numpy' not in fpiplist:
            print('Installing numpy...')
            os.system('sudo apt-get --yes --force-yes install python3-numpy')

    if 'matplotlib' not in flist:
        if 'matplotlib' not in fpiplist:
            print('Installing matplotlib...')
            os.system('sudo apt-get --yes --force-yes install python3-matplotlib')

    if 'cairocffi' not in flist:
        if 'cairocffi' not in fpiplist:
            print('Installing cairocffi...')
            os.system('sudo apt-get --yes --force-yes install python3-cairocffi')

    if 'scipy' not in flist:
        if 'scipy' not in fpiplist:
            print('Installing scipy...')
            os.system('sudo apt-get --yes --force-yes install python3-scipy')

    print('Finished installing dependencies!')

    print('Removing temporary files...')
    os.remove(os.path.join(os.path.expanduser('~pi'), 'installed-packages.txt'))
    os.remove(os.path.join(os.path.expanduser('~pi'), 'pip-installed-packages.txt'))
    os.remove(os.path.join(os.path.expanduser('~pi'), 'linux-release.txt'))

    print('System will now attempt ot reboot, if its stuck on reboot, please disconnect and reconnect to power soruce.')
    print('System will reboot in 5 seconds...')
    sleep(5)
    os.system('sudo reboot')


def addShortcuts():
    print('Checking for executables...')
    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables')):
        os.mkdir(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables'))

    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'GUIExecutables', 'RunGUI.py')):
        print('Creating heater and pump control GUI executable...')
        exf1 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py'), 'w')
        exf1.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startGUI()\n')
        exf1.close()
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py'))

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py')):
        print('Creating camera control GUI executable...')
        exf2 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py'), 'w')
        exf2.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startCameraGUI()\n')
        exf2.close()
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py'))

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py')):
        print('Creating RGB sensor GUI executable...')
        exf3 = open(os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py'), 'w')
        exf3.write('#!/usr/bin/env python3\n'
                   'from Coliform import GUI\n'
                   'GUI.startRGBSensorGUI()\n')
        exf3.close()
        os.system('chmod +x ' + os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py'))

    print('Finished creating executables...')

    print('Checking for desktop shortcuts...')
    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'gui.desktop')):
        print('Creating control GUI desktop shortcut...')
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunGUI.py')
        dshort1 = open(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'gui.desktop'), 'w')
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
        dshort1.close()

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'cameragui.desktop')):
        print('Creating camera interface GUI desktop shortcut...')
        dshort2 = open(os.path.join(os.path.expanduser('~'), 'Desktop', 'cameragui.desktop'), 'w')
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunCameraGUI.py')
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
        dshort2.close()

    if not os.path.exists(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'rgbsensorgui.desktop')):
        print('Creating RGB sensor GUI desktop shortcut...')
        dshort3 = open(os.path.join(os.path.expanduser('~pi'), 'Desktop', 'rgbsensorgui.desktop'), 'w')
        path = os.path.join(os.path.expanduser('~pi'), 'GUIExecutables', 'RunRGBSensorGUI.py')
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
        dshort3.close()

    print('Shortcuts added to desktop!')
