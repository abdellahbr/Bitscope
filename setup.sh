#!/bin/bash

if [ -e /usr/lib/python2.7 ]
then

  if [ -e /usr/share/doc/bitscope-library/examples/python/python-bindings-2.0-DC01L ]
  then
    echo "Une version de Bitlib est déja installé sur votre ordinateur"
  else
    if [ $(uname --machine) =~ "arm" ]
    then
    echo "Intstalation de Bitlib pour processeurs ARM..."
    sudo dpkg -i Bitlib/DEB_ARM/bitscope-link_1.1.FG14A_armhf.deb
    sudo dpkg -i Bitlib/DEB_ARM/bitscope-library_2.0.FE26B_armhf.deb
    sudo unzip python-bindings-2.0-DC01L.zip -d /usr/share/doc/bitscope-library/examples/python/
    sudo BASECFLAGS="" OPT="" CFLAGS="-O3" python /usr/share/doc/bitscope-library/examples/python/setup-bitlib.py install
    fi
    if [ $(uname --machine) == "x86_64" ]
    then
    echo "Intstalation de Bitlib pour processeurs Intel 64 bits"
    sudo dpkg -i Bitlib/DEB_64/bitscope-link_1.1.FG14A_amd64.deb
    sudo dpkg -i Bitlib/DEB_64/bitscope-library_2.0.FE26B_amd64.deb
    sudo unzip python-bindings-2.0-DC01L.zip -d /usr/share/doc/bitscope-library/examples/python/
    sudo BASECFLAGS="" OPT="" CFLAGS="-O3" python /usr/share/doc/bitscope-library/examples/python/setup-bitlib.py install
    fi
    if [ $(uname --machine) == "x86" ]
    then
    echo "Instalation de Bitlib pour processeurs Intel 32 bits"
    sudo dpkg -i Bitlib/DEB_32/bitscope-link_1.1.FG14A_i386.deb
    sudo dpkg -i Bitlib/DEB_32/bitscope-library_2.0.FE26B_i386.deb
    sudo unzip python-bindings-2.0-DC01L.zip -d /usr/share/doc/bitscope-library/examples/python/
    sudo BASECFLAGS="" OPT="" CFLAGS="-O3" python /usr/share/doc/bitscope-library/examples/python/setup-bitlib.py install
    fi
  fi
  sudo cp Modules/TR_Acquisition.py /usr/lib/python2.7 
  echo "Copie de Modules/TR_Acquisition.py ....."
  sudo cp Modules/Acquisition.py  /usr/lib/python2.7
  echo "Copie de Modules/Acquisition.py ....."
  echo "Instalation réussi !"
else
  echo "La version 2.7 de python est requise, elle ne semble pas être installé sur votre distribution linux"
fi


