#!/usr/bin/env python3
"""
Script de validación de seguridad para GitHub Actions - Colombia

Analiza resultados de gitleaks y semgrep para determinar si un merge
puede proceder basado en la severidad de las vulnerabilidades detectadas.

Cumplimiento Ley 1581: Detecta fugas de datos personales y proporciona
reportes comprensibles para stakeholders no técnicos.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class SecurityValidator:
    def __init__(self):
        self.secret_findings = []
        self.vulnerability_findings = []
        self.validation_result = {
            "status": "passed",
            "secret_findings": [],
            "vulnerability_findings": [],
            "summary": {
                "total_secrets": 0,
                "total_vulnerabilities": 0,
                "critical_vulnerabilities": 0,
                "high_vulnerabilities": 0,
                "medium_vulnerabilities": 0,
                "low_vulnerabilities": 0
            },
            "compliance": {
                "ley_1581": {
                    "data_leakage_detected": False,
                    "requires_notification": False,
                    "recommendations": []
                }
            }
        }
    
    def load_gitleaks_results(self, filepath: Path) -> bool:
        """Carga y procesa resultados de gitleaks con información detallada"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and 'findings' in data:
                findings = data['findings']
            elif isinstance(data, list):
                findings = data
            else:
                findings = []
            
            for finding in findings:
                if isinstance(finding, dict):
                    # Extraer información completa del hallazgo
                    secret_finding = {
                        "rule": finding.get("rule", "Unknown"),
                        "description": finding.get("description", ""),
                        "file": finding.get("file", "Unknown"),
                        "line": finding.get("line", 0),
                        "secret": finding.get("secret", "")[:20] + "..." if finding.get("secret") else "",
                        "secret_full": finding.get("secret", ""),
                        "commit": finding.get("commit", ""),
                        "author": finding.get("author", ""),
                        "email": finding.get("email", ""),
                        "date": finding.get("date", ""),
                        "entropy": finding.get("entropy", 0.0),
                        "severity": "high",  # Todos los secretos son de alta severidad
                        "tags": finding.get("tags", []),
                        "fingerprint": finding.get("fingerprint", "")
                    }
                    self.secret_findings.append(secret_finding)
            
            self.validation_result["summary"]["total_secrets"] = len(self.secret_findings)
            
            # Análisis de cumplimiento Ley 1581
            if self.secret_findings:
                self.validation_result["compliance"]["ley_1581"]["data_leakage_detected"] = True
                self.validation_result["compliance"]["ley_1581"]["requires_notification"] = True
                self.validation_result["compliance"]["ley_1581"]["recommendations"].append(
                    "Se detectaron fugas de datos personales. Notificar al área legal según Ley 1581."
                )
            
            # Análisis adicional por tipo de secreto
            aws_keys = [s for s in self.secret_findings if "aws" in s["rule"].lower()]
            api_keys = [s for s in self.secret_findings if "api" in s["rule"].lower()]
            
            if aws_keys:
                self.validation_result["compliance"]["ley_1581"]["recommendations"].append(
                    f"Se detectaron {len(aws_keys)} claves AWS expuestas. Alto riesgo financiero."
                )
            
            if api_keys:
                self.validation_result["compliance"]["ley_1581"]["recommendations"].append(
                    f"Se detectaron {len(api_keys)} API keys expuestas. Riesgo de acceso no autorizado."
                )
            
            return True
        except Exception as e:
            print(f"Error cargando resultados de gitleaks: {e}")
            return False
    
    def load_semgrep_results(self, filepath: Path) -> bool:
        """Carga y procesa resultados de semgrep (formato SARIF)"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Procesar formato SARIF
            if 'runs' in data:
                for run in data['runs']:
                    if 'results' in run:
                        for result in run['results']:
                            vulnerability = self._parse_sarif_result(result, run)
                            if vulnerability:
                                self.vulnerability_findings.append(vulnerability)
            
            # Actualizar resumen
            for v in self.vulnerability_findings:
                severity = v.get("severity", "medium").lower()
                if severity == "critical":
                    self.validation_result["summary"]["critical_vulnerabilities"] += 1
                elif severity == "high":
                    self.validation_result["summary"]["high_vulnerabilities"] += 1
                elif severity == "medium":
                    self.validation_result["summary"]["medium_vulnerabilities"] += 1
                elif severity == "low":
                    self.validation_result["summary"]["low_vulnerabilities"] += 1
            
            self.validation_result["summary"]["total_vulnerabilities"] = len(self.vulnerability_findings)
            
            return True
        except Exception as e:
            print(f"Error cargando resultados de semgrep: {e}")
            return False
    
    def _parse_sarif_result(self, result: Dict, run: Dict) -> Optional[Dict]:
        """Parsea un resultado individual de SARIF"""
        try:
            # Extraer información de ubicación
            location = result.get('locations', [{}])[0]
            physical_location = location.get('physicalLocation', {})
            artifact_location = physical_location.get('artifactLocation', {})
            region = physical_location.get('region', {})
            
            # Extraer regla y severidad
            rule_id = result.get('ruleId', 'Unknown')
            rule_index = result.get('ruleIndex', 0)
            
            # Buscar información de la regla
            rule_info = {}
            if 'tool' in run and 'driver' in run['tool']:
                rules = run['tool']['driver'].get('rules', [])
                if rule_index < len(rules):
                    rule_info = rules[rule_index]
            
            # Determinar severidad
            severity = "medium"
            if 'properties' in result:
                props = result['properties']
                if 'security-severity' in props:
                    sec_sev = float(props['security-severity'])
                    if sec_sev >= 9.0:
                        severity = "critical"
                    elif sec_sev >= 7.0:
                        severity = "high"
                    elif sec_sev >= 4.0:
                        severity = "medium"
                    else:
                        severity = "low"
                elif 'issue_severity' in props:
                    severity = props['issue_severity'].lower()
            
            return {
                "rule": rule_id,
                "description": rule_info.get('shortDescription', {}).get('text', ''),
                "file": artifact_location.get('uri', 'Unknown'),
                "line": region.get('startLine', 0),
                "severity": severity,
                "message": result.get('message', {}).get('text', '')
            }
        except Exception as e:
            print(f"Error parseando resultado SARIF: {e}")
            return None
    
    def determine_validation_status(self) -> str:
        """Determina el estado de validación basado en los hallazgos"""
        
        # Bloquear si hay secretos detectados
        if self.secret_findings:
            return "failed"
        
        # Bloquear si hay vulnerabilidades críticas o altas
        critical_high_count = (
            self.validation_result["summary"]["critical_vulnerabilities"] +
            self.validation_result["summary"]["high_vulnerabilities"]
        )
        
        if critical_high_count > 0:
            return "failed"
        
        # Requerir aprobación si hay vulnerabilidades medias o bajas
        medium_low_count = (
            self.validation_result["summary"]["medium_vulnerabilities"] +
            self.validation_result["summary"]["low_vulnerabilities"]
        )
        
        if medium_low_count > 0:
            return "requires_approval"
        
        # Pasar si no hay hallazgos
        return "passed"
    
    def generate_result(self) -> Dict:
        """Genera el resultado final de validación"""
        self.validation_result["status"] = self.determine_validation_status()
        self.validation_result["secret_findings"] = self.secret_findings
        self.validation_result["vulnerability_findings"] = self.vulnerability_findings
        
        # Agregar recomendaciones basadas en el contexto colombiano
        if self.validation_result["status"] == "failed":
            self.validation_result["compliance"]["ley_1581"]["recommendations"].append(
                "Revisión legal requerida antes de proceder con cambios que afecten datos personales."
            )
        
        return self.validation_result


def main():
    parser = argparse.ArgumentParser(
        description="Validador de seguridad para GitHub Actions - Colombia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --secrets gitleaks-report.json --sast semgrep-results.sarif
  
Este script ayuda al cumplimiento de la Ley 1581 de Protección de Datos
proporcionando análisis de fugas de datos y reportes comprensibles.
        """
    )
    
    parser.add_argument(
        "--secrets",
        required=True,
        help="Ruta al archivo JSON de resultados de gitleaks"
    )
    
    parser.add_argument(
        "--sast",
        required=True,
        help="Ruta al archivo SARIF de resultados de semgrep"
    )
    
    parser.add_argument(
        "--output",
        default="validation-result.json",
        help="Ruta de salida para el resultado de validación (default: validation-result.json)"
    )
    
    args = parser.parse_args()
    
    validator = SecurityValidator()
    
    # Cargar resultados
    secrets_path = Path(args.secrets)
    sast_path = Path(args.sast)
    
    if not secrets_path.exists():
        print(f"Advertencia: Archivo de secretos no encontrado: {secrets_path}")
    else:
        validator.load_gitleaks_results(secrets_path)
    
    if not sast_path.exists():
        print(f"Advertencia: Archivo SAST no encontrado: {sast_path}")
    else:
        validator.load_semgrep_results(sast_path)
    
    # Generar resultado
    result = validator.generate_result()
    
    # Guardar resultado
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # Imprimir presentación gráfica de hallazgos
    print("\n" + "="*80)
    print("🔒 RESULTADO DE ANÁLISIS DE SEGURIDAD - COLOMBIA")
    print("="*80)
    
    # Banner de estado con emojis
    status_icons = {
        "passed": "✅",
        "failed": "❌", 
        "requires_approval": "⚠️"
    }
    
    status_icon = status_icons.get(result["status"], "❓")
    print(f"\n{status_icon} ESTADO FINAL: {result['status'].upper()}")
    print("-" * 40)
    
    summary = result["summary"]
    
    # 📊 SECCIÓN 1: RESUMEN VISUAL CON EMOJIS
    print(f"\n📊 RESUMEN DE HALLazGOS")
    print("═" * 40)
    
    # Mostrar secreto como tarjetas visuales
    if summary['total_secrets'] > 0:
        print(f"\n🔴 SECRETOS EXPUESTOS: {summary['total_secrets']}")
        print("▔" * 30)
        
        # Mostrar cada secreto de manera gráfica
        for i, secret in enumerate(result["secret_findings"], 1):
            print(f"\n┌─ SECRETO #{i}")
            print(f"│  📄 ARCHIVO: {secret['file']}")
            print(f"│  📍 LÍNEA: {secret['line']}")
            print(f"│  🔖 REGLA: {secret['rule']}")
            print(f"│  ⚠️  SEVERIDAD: ALTA")
            print(f"└─ 🚨 ACCIÓN REQUERIDA: ELIMINAR INMEDIATAMENTE")
    
    # Mostrar vulnerabilidades por severidad
    if summary['total_vulnerabilities'] > 0:
        print(f"\n🟡 VULNERABILIDADES DETECTADAS: {summary['total_vulnerabilities']}")
        print("▔" * 40)
        
        # Barras visuales para cada nivel de severidad
        def print_severity_bar(count, label, emoji, color_code="🟢"):
            if count > 0:
                bar = "█" * min(count, 10) + f" ({count})"
                print(f"{emoji} {label}: {bar}")
        
        print_severity_bar(summary['critical_vulnerabilities'], "CRÍTICAS", "🔴")
        print_severity_bar(summary['high_vulnerabilities'], "ALTAS", "🟠") 
        print_severity_bar(summary['medium_vulnerabilities'], "MEDIAS", "🟡")
        print_severity_bar(summary['low_vulnerabilities'], "BAJAS", "🟢")
        
        # Mostrar vulnerabilidades críticas/altas específicas
        critical_high_vulns = [v for v in result["vulnerability_findings"] 
                              if v.get("severity") in ["critical", "high"]]
        
        if critical_high_vulns:
            print(f"\n🔴 VULNERABILIDADES CRÍTICAS/ALTAS:")
            for i, vuln in enumerate(critical_high_vulns[:3], 1):  # Mostrar máximo 3
                print(f"\n  {i}. 📄 {vuln['file']}:{vuln['line']}")
                print(f"     📝 {vuln['description'][:60]}...")
                print(f"     ⚠️  {vuln['severity'].upper()}")
    
    # 📋 SECCIÓN 2: CUMPLIMIENTO NORMATIVO
    print(f"\n🏛️  CUMPLIMIENTO NORMATIVO - LEY 1581")
    print("═" * 40)
    
    compliance = result["compliance"]["ley_1581"]
    
    if compliance["data_leakage_detected"]:
        print(f"\n🔴 FUGAS DE DATOS DETECTADAS: SÍ")
        print("   └─ 🚨 NOTIFICACIÓN LEGAL REQUERIDA")
        print("   └─ ⏰ PLAZO: 72 horas hábiles según SIC")
    else:
        print(f"\n🟢 FUGAS DE DATOS DETECTADAS: NO")
        print("   └─ ✅ Cumple con principios de seguridad Ley 1581")
    
    if compliance["requires_notification"]:
        print(f"\n📧 NOTIFICACIÓN REQUERIDA: SÍ")
        print("   └─ 📋 Titulares de datos afectados")
        print("   └─ 🏛️  Superintendencia de Industria y Comercio (SIC)")
    
    # 💡 SECCIÓN 3: RECOMENDACIONES VISUALES
    if compliance["recommendations"] or summary['total_secrets'] > 0 or summary['critical_vulnerabilities'] > 0:
        print(f"\n💡 RECOMENDACIONES DE ACCIÓN")
        print("═" * 40)
        
        if summary['total_secrets'] > 0:
            print(f"\n🔴 PRIORIDAD ALTA:")
            print("   1. 🔑 Implementar sistema de gestión de secretos (Vault, Secrets Manager)")
            print("   2. 🗑️  Eliminar credenciales del código fuente")
            print("   3. 📋 Revisar historial de commits para otras exposiciones")
        
        if summary['critical_vulnerabilities'] > 0:
            print(f"\n🟠 PRIORIDAD MEDIA:")
            print("   1. 🔧 Corregir vulnerabilidades críticas en 7 días hábiles")
            print("   2. 👥 Asignar equipo dedicado de seguridad")
            print("   3. 📊 Actualizar matriz de riesgos")
        
        if compliance["data_leakage_detected"]:
            print(f"\n🏛️  ACCIONES LEGALES:")
            print("   1. 📞 Contactar área legal inmediatamente")
            print("   2. 📄 Documentar incidente según protocolo interno")
            print("   3. 🕒 Cumplir plazos de notificación Ley 1581")
    
    # 🎯 SECCIÓN 4: DECISIÓN FINAL CON ÉNFASIS VISUAL
    print(f"\n" + "="*80)
    
    if result["status"] == "failed":
        print(f"\n{'❌' * 10} DECISIÓN FINAL {'❌' * 10}")
        print(f"\n🚫 MERGE BLOQUEADO AUTOMÁTICAMENTE")
        print(f"\n📋 RAZONES:")
        
        if summary['total_secrets'] > 0:
            print(f"   • 🔴 {summary['total_secrets']} secretos expuestos detectados")
        
        critical_high_count = summary['critical_vulnerabilities'] + summary['high_vulnerabilities']
        if critical_high_count > 0:
            print(f"   • 🟠 {critical_high_count} vulnerabilidades críticas/altas")
        
        print(f"\n📞 CONTACTOS URGENTES:")
        print(f"   • 👨‍💼 Responsable de seguridad: seguridad@empresa.co")
        print(f"   • ⚖️  Área legal: legal@empresa.co")
        
        sys.exit(1)
        
    elif result["status"] == "requires_approval":
        print(f"\n{'⚠️ ' * 10} DECISIÓN FINAL {' ⚠️' * 10}")
        print(f"\n⏳ APROBACIÓN MANUAL REQUERIDA")
        print(f"\n📋 DETALLES:")
        print(f"   • 🟡 {summary['medium_vulnerabilities']} vulnerabilidades medias")
        print(f"   • 🟢 {summary['low_vulnerabilities']} vulnerabilidades bajas")
        print(f"\n✅ ACCIONES PERMITIDAS:")
        print(f"   • 📝 Revisión técnica por equipo de seguridad")
        print(f"   • ✍️  Aprobación manual por responsable")
        
        sys.exit(0)
        
    else:
        print(f"\n{'✅' * 10} DECISIÓN FINAL {'✅' * 10}")
        print(f"\n🎉 ¡ANÁLISIS EXITOSO!")
        print(f"\n📊 RESUMEN POSITIVO:")
        print(f"   • 🔒 0 secretos expuestos")
        print(f"   • 🛡️  0 vulnerabilidades críticas/altas")
        print(f"   • 📋 Cumple con Ley 1581")
        print(f"\n🚀 ACCIÓN: MERGE PERMITIDO")
        
        sys.exit(0)


if __name__ == "__main__":
    main()