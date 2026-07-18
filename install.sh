#!/usr/bin/env bash
# ==============================================================================
# Script de Instalación de Dotfiles - Perú Cyber Security Theme
# Desarrollado por Joseph_ICV & Antigravity AI
# Soporta: Debian, Ubuntu, Parrot OS y distribuciones basadas en APT.
# ==============================================================================

set -e

# Colores para salida en terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}   Instalador de Dotfiles - Perú Cyber Security Theme ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Verificar si el sistema usa APT
if ! command -v apt-get &> /dev/null; then
    echo -e "${RED}[Error] Este instalador está diseñado para distribuciones basadas en Debian/APT (Parrot OS, Ubuntu, etc.)${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/4] Instalando dependencias del sistema...${NC}"
sudo apt-get update
sudo apt-get install -y \
    i3-wm \
    polybar \
    rofi \
    picom \
    maim \
    slop \
    brightnessctl \
    xcape \
    zsh \
    kitty \
    feh \
    python3 \
    python3-i3ipc \
    fastfetch \
    waybar

echo -e "${GREEN}[✔] Dependencias instaladas con éxito.${NC}"

# 2. Configurar directorios
echo -e "${YELLOW}[2/4] Creando estructura de directorios...${NC}"
mkdir -p "$HOME/.config"
mkdir -p "$HOME/.local/share/applications"

# Directorio base de dotfiles
DOTFILES_DIR="$HOME/.dotfiles"

# 3. Enlazar archivos de configuración
echo -e "${YELLOW}[3/4] Creando enlaces simbólicos de configuración...${NC}"

# Enlazar carpetas de configuración (.config)
configs=(i3 polybar rofi kitty picom fastfetch waybar)
for cfg in "${configs[@]}"; do
    src="$DOTFILES_DIR/config/.config/$cfg"
    dest="$HOME/.config/$cfg"
    
    if [ -d "$src" ] || [ -f "$src" ]; then
        echo -e "Enlazando: $dest -> $src"
        rm -rf "$dest"
        ln -sf "$src" "$dest"
    fi
done

# Enlazar Zsh config
if [ -f "$DOTFILES_DIR/config/.zshrc" ]; then
    echo -e "Enlazando: $HOME/.zshrc -> $DOTFILES_DIR/config/.zshrc"
    rm -f "$HOME/.zshrc"
    ln -sf "$DOTFILES_DIR/config/.zshrc" "$HOME/.zshrc"
else
    # Si .zshrc está en la raíz del repo (como en Oh My Zsh normal)
    if [ -f "$DOTFILES_DIR/.zshrc" ]; then
        echo -e "Enlazando: $HOME/.zshrc -> $DOTFILES_DIR/.zshrc"
        rm -f "$HOME/.zshrc"
        ln -sf "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
    fi
fi

# Hacer scripts ejecutables
echo -e "${YELLOW}[4/4] Dando permisos de ejecución a los scripts...${NC}"
chmod +x "$DOTFILES_DIR/config/.config/polybar/launch.sh"
chmod +x "$DOTFILES_DIR/config/.config/rofi/launchers/launcher.sh"
chmod +x "$DOTFILES_DIR/config/.config/rofi/scripts/rofi-category-launcher.py"
chmod +x "$DOTFILES_DIR/config/.config/rofi/scripts/rofi-wallpaper-changer.sh"
chmod +x "$DOTFILES_DIR/config/.config/i3/scripts/alternating_layouts.py"

# Configurar el fondo de pantalla activo inicial
active_wallpaper="$DOTFILES_DIR/assets/wallpaper/wallpaper.png"
if [ -f "$DOTFILES_DIR/assets/wallpaper/peru_cyber_dark_upscayl_2x_digital-art-4x.png" ]; then
    rm -f "$active_wallpaper"
    ln -sf "$DOTFILES_DIR/assets/wallpaper/peru_cyber_dark_upscayl_2x_digital-art-4x.png" "$active_wallpaper"
fi

# Integrar el lanzador de Upscayl si el AppImage existe en descargas
upscayl_path="$HOME/Downloads/upscayl-2.15.0-linux.AppImage"
if [ -f "$upscayl_path" ]; then
    chmod +x "$upscayl_path"
    
    # Crear archivo desktop para Upscayl
    cat <<EOF > "$HOME/.local/share/applications/upscayl.desktop"
[Desktop Entry]
Name=Upscayl
Comment=Free and Open Source AI Image Upscaler
Exec=$upscayl_path
Icon=image-viewer
Terminal=false
Type=Application
Categories=Graphics;Utility;
EOF
fi

# Integrar Antigravity si existe en Descargas
antigravity_path="$HOME/Downloads/Antigravity-x64/antigravity"
if [ -f "$antigravity_path" ]; then
    chmod +x "$antigravity_path"
    cat <<EOF > "$HOME/.local/share/applications/antigravity.desktop"
[Desktop Entry]
Name=Antigravity
Comment=Antigravity AI Coding Assistant
Exec=$antigravity_path
Icon=brain
Terminal=false
Type=Application
Categories=Utility;14;
EOF
fi

# Integrar Antigravity IDE si existe en Descargas
antigravity_ide_path="$HOME/Downloads/Antigravity IDE/antigravity-ide"
if [ -f "$antigravity_ide_path" ]; then
    chmod +x "$antigravity_ide_path"
    cat <<EOF > "$HOME/.local/share/applications/antigravity-ide.desktop"
[Desktop Entry]
Name=Antigravity IDE
Comment=Antigravity AI Integrated Development Environment
Exec="$antigravity_ide_path"
Icon=devel
Terminal=false
Type=Application
Categories=Development;14;
EOF
fi

# Actualizar base de datos de aplicaciones
update-desktop-database "$HOME/.local/share/applications" || true

echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}   [✔] ¡Instalación Completada con Éxito!              ${NC}"
echo -e "${YELLOW}   Reinicia i3 con Super+Shift+r para aplicar los cambios.${NC}"
echo -e "${YELLOW}   Cambia fondos con Super+Shift+w o abre Caja con Super+e.${NC}"
echo -e "${GREEN}======================================================${NC}"
