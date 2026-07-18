#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import i3ipc
import time
import socket
import sys

def on_window_focus(i3, e):
    try:
        focused = i3.get_tree().find_focused()
        if focused and focused.type == 'con':
            # Ignorar si es una ventana flotante
            if focused.floating and focused.floating != 'auto_off':
                return
            rect = focused.rect
            # Si el ancho es mayor que el alto, dividir horizontalmente; si no, verticalmente
            if rect.width > rect.height:
                i3.command('split h')
            else:
                i3.command('split v')
    except Exception:
        pass

def main():
    # Asegurar instancia única usando un socket abstracto
    try:
        # En Python, el prefijo \0 crea un socket en el espacio de nombres abstracto
        lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        lock_socket.bind('\0alternating_layouts_i3_lock')
    except socket.error:
        # Ya hay otra instancia corriendo, salir silenciosamente
        sys.exit(0)

    # Esperar un momento a que i3 termine de inicializarse
    time.sleep(1)

    i3 = None
    # Intentar conectar con reintentos
    for _ in range(15):
        try:
            i3 = i3ipc.Connection()
            break
        except Exception:
            time.sleep(0.5)
            
    if i3 is None:
        return
        
    try:
        # Configurar el split inicial
        on_window_focus(i3, None)
        # Escuchar eventos de enfoque
        i3.on("window::focus", on_window_focus)
        i3.main()
    except Exception:
        pass

if __name__ == "__main__":
    main()
