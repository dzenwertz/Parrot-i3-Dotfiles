#!/usr/bin/env bash

# Directorio de wallpapers
WALLPAPER_DIR="/home/wlaz/.dotfiles/assets/wallpaper"
ROFI_THEME="/home/wlaz/.config/rofi/launchers/style-4.rasi"

# Listar wallpapers disponibles (excluyendo el symlink activo 'wallpaper.png')
wallpapers=$(find "$WALLPAPER_DIR" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.png" \) ! -name "wallpaper.png" -printf "%f\n" | sort)

if [ -z "$wallpapers" ]; then
    notify-send "Wallpaper Changer" "No se encontraron fondos en $WALLPAPER_DIR"
    exit 1
fi

# Mostrar menú en Rofi
selected=$(echo "$wallpapers" | rofi -dmenu -p "Seleccionar Fondo" -theme "$ROFI_THEME" -i)

if [ -n "$selected" ]; then
    selected_path="$WALLPAPER_DIR/$selected"
    active_path="$WALLPAPER_DIR/wallpaper.png"

    # Cambiar el enlace simbólico para que persista al reiniciar i3
    rm -f "$active_path"
    ln -sf "$selected_path" "$active_path"

    # Aplicar el fondo inmediatamente con feh
    feh --bg-fill "$active_path"

    # Enviar notificación
    notify-send "Fondo de Pantalla" "Cambiado con éxito a: $selected" -i "$selected_path"
fi
