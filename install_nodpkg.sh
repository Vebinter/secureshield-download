#!/bin/bash
# SecureShield v1.0 — Установка БЕЗ пакетного менеджера
# Двойной клик = установка

echo "🛡️ SecureShield v1.0 — Установка (без dpkg)..."
DIR="$(cd "$(dirname "$0")" && pwd)"

# Если есть dpkg — используем
if command -v dpkg &>/dev/null; then
    echo "📦 Найден dpkg — устанавливаем .deb"
    pkexec dpkg -i "$DIR/secureshield_1.0_amd64.deb"
else
    echo "📂 dpkg не найден — распаковываем вручную"
    pkexec mkdir -p /opt/secureshield
    pkexec mkdir -p /etc/secureshield
    # Распаковываем .deb как архив
    cd /tmp && ar x "$DIR/secureshield_1.0_amd64.deb" 2>/dev/null
    if [ -f data.tar.xz ]; then
        pkexec tar -xf data.tar.xz -C /
    elif [ -f data.tar.gz ]; then
        pkexec tar -xf data.tar.gz -C /
    fi
    cd "$DIR"
fi

# Права
pkexec chmod 777 /etc/secureshield 2>/dev/null
pkexec touch /etc/secureshield/license.json 2>/dev/null
pkexec chmod 666 /etc/secureshield/license.json 2>/dev/null

# Ярлык в меню
pkexec bash -c 'cat > /usr/share/applications/secureshield.desktop << DESK
[Desktop Entry]
Name=SecureShield
Exec=/opt/secureshield/main.py
Icon=security-high
Type=Application
Categories=Utility;
DESK'

echo "✅ SecureShield установлен!"
read -p "Нажми Enter для выхода..."
