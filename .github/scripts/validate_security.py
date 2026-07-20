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
        """Carga y procesa resultados de gitleaks"""
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
                    secret_finding = {
                        "rule": finding.get("rule", "Unknown"),
                        "file": finding.get("file", "Unknown"),
                        "line": finding.get("line", 0),
                        "secret": finding.get("secret", "")[:20] + "..." if finding.get("secret") else "",
                        "severity": "high"  # Todos los secretos son de alta severidad
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
    
    # Imprimir resumen
    print("\n" + "="*60)
    print("RESULTADO DE VALIDACIÓN DE SEGURIDAD - COLOMBIA")
    print("="*60)
    
    summary = result["summary"]
    print(f"\n📊 Resumen:")
    print(f"  Secretos detectados: {summary['total_secrets']}")
    print(f"  Vulnerabilidades totales: {summary['total_vulnerabilities']}")
    print(f"  • Críticas: {summary['critical_vulnerabilities']}")
    print(f"  • Altas: {summary['high_vulnerabilities']}")
    print(f"  • Medias: {summary['medium_vulnerabilities']}")
    print(f"  • Bajas: {summary['low_vulnerabilities']}")
    
    print(f"\n🏛️  Cumplimiento Ley 1581:")
    compliance = result["compliance"]["ley_1581"]
    print(f"  Fuga de datos detectada: {'SÍ' if compliance['data_leakage_detected'] else 'NO'}")
    print(f"  Notificación requerida: {'SÍ' if compliance['requires_notification'] else 'NO'}")
    
    if compliance["recommendations"]:
        print(f"\n  Recomendaciones:")
        for rec in compliance["recommendations"]:
            print(f"  • {rec}")
    
    print(f"\n🔒 Estado de validación: {result['status'].upper()}")
    
    if result["status"] == "failed":
        print("\n❌ MERGE BLOQUEADO - Se detectaron vulnerabilidades críticas/altas o secretos expuestos")
        sys.exit(1)
    elif result["status"] == "requires_approbation":
        print("\n⚠️  APROBACIÓN REQUERIDA - Se detectaron vulnerabilidades medias/bajas")
        sys.exit(0)
    else:
        print("\n✅ VALIDACIÓN EXITOSA - No se detectaron problemas de seguridad críticos")
        sys.exit(0)


if __name__ == "__main__":
    main()