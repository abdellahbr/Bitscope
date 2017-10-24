#!bin/bash
#Permet de commit en une seul ligne tout le projet par appel dans le dossier de : bash nomfichier.sh
git add Acquisition.py
git add Test.py
git add EasyCommit.sh
git commit -m $1
git push origin master
