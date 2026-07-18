#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import glob

# Mapeo de categorías con emojis para una interfaz bonita
CATEGORIES_MAPPING = {
    "top10": "⭐ Herramientas Top 10",
    "01": "🔍 01 - Recopilación de Información",
    "02": "🛡️ 02 - Análisis de Vulnerabilidades",
    "03": "🌐 03 - Análisis de Aplicaciones Web",
    "04": "🗄️ 04 - Evaluación de Bases de Datos",
    "05": "🔑 05 - Ataques de Contraseñas",
    "06": "📶 06 - Ataques Inalámbricos",
    "07": "💻 07 - Ingeniería Inversa",
    "08": "💥 08 - Herramientas de Explotación",
    "09": "🕵️ 09 - Sniffing y Spoofing",
    "10": "🚪 10 - Post-Explotación",
    "11": "🔎 11 - Análisis Forense",
    "12": "📝 12 - Herramientas de Reportes",
    "13": "👥 13 - Ingeniería Social",
    "14": "🤖 14 - Inteligencia Artificial",
    "cryptography": "🔐 Criptografía",
    "privacy": "👁️ Privacidad",
    "Development": "🛠️ Desarrollo",
    "System": "⚙️ Sistema",
    "Utility": "🔧 Utilidades y Accesorios",
    "Network": "🔌 Red / Conectividad",
    "WebBrowser": "🌍 Internet y Navegación",
    "Graphics": "🎨 Gráficos y Diseño",
    "AudioVideo": "🎬 Multimedia / Audio y Video",
    "Office": "📁 Oficina y Documentos",
}

# Iconos por defecto para las categorías en Rofi
CATEGORY_ICONS = {
    "⭐ Herramientas Top 10": "favorites",
    "🔍 01 - Recopilación de Información": "system-search",
    "🛡️ 02 - Análisis de Vulnerabilidades": "security-high",
    "🌐 03 - Análisis de Aplicaciones Web": "browser",
    "🗄️ 04 - Evaluación de Bases de Datos": "server-database",
    "🔑 05 - Ataques de Contraseñas": "password",
    "📶 06 - Ataques Inalámbricos": "network-wireless",
    "💻 07 - Ingeniería Inversa": "devel",
    "💥 08 - Herramientas de Explotación": "reaper",
    "🕵️ 09 - Sniffing y Spoofing": "network-wired",
    "🚪 10 - Post-Explotación": "backdoor",
    "🔎 11 - Análisis Forense": "search",
    "📝 12 - Herramientas de Reportes": "report",
    "👥 13 - Ingeniería Social": "users",
    "🤖 14 - Inteligencia Artificial": "brain",
    "🔐 Criptografía": "lock",
    "👁️ Privacidad": "visibility-off",
    "🛠️ Desarrollo": "applications-development",
    "⚙️ Sistema": "applications-system",
    "🔧 Utilidades y Accesorios": "applications-utilities",
    "🔌 Red / Conectividad": "network-workgroup",
    "🌍 Internet y Navegación": "applications-internet",
    "🎨 Gráficos y Diseño": "applications-graphics",
    "🎬 Multimedia / Audio y Video": "applications-multimedia",
    "📁 Oficina y Documentos": "applications-office",
}

def parse_desktop_file(filepath):
    """Parsea un archivo .desktop y extrae información básica."""
    entry = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            in_section = False
            for line in f:
                line = line.strip()
                if line == '[Desktop Entry]':
                    in_section = True
                    continue
                elif line.startswith('[') and line.endswith(']'):
                    in_section = False
                    continue
                if in_section and '=' in line:
                    key, val = line.split('=', 1)
                    entry[key.strip()] = val.strip()
    except Exception:
        pass
    return entry

def clean_exec(exec_line):
    """Limpia los argumentos de archivos del comando Exec (%u, %U, %f, etc.)."""
    cleaned = exec_line
    for placeholder in ['%u', '%U', '%f', '%F', '%i', '%c', '%k']:
        cleaned = cleaned.replace(placeholder, '')
    return cleaned.strip()

