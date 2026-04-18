# Ce fichier est conservé pour compatibilité.
# Le vrai point d'entrée est maintenant : aisatou.py
#
# Lance : python aisatou.py  (ou python aisatou.py --voice)

import subprocess, sys
subprocess.run([sys.executable, "aisatou.py"] + sys.argv[1:])
