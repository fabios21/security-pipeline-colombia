#!/usr/bin/env python3
"""
Generador de reportes de seguridad para stakeholders no técnicos

Este script procesa resultados de análisis de seguridad y genera reportes
comprensibles, incluyendo secciones específicas sobre cumplimiento
de la Ley 1581 de Protección de Datos de Colombia.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import html
import os


class SecurityReportGenerator:
    def __init__(self, language="es_CO"):
        self.language = language
        
        # Definir traducciones según idioma
        self.translations = self._get_translations(language)
        
        self.report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "timezone": "America/Bogota",
                "language": language,
                "jurisdiction": "Colombia"
            },
            "executive_summary": {},
            "detailed_findings": {},
            "compliance_analysis": {},
            "recommendations": []
        }
    
    def _get_translations(self, language):
        """Obtener traducciones según el idioma"""
        if language in ["es_CO", "es"]:
            return {
                "report_title": "Reporte de Seguridad Informática",
                "report_subtitle": "Análisis automatizado para cumplimiento normativo",
                "jurisdiction": "Colombia",
                "status_passed": "aprobado",
                "status_failed": "rechazado",
                "status_requires_approval": "requiere aprobación",
                "status_unknown": "desconocido",
                "no_critical_issues": "No se detectaron problemas de seguridad críticos en el análisis",
                "data_leakage_detected": "Se detectaron {} posibles fugas de información sensible",
                "critical_vulnerabilities_detected": "Se encontraron {} vulnerabilidades críticas que requieren atención inmediata",
                "high_vulnerabilities_detected": "Se encontraron {} vulnerabilidades de alto riesgo",
                "business_impact_high": "ALTO IMPACTO - Existen riesgos significativos que podrían afectar la continuidad del negocio y generar responsabilidades legales.",
                "business_impact_moderate": "IMPACTO MODERADO - Se requieren controles adicionales antes de proceder con los cambios propuestos.",
                "business_impact_low": "BAJO IMPACTO - El nivel de seguridad actual es apropiado para las operaciones del negocio."
            }
        else:  # English
            return {
                "report_title": "Security Report",
                "report_subtitle": "Automated analysis for regulatory compliance",
                "jurisdiction": "Colombia",
                "status_passed": "passed",
                "status_failed": "failed",
                "status_requires_approval": "requires approval",
                "status_unknown": "unknown",
                "no_critical_issues": "No critical security issues detected in the analysis",
                "data_leakage_detected": "Detected {} potential sensitive information leaks",
                "critical_vulnerabilities_detected": "Found {} critical vulnerabilities requiring immediate attention",
                "high_vulnerabilities_detected": "Found {} high-risk vulnerabilities",
                "business_impact_high": "HIGH IMPACT - Significant risks exist that could affect business continuity and generate legal liabilities.",
                "business_impact_moderate": "MODERATE IMPACT - Additional controls required before proceeding with proposed changes.",
                "business_impact_low": "LOW IMPACT - Current security level is appropriate for business operations."
            }
    
    def load_validation_result(self, filepath: Path) -> bool:
        """Carga resultado de validación previa"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.validation_result = json.load(f)
            return True
        except Exception as e:
            print(f"Error cargando resultado de validación: {e}")
            return False
    
    def generate_executive_summary(self) -> Dict:
        """Genera resumen ejecutivo en el idioma configurado"""
        summary = {
            "title": self.translations["report_title"],
            "subtitle": self.translations["report_subtitle"],
            "overall_status": self._translate_status(self.validation_result.get("status", "unknown")),
            "key_findings": [],
            "business_impact": ""
        }
        
        # Traducir hallazgos clave usando las traducciones
        secrets_count = self.validation_result["summary"]["total_secrets"]
        vuln_counts = self.validation_result["summary"]
        
        if secrets_count > 0:
            summary["key_findings"].append(
                self.translations["data_leakage_detected"].format(secrets_count)
            )
        
        if vuln_counts["critical_vulnerabilities"] > 0:
            summary["key_findings"].append(
                self.translations["critical_vulnerabilities_detected"].format(vuln_counts['critical_vulnerabilities'])
            )
        
        if vuln_counts["high_vulnerabilities"] > 0:
            summary["key_findings"].append(
                self.translations["high_vulnerabilities_detected"].format(vuln_counts['high_vulnerabilities'])
            )
        
        if not summary["key_findings"]:
            summary["key_findings"].append(
                self.translations["no_critical_issues"]
            )
        
        # Impacto empresarial traducido
        if self.validation_result["status"] == "failed":
            summary["business_impact"] = self.translations["business_impact_high"]
        elif self.validation_result["status"] == "requires_approval":
            summary["business_impact"] = self.translations["business_impact_moderate"]
        else:
            summary["business_impact"] = self.translations["business_impact_low"]
        
        return summary
    
    def generate_compliance_analysis(self) -> Dict:
        """Genera análisis de cumplimiento normativo colombiano"""
        compliance = {
            "ley_1581": {
                "title": "Cumplimiento de la Ley 1581 de Protección de Datos",
                "applicability": "Esta ley regula el tratamiento de datos personales en Colombia",
                "findings": [],
                "obligations": [],
                "status": "pending_review"
            },
            "sic": {
                "title": "Consideraciones para la Superintendencia de Industria y Comercio (SIC)",
                "recommendations": []
            }
        }
        
        # Análisis Ley 1581
        ley_1581 = compliance["ley_1581"]
        
        if self.validation_result["compliance"]["ley_1581"]["data_leakage_detected"]:
            ley_1581["findings"].append(
                "Se detectó posible fuga de datos personales, lo que constituye "
                "una violación a los principios de seguridad y confidencialidad "
                "establecidos en la Ley 1581."
            )
            ley_1581["obligations"].append(
                "Notificar al área legal para evaluación de posibles "
                "notificaciones a la SIC y titulares de datos afectados."
            )
            ley_1581["status"] = "requires_action"
        else:
            ley_1581["findings"].append(
                "No se detectaron fugas evidentes de datos personales en el análisis."
            )
            ley_1581["status"] = "compliant"
        
        # Obligaciones generales Ley 1581
        ley_1581["obligations"].extend([
            "Mantener inventario actualizado de datos personales tratados",
            "Implementar medidas técnicas y organizativas apropiadas",
            "Designar responsable del tratamiento de datos personales",
            "Establecer procedimientos para ejercicio de derechos ARCO"
        ])
        
        # Recomendaciones SIC
        compliance["sic"]["recommendations"] = [
            "Documentar los controles de seguridad implementados",
            "Mantener registros de evaluaciones de seguridad periódicas",
            "Establecer procedimientos para gestión de incidentes de seguridad",
            "Capacitar al personal en protección de datos personales"
        ]
        
        return compliance
    
    def generate_recommendations(self) -> List[str]:
        """Genera recomendaciones específicas para el contexto colombiano"""
        recommendations = []
        
        # Recomendaciones técnicas
        if self.validation_result["summary"]["total_secrets"] > 0:
            recommendations.append(
                "Implementar sistema de gestión de secretos (ej: HashiCorp Vault, "
                "AWS Secrets Manager) para eliminar credenciales en código fuente."
            )
        
        if self.validation_result["summary"]["critical_vulnerabilities"] > 0:
            recommendations.append(
                "Priorizar la corrección de vulnerabilidades críticas en los "
                "próximos 7 días hábiles, asignando recursos dedicados."
            )
        
        # Recomendaciones organizacionales
        recommendations.extend([
            "Establecer comité de seguridad de la información con participación "
            "de áreas legal, TI y operaciones",
            
            "Implementar programa de concientización en seguridad para todos "
            "los colaboradores, con énfasis en protección de datos personales",
            
            "Realizar auditorías trimestrales de seguridad con enfoque en "
            "cumplimiento de normativa colombiana vigente",
            
            "Documentar procedimientos para respuesta a incidentes de seguridad, "
            "considerando plazos de notificación establecidos por la SIC"
        ])
        
        return recommendations
    
    def generate_html_report(self) -> str:
        """Genera reporte en formato HTML"""
        html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Seguridad - Colombia</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 15px;
            font-size: 1.1em;
            box-shadow: 0 3px 5px rgba(0,0,0,0.2);
        }}
        
        .status-passed {{ 
            background: linear-gradient(135deg, #4caf50, #2e7d32);
            color: white;
            border: 2px solid #2e7d32;
        }}
        .status-requires-approval {{ 
            background: linear-gradient(135deg, #ff9800, #f57c00);
            color: white;
            border: 2px solid #f57c00;
        }}
        .status-failed {{ 
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
            border: 2px solid #d32f2f;
        }}
        
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            border: 1px solid #e0e0e0;
        }}
        
        .section h2 {{
            color: #0d47a1;
            border-bottom: 3px solid #0d47a1;
            padding-bottom: 12px;
            margin-top: 0;
            font-size: 1.8em;
        }}
        
        .severity-card {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 6px solid;
            transition: transform 0.2s;
        }}
        
        .severity-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .severity-critical {{ 
            border-left-color: #d32f2f;
            background: linear-gradient(to right, #ffebee, white);
        }}
        .severity-high {{ 
            border-left-color: #f57c00;
            background: linear-gradient(to right, #fff3e0, white);
        }}
        .severity-medium {{ 
            border-left-color: #ffb300;
            background: linear-gradient(to right, #fff8e1, white);
        }}
        .severity-low {{ 
            border-left-color: #388e3c;
            background: linear-gradient(to right, #e8f5e9, white);
        }}
        
        .secret-finding {{
            background: #fff8e1;
            border-left: 6px solid #ff9800;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        
        .secret-finding.critical {{
            background: #ffebee;
            border-left-color: #f44336;
        }}
        
        .severity-indicator {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 10px;
        }}
        
        .critical-indicator {{ background-color: #f44336; color: white; }}
        .high-indicator {{ background-color: #ff9800; color: white; }}
        .medium-indicator {{ background-color: #ffc107; color: #333; }}
        .low-indicator {{ background-color: #4caf50; color: white; }}
        
        .compliance-section {{
            background: linear-gradient(to right, #e8f5e9, #f1f8e9);
            border-left: 6px solid #2e7d32;
            border-radius: 10px;
            padding: 25px;
        }}
        
        .legal-alert {{
            background: #fff3e0;
            border: 2px solid #ff9800;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        
        .action-required {{
            background: #ffebee;
            border: 2px dashed #f44336;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4); }}
            70% {{ box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }}
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 25px;
            border-top: 2px solid #ddd;
            color: #666;
            font-size: 0.9em;
            background: #f9f9f9;
            border-radius: 8px;
            padding: 25px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            border-top: 4px solid;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        th {{
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background-color: #f5f7fa;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .progress-bar {{
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 10px;
        }}
        
        .critical-progress {{ background: linear-gradient(to right, #f44336, #d32f2f); }}
        .high-progress {{ background: linear-gradient(to right, #ff9800, #f57c00); }}
        .medium-progress {{ background: linear-gradient(to right, #ffc107, #ffa000); }}
        .low-progress {{ background: linear-gradient(to right, #4caf50, #388e3c); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Reporte de Seguridad Informática</h1>
        <div class="subtitle">
            Análisis automatizado para aplicaciones web - Contexto Colombiano
        </div>
        <div class="status-badge status-{status_class}">
            Estado: {overall_status}
        </div>
    </div>
    
    <div class="section">
        <h2>📋 Resumen Ejecutivo</h2>
        <p><strong>Fecha de generación:</strong> {generated_at}</p>
        <p><strong>Jurisdicción:</strong> Colombia</p>
        <p><strong>Zona horaria:</strong> America/Bogota</p>
        
        <h3>Hallazgos Principales</h3>
        <ul>
            {key_findings_html}
        </ul>
        
        <h3>Impacto Empresarial</h3>
        <p>{business_impact}</p>
    </div>
    
    <div class="section">
        <h2>📊 Resumen de Hallazgos</h2>
        <table>
            <tr>
                <th>Tipo de Hallazgo</th>
                <th>Cantidad</th>
                <th>Nivel de Riesgo</th>
            </tr>
            {summary_table_rows}
        </table>
    </div>
    
    <div class="section compliance-section">
        <h2>🏛️ Cumplimiento Normativo - Ley 1581</h2>
        <h3>Análisis de Cumplimiento</h3>
        <ul>
            {ley_1581_findings_html}
        </ul>
        
        <h3>Obligaciones Detectadas</h3>
        <ul>
            {ley_1581_obligations_html}
        </ul>
        
        <h3>Estado de Cumplimiento: <strong>{ley_1581_status}</strong></h3>
        
        <h3>Recomendaciones para la SIC</h3>
        <ul>
            {sic_recommendations_html}
        </ul>
    </div>
    
    <div class="section">
        <h2>🎯 Recomendaciones Específicas</h2>
        <h3>Para el Contexto Colombiano</h3>
        <ul>
            {recommendations_html}
        </ul>
    </div>
    
    <div class="footer">
        <p>Este reporte fue generado automáticamente por el Security Pipeline Colombia</p>
        <p>Para preguntas técnicas: equipo.seguridad@empresa.co</p>
        <p>Para asuntos legales: legal.compliance@empresa.co</p>
        <p>© {current_year} - Todos los derechos reservados</p>
    </div>
</body>
</html>"""
        
        # Preparar datos para la plantilla
        executive_summary = self.generate_executive_summary()
        compliance = self.generate_compliance_analysis()
        recommendations = self.generate_recommendations()
        
        # Determinar clase CSS para el estado
        status_class = self.validation_result["status"]
        if status_class == "passed":
            status_class = "passed"
        elif status_class == "requires_approval":
            status_class = "requires-approval"
        else:
            status_class = "failed"
        
        # Generar HTML para listas
        key_findings_html = "".join([
            f"<li>{html.escape(finding)}</li>"
            for finding in executive_summary["key_findings"]
        ])
        
        # Tabla de resumen
        summary = self.validation_result["summary"]
        summary_table_rows = f"""
            <tr>
                <td>Secretos expuestos</td>
                <td>{summary['total_secrets']}</td>
                <td>{'Alto' if summary['total_secrets'] > 0 else 'N/A'}</td>
            </tr>
            <tr>
                <td>Vulnerabilidades críticas</td>
                <td>{summary['critical_vulnerabilities']}</td>
                <td>Crítico</td>
            </tr>
            <tr>
                <td>Vulnerabilidades altas</td>
                <td>{summary['high_vulnerabilities']}</td>
                <td>Alto</td>
            </tr>
            <tr>
                <td>Vulnerabilidades medias</td>
                <td>{summary['medium_vulnerabilities']}</td>
                <td>Medio</td>
            </tr>
            <tr>
                <td>Vulnerabilidades bajas</td>
                <td>{summary['low_vulnerabilities']}</td>
                <td>Bajo</td>
            </tr>
        """
        
        # Ley 1581
        ley_1581_findings_html = "".join([
            f"<li>{html.escape(finding)}</li>"
            for finding in compliance["ley_1581"]["findings"]
        ])
        
        ley_1581_obligations_html = "".join([
            f"<li>{html.escape(obligation)}</li>"
            for obligation in compliance["ley_1581"]["obligations"]
        ])
        
        # SIC
        sic_recommendations_html = "".join([
            f"<li>{html.escape(recommendation)}</li>"
            for recommendation in compliance["sic"]["recommendations"]
        ])
        
        # Recomendaciones generales
        recommendations_html = "".join([
            f"<li>{html.escape(recommendation)}</li>"
            for recommendation in recommendations
        ])
        
        # Rellenar plantilla
        html_content = html_template.format(
            status_class=status_class,
            overall_status=self._translate_status(self.validation_result["status"]).upper(),
            generated_at=self.report_data["metadata"]["generated_at"],
            key_findings_html=key_findings_html,
            business_impact=html.escape(executive_summary["business_impact"]),
            summary_table_rows=summary_table_rows,
            ley_1581_findings_html=ley_1581_findings_html,
            ley_1581_obligations_html=ley_1581_obligations_html,
            ley_1581_status=compliance["ley_1581"]["status"].upper(),
            sic_recommendations_html=sic_recommendations_html,
            recommendations_html=recommendations_html,
            current_year=datetime.now().year
        )
        
        return html_content
    
    def generate_markdown_report(self) -> str:
        """Genera reporte en formato Markdown"""
        executive_summary = self.generate_executive_summary()
        compliance = self.generate_compliance_analysis()
        recommendations = self.generate_recommendations()
        
        md = f"""# Reporte de Seguridad Informática
## Análisis automatizado para aplicaciones web - Contexto Colombiano

**Fecha de generación:** {self.report_data['metadata']['generated_at']}
**Jurisdicción:** Colombia
**Zona horaria:** America/Bogota

## 📋 Resumen Ejecutivo

**Estado general:** {self._translate_status(self.validation_result['status']).upper()}

### Hallazgos Principales
"""
        
        for finding in executive_summary["key_findings"]:
            md += f"- {finding}\n"
        
        md += f"\n### Impacto Empresarial\n{executive_summary['business_impact']}\n"
        
        md += f"""
## 📊 Resumen de Hallazgos

| Tipo de Hallazgo | Cantidad | Nivel de Riesgo |
|------------------|----------|-----------------|
| Secretos expuestos | {self.validation_result['summary']['total_secrets']} | {'Alto' if self.validation_result['summary']['total_secrets'] > 0 else 'N/A'} |
| Vulnerabilidades críticas | {self.validation_result['summary']['critical_vulnerabilities']} | Crítico |
| Vulnerabilidades altas | {self.validation_result['summary']['high_vulnerabilities']} | Alto |
| Vulnerabilidades medias | {self.validation_result['summary']['medium_vulnerabilities']} | Medio |
| Vulnerabilidades bajas | {self.validation_result['summary']['low_vulnerabilities']} | Bajo |
"""
        
        md += f"""
## 🏛️ Cumplimiento Normativo - Ley 1581

### Análisis de Cumplimiento
"""
        
        for finding in compliance["ley_1581"]["findings"]:
            md += f"- {finding}\n"
        
        md += f"\n### Obligaciones Detectadas\n"
        for obligation in compliance["ley_1581"]["obligations"]:
            md += f"- {obligation}\n"
        
        md += f"\n### Estado de Cumplimiento: **{compliance['ley_1581']['status'].upper()}**\n"
        
        md += f"\n### Recomendaciones para la SIC\n"
        for recommendation in compliance["sic"]["recommendations"]:
            md += f"- {recommendation}\n"
        
        md += f"""
## 🎯 Recomendaciones Específicas

### Para el Contexto Colombiano
"""
        
        for recommendation in recommendations:
            md += f"- {recommendation}\n"
        
        md += f"""
---

*Este reporte fue generado automáticamente por el Security Pipeline Colombia*

**Para preguntas técnicas:** equipo.seguridad@empresa.co  
**Para asuntos legales:** legal.compliance@empresa.co  

© {datetime.now().year} - Todos los derechos reservados
"""
        
        return md
    
    def _translate_status(self, status: str) -> str:
        """Traduce estados técnicos según el idioma configurado"""
        translation_map = {
            "passed": self.translations["status_passed"],
            "failed": self.translations["status_failed"],
            "requires_approval": self.translations["status_requires_approval"],
            "unknown": self.translations["status_unknown"]
        }
        return translation_map.get(status, status)


def main():
    parser = argparse.ArgumentParser(
        description="Generador de reportes de seguridad multilingüe",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--validation",
        required=True,
        help="Ruta al archivo JSON de resultado de validación"
    )
    
    parser.add_argument(
        "--output",
        default="security-report.html",
        help="Nombre base para archivos de salida (se generarán .html y .md)"
    )
    
    parser.add_argument(
        "--format",
        choices=['html', 'markdown', 'both'],
        default='both',
        help="Formato de salida"
    )
    
    parser.add_argument(
        "--language",
        default="es_CO",
        choices=['es_CO', 'es', 'en'],
        help="Idioma del reporte"
    )
    
    parser.add_argument(
        "--secrets",
        help="Ruta al archivo de resultados de gitleaks (JSON)"
    )
    
    parser.add_argument(
        "--sast",
        help="Ruta al archivo de resultados de SAST (SARIF)"
    )
    
    args = parser.parse_args()
    
    generator = SecurityReportGenerator(language=args.language)
    
    if not generator.load_validation_result(Path(args.validation)):
        print("Error: No se pudo cargar el resultado de validación")
        sys.exit(1)
    
    # Generar reportes según formato solicitado
    if args.format in ['html', 'both']:
        html_content = generator.generate_html_report()
        html_path = Path(args.output)
        if not args.output.endswith('.html'):
            html_path = Path(f"{args.output}.html")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    if args.format in ['markdown', 'both']:
        md_content = generator.generate_markdown_report()
        md_path = Path(args.output)
        if not args.output.endswith('.md'):
            md_path = Path(f"{args.output}.md")
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    # Mensaje de éxito traducido
    success_msg = {
        "es_CO": "✅ Reportes generados exitosamente:",
        "es": "✅ Reportes generados exitosamente:",
        "en": "✅ Reports generated successfully:"
    }
    
    summary_msg = {
        "es_CO": "📋 Resumen del análisis:",
        "es": "📋 Resumen del análisis:",
        "en": "📋 Analysis summary:"
    }
    
    lang = args.language[:2]  # Tomar primeros 2 caracteres
    
    print(f"{success_msg.get(lang, success_msg['es_CO'])}")
    
    if args.format in ['html', 'both']:
        print(f"   • HTML: {html_path}")
    if args.format in ['markdown', 'both']:
        print(f"   • Markdown: {md_path}")
    
    print(f"\n{summary_msg.get(lang, summary_msg['es_CO'])}")
    print(f"   Status: {generator._translate_status(generator.validation_result['status']).upper()}")
    print(f"   Secrets detected: {generator.validation_result['summary']['total_secrets']}")
    print(f"   Critical/High vulnerabilities: {generator.validation_result['summary']['critical_vulnerabilities'] + generator.validation_result['summary']['high_vulnerabilities']}")


if __name__ == "__main__":
    import sys
    main()