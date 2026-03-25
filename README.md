# Propuestas Capital Lab

Repositorio para hostear propuestas comerciales de Capital Lab via GitHub Pages.

## Estructura

```
docs/                    <- GitHub Pages sirve desde aqui
  CNAME                  <- propuestas.caplab.com.co
  index.html             <- Pagina base
  robots.txt             <- Bloquea indexacion
  2026/                  <- Propuestas por ano
    cliente-servicio/
      index.html         <- Propuesta HTML autocontenida
templates/
  base_propuesta.html    <- Template base reutilizable
gen_propuesta.py         <- Generador parametrizado
```

## Convencion de URLs

`propuestas.caplab.com.co/YYYY/nombre-servicio/`

Ejemplo: `propuestas.caplab.com.co/2026/pipe-constitucion/`

## Generar una propuesta

```bash
python gen_propuesta.py --tipo contabilidad --cliente "Nombre" --output docs/2026/nombre-contabilidad/
```

## Deploy

Push a `main` y GitHub Pages despliega automaticamente desde `/docs`.