def get_applications():
    """Escanea los directorios de aplicaciones y las agrupa por categoría."""
    paths = [
        '/usr/share/applications/*.desktop',
        os.path.expanduser('~/.local/share/applications/*.desktop')
    ]
    
    desktop_files = []
    for path in paths:
        desktop_files.extend(glob.glob(path))
        
    apps_by_category = {}
    # Inicializar categorías
    for cat_name in CATEGORIES_MAPPING.values():
        apps_by_category[cat_name] = []
    
    apps_by_category["🔧 Utilidades y Accesorios"] = []
    
    for filepath in desktop_files:
        entry = parse_desktop_file(filepath)
        if not entry or entry.get('NoDisplay') == 'true' or entry.get('Type') != 'Application':
            continue
            
        name = entry.get('Name')
        exec_cmd = entry.get('Exec')
        if not name or not exec_cmd:
            continue
            
        icon = entry.get('Icon', 'application-x-executable')
        categories_str = entry.get('Categories', '')
        terminal = entry.get('Terminal', 'false').lower() == 'true'
        comment = entry.get('Comment', '')
        
        app_data = {
            'name': name,
            'exec': clean_exec(exec_cmd),
            'icon': icon,
            'terminal': terminal,
            'comment': comment
        }
        
        # Clasificar la aplicación
        assigned = False
        categories_list = [c.strip() for c in categories_str.replace(';', ' ').split() if c.strip()]
        
        # 1. Buscar coincidencias por prefijo o coincidencia exacta con CATEGORIES_MAPPING
        for cat_code in CATEGORIES_MAPPING.keys():
            for app_cat in categories_list:
                if app_cat == cat_code or app_cat.startswith(cat_code + '-'):
                    apps_by_category[CATEGORIES_MAPPING[cat_code]].append(app_data)
                    assigned = True
                    break
            if assigned:
                break
                
        # 2. Si no se asignó, poner en "Otros"
        if not assigned:
            apps_by_category["🔧 Utilidades y Accesorios"].append(app_data)
            
    # Filtrar categorías vacías y eliminar duplicados dentro de cada categoría
    final_grouped = {}
    for cat, apps in apps_by_category.items():
        if apps:
            # Eliminar duplicados por nombre
            seen = set()
            unique_apps = []
            for app in apps:
                if app['name'] not in seen:
                    seen.add(app['name'])
                    unique_apps.append(app)
            final_grouped[cat] = sorted(unique_apps, key=lambda x: x['name'].lower())
            
    return final_grouped

