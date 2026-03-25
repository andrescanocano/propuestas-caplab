"""
Generador de propuestas comerciales HTML para Capital Lab.
Uso: python gen_propuesta.py --config propuesta.json --output docs/2026/cliente-servicio/
"""
import argparse
import base64
import json
import os
import sys

# Rutas de logos (base64 pre-generados)
LOGO_H_PATH = os.path.join(os.path.dirname(__file__), "..", "logo_b64.txt")          # Negro
LOGO_C_PATH = os.path.join(os.path.dirname(__file__), "..", "logo_circle_b64.txt")   # Negro
LOGO_W_PATH = os.path.join(os.path.dirname(__file__), "..", "logo_blanco_b64.txt")   # Blanco (banner)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, "base_propuesta.html")


def load_logo(path):
    """Carga un logo como data URI desde archivo base64."""
    with open(path, "r", encoding="utf-8") as f:
        b64 = f.read().strip()
    return f"data:image/png;base64,{b64}"


def render_section(section):
    """Renderiza una seccion del JSON a HTML."""
    tipo = section.get("tipo", "texto")
    html_parts = []

    # Titulo de seccion
    if "etiqueta" in section:
        html_parts.append(f'<div class="section-title">{section["etiqueta"]}</div>')
    if "titulo" in section:
        html_parts.append(f'<h2>{section["titulo"]}</h2>')
    if "texto" in section:
        for p in (section["texto"] if isinstance(section["texto"], list) else [section["texto"]]):
            html_parts.append(f"<p>{p}</p>")

    # Tipos de contenido
    if tipo == "checklist" and "items" in section:
        html_parts.append('<ul class="checklist">')
        for item in section["items"]:
            html_parts.append(f"  <li>{item}</li>")
        html_parts.append("</ul>")

    elif tipo == "lista" and "items" in section:
        html_parts.append('<ul class="item-list">')
        for item in section["items"]:
            html_parts.append(f"  <li>{item}</li>")
        html_parts.append("</ul>")

    elif tipo == "cards" and "cards" in section:
        html_parts.append('<div class="cards">')
        for card in section["cards"]:
            html_parts.append('<div class="card">')
            if "etiqueta" in card:
                html_parts.append(f'  <div class="card-label">{card["etiqueta"]}</div>')
            if "titulo" in card:
                html_parts.append(f'  <div class="card-title">{card["titulo"]}</div>')
            if "texto" in card:
                html_parts.append(f'  <div class="card-text">{card["texto"]}</div>')
            html_parts.append("</div>")
        html_parts.append("</div>")

    elif tipo == "fases" and "fases" in section:
        html_parts.append('<div class="phases">')
        for i, fase in enumerate(section["fases"], 1):
            html_parts.append('<div class="phase">')
            html_parts.append(f'  <div class="phase-number">Fase {i}</div>')
            html_parts.append(f'  <div class="phase-title">{fase.get("titulo", "")}</div>')
            html_parts.append(f'  <div class="phase-text">{fase.get("texto", "")}</div>')
            if "tiempo" in fase:
                html_parts.append(f'  <div class="phase-time">{fase["tiempo"]}</div>')
            html_parts.append("</div>")
        html_parts.append("</div>")

    elif tipo == "tabla" and "filas" in section:
        cols = section.get("columnas", ["Concepto", "Valor"])
        html_parts.append('<table class="invest-table">')
        html_parts.append("<thead><tr>")
        for col in cols:
            cls = ' class="amount"' if col.lower() in ("valor", "inversion", "precio") else ""
            html_parts.append(f"  <th{cls}>{col}</th>")
        html_parts.append("</tr></thead>")
        html_parts.append("<tbody>")
        for fila in section["filas"]:
            html_parts.append("<tr>")
            for j, celda in enumerate(fila):
                cls = ' class="amount"' if j == len(fila) - 1 else ""
                html_parts.append(f"  <td{cls}>{celda}</td>")
            html_parts.append("</tr>")
        html_parts.append("</tbody></table>")

    elif tipo == "dos_columnas" and "columnas" in section:
        html_parts.append('<div class="two-col">')
        for col in section["columnas"]:
            html_parts.append("<div>")
            if "titulo" in col:
                html_parts.append(f'<div class="card-label">{col["titulo"]}</div>')
            if "items" in col:
                html_parts.append('<ul class="item-list">')
                for item in col["items"]:
                    html_parts.append(f"  <li>{item}</li>")
                html_parts.append("</ul>")
            html_parts.append("</div>")
        html_parts.append("</div>")

    # Nota opcional
    if "nota" in section:
        html_parts.append(f'<div class="note">{section["nota"]}</div>')

    return f'<div class="section">\n' + "\n".join(html_parts) + "\n</div>"


def generate(config_path, output_dir, template_name=None):
    """Genera la propuesta HTML desde un JSON de configuracion."""
    # Cargar config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Cargar template
    tpl_path = os.path.join(TEMPLATES_DIR, template_name) if template_name else TEMPLATE_PATH
    with open(tpl_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Cargar logos
    logo_h = load_logo(LOGO_H_PATH)
    logo_c = load_logo(LOGO_C_PATH)
    logo_w = load_logo(LOGO_W_PATH)

    # Renderizar secciones
    secciones_html = "\n\n".join(render_section(s) for s in config.get("secciones", []))

    # Reemplazar placeholders
    html = template
    html = html.replace("{{TITULO}}", config.get("titulo", "Propuesta - Capital Lab"))
    html = html.replace("{{LOGO_HORIZONTAL}}", logo_h)
    html = html.replace("{{LOGO_BLANCO}}", logo_w)
    html = html.replace("{{LOGO_CIRCLE}}", logo_c)
    html = html.replace("{{FECHA}}", config.get("fecha", ""))
    html = html.replace("{{REFERENCIA}}", config.get("referencia", ""))
    html = html.replace("{{TITULO_HERO}}", config.get("titulo_hero", ""))
    html = html.replace("{{SUBTITULO}}", config.get("subtitulo", ""))
    html = html.replace("{{SECCIONES}}", secciones_html)
    html = html.replace("{{CTA_TITULO}}", config.get("cta_titulo", "<strong>Hablemos</strong>"))
    html = html.replace("{{CTA_TEXTO}}", config.get("cta_texto", "Queremos entender tu negocio para disenar una solucion a la medida."))

    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size = len(html)
    print(f"Propuesta generada: {output_path}")
    print(f"Tamano: {size:,} caracteres")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Genera propuestas HTML para Capital Lab")
    parser.add_argument("--config", required=True, help="Ruta al JSON de configuracion")
    parser.add_argument("--output", required=True, help="Directorio de salida (ej: docs/2026/pipe-contabilidad/)")
    parser.add_argument("--template", default=None, help="Nombre del template (ej: propuesta_marca.html)")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: no se encontro {args.config}")
        sys.exit(1)

    generate(args.config, args.output, args.template)


if __name__ == "__main__":
    main()
