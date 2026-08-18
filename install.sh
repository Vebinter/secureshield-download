#!/bin/bash
# SecureShield v1.0 — Автоматическая установка
# Двойной клик по этому файлу = установка

echo "🛡️ SecureShield v1.0 — Установка..."
DIR="$(cd "$(dirname "$0")" && pwd)"
pkexec dpkg -i "$DIR/secureshield_1.0_amd64.deb"
pkexec chmod 777 /etc/secureshield 2>/dev/null
pkexec touch /etc/secureshield/license.json 2>/dev/null
pkexec chmod 666 /etc/secureshield/license.json 2>/dev/null
echo "✅ SecureShield установлен! Найди в меню приложений."
read -p "Нажми Enter для выхода..."