def run_rofi(options, prompt, theme_path):
    """Ejecuta Rofi en modo dmenu con una lista de opciones con formato (nombre\0icon\x1ficon_name)."""
    rofi_cmd = [
        'rofi', '-dmenu',
        '-p', prompt,
        '-theme', theme_path,
        '-i'  # Búsqueda insensible a mayúsculas
    ]
    
    # Formatear las opciones con iconos si los tienen
    input_data = []
    for opt in options:
        display = opt['display']
        icon = opt.get('icon')
        if icon:
            input_data.append(f"{display}\0icon\x1f{icon}")
        else:
            input_data.append(display)
            
    proc = subprocess.Popen(rofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = proc.communicate('\n'.join(input_data))
    
    if proc.returncode == 0:
        return stdout.strip()
    return None

def launch_app(app):
    """Ejecuta la aplicación en segundo plano."""
    cmd = app['exec']
    if app['terminal']:
        # Abrir en Kitty
        subprocess.Popen(['kitty', '-e', 'sh', '-c', cmd])
    else:
        # Abrir directamente en segundo plano con nohup
        # Redirigir stdout/stderr para evitar bloquear el script
        subprocess.Popen(f"nohup {cmd} >/dev/null 2>&1 &", shell=True)

def main():
    theme_path = os.path.expanduser('~/.config/rofi/launchers/style-4.rasi')
    
    # Obtener aplicaciones clasificadas
    apps_grouped = get_applications()
    
    # Loop de navegación de menús
    current_category = None
    while True:
        if current_category is None:
            # --- MENU 1: LISTA DE CATEGORÍAS Y TODAS LAS APLICACIONES ---
            categories_opts = []
            
            # 1. Agregar categorías
            for cat in sorted(apps_grouped.keys()):
                icon = CATEGORY_ICONS.get(cat, 'folder')
                categories_opts.append({
                    'display': cat,
                    'icon': icon,
                    'is_category': True,
                    'cat_name': cat
                })
                
            # 2. Agregar todas las aplicaciones ordenadas por nombre
            all_apps = []
            seen_apps = set()
            for cat, apps in apps_grouped.items():
                for app in apps:
                    if app['name'] not in seen_apps:
                        seen_apps.add(app['name'])
                        all_apps.append(app)
            
            all_apps_sorted = sorted(all_apps, key=lambda x: x['name'].lower())
            
            for app in all_apps_sorted:
                display_name = app['name']
                if app['comment']:
                    display_name = f"{app['name']} — {app['comment']}"
                categories_opts.append({
                    'display': display_name,
                    'icon': app['icon'],
                    'is_category': False,
                    'app_data': app
                })
                
            selection = run_rofi(categories_opts, "Buscar o elegir Categoría", theme_path)
            if not selection:
                break # Cancelado por el usuario (ESC)
                
            selected_opt = next((o for o in categories_opts if o['display'] == selection), None)
            if selected_opt:
                if selected_opt['is_category']:
                    current_category = selected_opt['cat_name']
                else:
                    launch_app(selected_opt['app_data'])
                    break
            else:
                # Búsqueda global de fallback si el usuario escribe algo personalizado y presiona Enter
                matches = []
                for cat, apps in apps_grouped.items():
                    for app in apps:
                        if (selection.lower() in app['name'].lower()) or (selection.lower() in app['exec'].lower()):
                            matches.append(app)
                
                if len(matches) == 1:
                    launch_app(matches[0])
                    break
                elif len(matches) > 1:
                    # Mostrar las coincidencias encontradas
                    match_opts = []
                    for app in matches:
                        display_name = app['name']
                        if app['comment']:
                            display_name = f"{app['name']} — {app['comment']}"
                        match_opts.append({
                            'display': display_name,
                            'icon': app['icon'],
                            'app_data': app,
                            'is_back': False
                        })
                    sub_selection = run_rofi(match_opts, f"Resultados para '{selection}'", theme_path)
                    if sub_selection:
                        selected_opt = next((o for o in match_opts if o['display'] == sub_selection), None)
                        if selected_opt:
                            launch_app(selected_opt['app_data'])
                    break
                else:
                    # Si no hay coincidencias, no hacer nada y seguir en el menú principal
                    pass
        else:
            # --- MENU 2: APLICACIONES EN LA CATEGORÍA SELECCIONADA ---
            app_opts = [{
                'display': ".. (Volver a Categorías)",
                'icon': "go-previous",
                'is_back': True
            }]
            
            for app in apps_grouped[current_category]:
                # Nombre de la aplicación con comentario/subtítulo si existe
                display_name = app['name']
                if app['comment']:
                    display_name = f"{app['name']} — {app['comment']}"
                app_opts.append({
                    'display': display_name,
                    'icon': app['icon'],
                    'app_data': app,
                    'is_back': False
                })
                
            selection = run_rofi(app_opts, current_category, theme_path)
            if not selection:
                break # Cancelado por el usuario (ESC)
                
            # Buscar la opción seleccionada
            selected_opt = None
            for opt in app_opts:
                if opt['display'] == selection:
                    selected_opt = opt
                    break
                    
            if selected_opt:
                if selected_opt.get('is_back'):
                    current_category = None # Regresar al menú de categorías
                else:
                    # Lanzar la aplicación
                    launch_app(selected_opt['app_data'])
                    break

if __name__ == '__main__':
    main()
