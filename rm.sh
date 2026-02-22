#!/bin/bash

# 1. Activamos las opciones extendidas de Bash
shopt -s extglob

# 2. Ejecutamos el borrado ignorando tus archivos importantes
# La sintaxis !(file1|file2) significa "todo lo que NO sea esto"
rm -rf !(.git|.gitignore|analyze_instagram.py|open_profiles.py|README.md|rm.sh)

# 3. Desactivamos la opción (opcional, por limpieza)
shopt -u extglob

echo "Limpieza completada: Solo quedan tus archivos de código y configuración."