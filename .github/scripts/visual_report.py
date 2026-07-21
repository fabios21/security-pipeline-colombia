#!/usr/bin/env python3
"""
Generador de reportes visuales para hallazgos de seguridad
Presenta los resultados de manera gráfica y fácil de entender
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import sys


class VisualSecurityReport:
    def __init__(self):
        self.secret_categories = {
            "aws": {"icon": "☁️", "color": "🟠", "name": "AWS Keys"},
            "stripe": {"icon": "💳", "color": "🟣", "name": "Stripe Keys"},
            "google": {"icon": "🔍", "color": "🔵", "name": "Google APIs"},
            "api": {"icon": "🔑", "color": "🟡", "name": "API Keys"},
            "password": {"icon": "🔒", "color": "🔴", "name": "Passwords"},
            "jwt": {"icon": "🎫", "color": "🟢", "name": "JWT Tokens"}
        }
    
    def generate_visual_summary(self, validation_file: Path) -> str:
        """Genera un resumen visual de los hallazgos"""
        try:
            with open(validation_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            output = []
            
            # 📊 ENCABEZADO VISUAL
            output.append("\n" + "╔" + "═" * 78 + "╗")
            output.append("║" + "🔒 ANÁLISIS DE SEGURIDAD - REPORTE VISUAL".center(78) + "║")
            output.append("║" + f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
            output.append("╚" + "═" * 78 + "╝")
            
            # 🎯 ESTADO GENERAL
            status = data.get("status", "unknown")
            status_icons = {"passed": "✅", "failed": "❌", "requires_approval": "⚠️"}
            
            output.append("\n" + "─" * 80)
            output.append(f"\n{status_icons.get(status, '❓')} ESTADO DE VALIDACIÓN: {status.upper()}")
            output.append("─" * 40)
            
            # 📈 SECCIÓN DE SECRETOS
            secrets = data.get("secret_findings", [])
            if secrets:
                output.append("\n" + "🔴 SECRETOS EXPUESTOS".center(80))
                output.append("▀" * 80)
                
                for i, secret in enumerate(secrets, 1):
                    output.append(f"\n┌─ {'SECRETO #' + str(i):─^76} ┐")
                    output.append(f"│  📄 ARCHIVO: {secret.get('file', 'Desconocido')}")
                    output.append(f"│  📍 LÍNEA: {secret.get('line', 0)}")
                    
                    # Determinar categoría del secreto
                    rule = secret.get("rule", "").lower()
                    category = "api"
                    for cat in self.secret_categories:
                        if cat in rule:
                            category = cat
                            break
                    
                    cat_info = self.secret_categories.get(category, {"icon": "❓", "color": "⚪", "name": "Otro"})
                    output.append(f"│  {cat_info['icon']} TIPO: {cat_info['name']}")
                    output.append(f"│  🔖 REGLA: {secret.get('rule', 'Desconocida')}")
                    
                    # Mostrar parte del secreto (censurado)
                    secret_text = secret.get("secret", "")
                    if len(secret_text) > 30:
                        secret_display = f"{secret_text[:15]}...{secret_text[-10:]}"
                    else:
                        secret_display = secret_text
                    
                    output.append(f"│  🕵️  SECRETO: {secret_display}")
                    output.append(f"│  ⚠️  SEVERIDAD: ALTA")
                    output.append(f"│  🚨 ACCIÓN: ELIMINAR INMEDIATAMENTE")
                    output.append(f"└" + "─" * 78 + "┘")
            
            # 📊 RESUMEN ESTADÍSTICO
            summary = data.get("summary", {})
            output.append("\n" + "📊 RESUMEN ESTADÍSTICO".center(80))
            output.append("▄" * 80)
            
            # Gráfico de barras para secretos
            secret_count = summary.get("total_secrets", 0)
            if secret_count > 0:
                bar_length = min(secret_count * 3, 40)
                bar = "█" * bar_length
                output.append(f"\n🔴 SECRETOS: {bar} ({secret_count})")
            
            # Gráfico de vulnerabilidades
            vuln_counts = [
                ("CRÍTICAS", summary.get("critical_vulnerabilities", 0), "🔴"),
                ("ALTAS", summary.get("high_vulnerabilities", 0), "🟠"),
                ("MEDIAS", summary.get("medium_vulnerabilities", 0), "🟡"),
                ("BAJAS", summary.get("low_vulnerabilities", 0), "🟢")
            ]
            
            for name, count, icon in vuln_counts:
                if count > 0:
                    bar_length = min(count * 2, 30)
                    bar = "█" * bar_length
                    output.append(f"{icon} {name}: {bar} ({count})")
            
            # ⚠️ ALERTA DE SEGURIDAD
            compliance = data.get("compliance", {}).get("ley_1581", {})
            if compliance.get("data_leakage_detected", False):
                output.append("\n" + "🚨 ALERTA DE SEGURIDAD - RIESGO CRÍTICO".center(80))
                output.append("⚠️" * 40)
                output.append("\n🔴 CREDENCIALES SENSIBLES EXPUESTAS")
                output.append("   ├─ 📞 Contactar equipo de seguridad inmediatamente")
                output.append("   ├─ 📄 Documentar incidente según protocolo de seguridad")
                output.append("   └─ ⏰ Revisar e implementar controles de seguridad")
            
            # 💡 RECOMENDACIONES
            if secrets or summary.get("critical_vulnerabilities", 0) > 0:
                output.append("\n" + "💡 RECOMENDACIONES PRIORITARIAS".center(80))
                output.append("★" * 40)
                
                if secret_count > 0:
                    output.append("\n🔴 PRIORIDAD ALTA (Secretos):")
                    output.append("   1. 🔑 Implementar sistema de gestión de secretos")
                    output.append("   2. 🗑️  Eliminar credenciales del código")
                    output.append("   3. 🔍 Revisar historial completo de commits")
                
                if summary.get("critical_vulnerabilities", 0) > 0:
                    output.append("\n🟠 PRIORIDAD MEDIA (Vulnerabilidades):")
                    output.append("   1. 🔧 Corregir en 7 días hábiles")
                    output.append("   2. 👥 Asignar equipo de seguridad")
                    output.append("   3. 📊 Actualizar matriz de riesgos")
            
            # 🎯 DECISIÓN FINAL
            output.append("\n" + "═" * 80)
            
            if status == "failed":
                output.append("\n" + "❌" * 20 + " BLOQUEADO " + "❌" * 20)
                output.append("\n🚫 MERGE NO PERMITIDO - RIESGOS CRÍTICOS DETECTADOS")
                
                if secret_count > 0:
                    output.append(f"\n📋 Motivo: {secret_count} secretos expuestos")
                
                critical_high = summary.get("critical_vulnerabilities", 0) + summary.get("high_vulnerabilities", 0)
                if critical_high > 0:
                    output.append(f"📋 Motivo: {critical_high} vulnerabilidades críticas/altas")
                
            elif status == "requires_approval":
                output.append("\n" + "⚠️ " * 15 + " REVISIÓN " + " ⚠️" * 15)
                output.append("\n⏳ APROBACIÓN MANUAL REQUERIDA")
                output.append("\n📋 Motivo: Vulnerabilidades de riesgo medio/bajo")
                
            else:
                output.append("\n" + "✅" * 20 + " APROBADO " + "✅" * 20)
                output.append("\n🎉 ¡ANÁLISIS EXITOSO!")
                output.append("\n🚀 ACCIÓN: MERGE PERMITIDO")
            
            output.append("\n" + "═" * 80)
            
            return "\n".join(output)
            
        except Exception as e:
            return f"\n❌ Error generando reporte visual: {e}\n"


def main():
    """Función principal para generar reporte visual"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generador de reportes visuales de seguridad")
    parser.add_argument("--validation", required=True, help="Archivo JSON de validación")
    parser.add_argument("--output", default="visual-report.txt", help="Archivo de salida")
    
    args = parser.parse_args()
    
    generator = VisualSecurityReport()
    report = generator.generate_visual_summary(Path(args.validation))
    
    # Guardar reporte
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Imprimir en consola
    print(report)
    
    print(f"\n📄 Reporte visual guardado en: {args.output}")


if __name__ == "__main__":
    main()