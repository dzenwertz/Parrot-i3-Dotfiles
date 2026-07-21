#!/bin/bash
# Script inteligente para cerrar aplicaciones Electron/AppImage limpiamente.
# Mata la ventana i3 enfocada y luego limpia todos los procesos hijos huérfanos.

# Obtener la ventana enfocada y su PID
FOCUSED_PID=$(xdotool getactivewindow getwindowpid 2>/dev/null)
FOCUSED_CLASS=$(xdotool getactivewindow getwindowclassname 2>/dev/null)

# Cerrar la ventana vía i3
i3-msg kill

# Esperar un momento para que i3 procese el cierre
sleep 0.3

# Si era una app Electron o AppImage, matar el árbol completo de procesos
if [ -n "$FOCUSED_PID" ]; then
    case "$FOCUSED_CLASS" in
        antigravity|Antigravity|"Antigravity IDE"|antigravity-ide|PacketTracer|"Cisco Packet Tracer")
            # Matar todo el árbol de procesos del padre
            pkill -TERM -P "$FOCUSED_PID" 2>/dev/null
            kill -TERM "$FOCUSED_PID" 2>/dev/null
            sleep 0.5
            # Si siguen vivos, forzar la muerte
            pkill -9 -P "$FOCUSED_PID" 2>/dev/null
            kill -9 "$FOCUSED_PID" 2>/dev/null
            ;;
        *)
            # Para apps normales, solo confiar en i3 kill
            ;;
    esac
fi
