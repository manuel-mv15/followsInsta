# Instagram Follow Analyzer

Este conjunto de scripts permite analizar tus conexiones de Instagram para identificar quién no te sigue de vuelta, a quién no sigues de vuelta y tus seguidores mutuos. Funciona procesando los archivos HTML exportados desde la herramienta "Descargar tu información" de Instagram.

## Características

*   **Análisis de Seguidores/Siguiendo**: Genera listas comparativas.
*   **Identificación de "Fans"**: Personas que te siguen pero tú no sigues.
*   **Identificación de "No Follow Back"**: Personas que sigues pero no te siguen de vuelta.
*   **Apertura Automática**: Ayudante para abrir perfiles en el navegador rápidamente.

## Requisitos

*   Python 3 instalado en tu sistema.
*   No requiere librerías externas (solo usa módulos estándar de Python).

## Instalación y Configuración

1.  **Clona o descarga este repositorio**.

2.  **Descarga tu información de Instagram**:
    *   Ve a **Tu actividad** > **Descargar tu información**.
    *   Solicita una descarga en formato **HTML**.
    *   Cuando la descarga esté lista, descomprime el archivo ZIP.

3.  **Coloca los archivos**:
    *   Busca la carpeta `connections` dentro de los archivos descomprimidos.
    *   Copia la carpeta `connections` completa a la raíz de este proyecto (donde están los scripts `.py`).
    *   Asegúrate de que la estructura de carpetas sea exactamente así:
        ```
        proyecto/
        ├── analyze_instagram.py
        ├── open_profiles.py
        └── connections/
            └── followers_and_following/
                ├── following.html
                └── followers_1.html
        ```

## Uso

### Paso 1: Analizar las conexiones

Ejecuta el script de análisis para generar las listas:

```bash
python3 analyze_instagram.py
```

Esto generará los siguientes archivos de texto:
*   `followers.txt`: Todos los que te siguen.
*   `following.txt`: Todos los que sigues.
*   `me_siguen_no_sigo.txt`: **"Fans"** (Te siguen, tú no).
*   `sigo_no_me_siguen.txt`: **"No Follow Back"** (Sigues, no te siguen).

### Paso 2: Abrir perfiles (Opcional)

Si deseas revisar los perfiles (por ejemplo, para dejar de seguir a quienes no te siguen), usa el script auxiliar:

```bash
python3 open_profiles.py
```

1.  El script listará los archivos `.txt` generados.
2.  Selecciona el número del archivo que quieres procesar (ej. el de "sigo_no_me_siguen").
3.  Elige el modo:
    *   **Modo 1**: Abrir perfiles uno por uno presionando Enter.
    *   **Modo 2**: Abrir todos los perfiles en pestañas del navegador (¡Úsalo con precaución si son muchos!).

## Notas Importantes

*   Asegúrate de que la ruta de los archivos HTML coincida con lo esperado por el script (`connections/followers_and_following/`). Si Instagram cambia la estructura de carpetas en el futuro, podrías necesitar ajustar las rutas en `analyze_instagram.py`.
