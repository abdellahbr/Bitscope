#!/bin/bash

if [ -e /usr/lib/python2.7 ]
then

  if [ $(uname --machine) == "x86_64" ]
  then
  # mettre installation de la bitlib
  echo "Archi 64 bit détecté"
  fi
  sudo cp Modules/TR_Acquisition.py /usr/lib/python2.7 
  sudo cp Modules/Acquisition.py  /usr/lib/python2.7
else
  echo "La version 2.7 de python est requise, elle ne semble pas être installé sur votre distribution linux"
fi


