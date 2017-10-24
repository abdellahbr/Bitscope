#!bin/bash
#Permet de commit en une seul ligne tout le projet par appel dans le dossier de : bash nomfichier.sh
git add --all
git commit -m $1
git push origin master
