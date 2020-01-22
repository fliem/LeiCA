# CPAC Image Resources installation script
# script usage: ./install_resources.sh 
# Note: Will not work if FSLDIR is unset.

cp -n MNI_3mm/* $FSLDIR/data/standard
cp -n symmetric/* $FSLDIR/data/standard
cp -nr tissuepriors/2mm $FSLDIR/data/standard/tissuepriors
cp -nr tissuepriors/3mm $FSLDIR/data/standard/tissuepriors
cp -n HarvardOxford-lateral-ventricles-thr25-2mm.nii.gz $FSLDIR/data/atlases/HarvardOxford
