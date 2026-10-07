# Notes API

Ein kleiner REST-Dienst für Notizen, gebaut mit FastAPI und Pydantic v2. Notizen
liegen ausschließlich im Arbeitsspeicher des Prozesses (keine Datenbank); die
Konfiguration wird über `pydantic-settings` aus Umgebungsvariablen gelesen.
Der Dienst stellt Endpunkte zum Anlegen, Auflisten (optional nach Tag gefiltert),
Abrufen und Löschen von Notizen bereit.

## Tech Stack

- **Sprache**: Python 3.11+
- **Framework**: FastAPI
- **Validierung**: Pydantic v2 (`model_config`, `field_validator`)
- **Konfiguration**: pydantic-settings
- **Server**: uvicorn
- **Speicher**: In-Memory (keine Datenbank)
- **Tests**: pytest + FastAPI `TestClient` (httpx)
- **Linting**: ruff

## Installation

```bash
py -m pip install -r requirements.txt
```

## Starten (Entwicklung)

```bash
py -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Danach ist die API unter `http://localhost:8000` erreichbar, die interaktive
Dokumentation unter `http://localhost:8000/docs`.

## Umgebungsvariablen

Beide Variablen sind optional; ohne sie startet der Dienst mit Defaults.

| Variable    | Default     | Beschreibung                     |
| ----------- | ----------- | -------------------------------- |
| `APP_NAME`  | `Notes API` | Name der Anwendung                |
| `LOG_LEVEL` | `INFO`      | Log-Level                        |

## Tests

```bash
py -m pytest
```

## Endpunkte

| Methode  | Pfad                | Body / Parameter    | Antwort                          |
| -------- | ------------------- | ------------------- | -------------------------------- |
| `GET`    | `/health`           | –                   | `200` `{"status":"ok","app_name":"Notes API"}` |
| `POST`   | `/notes`            | `NoteCreate` (JSON) | `201` `Note`; `422` bei ungültigem Body |
| `GET`    | `/notes`            | `?tag=<str>` (optional) | `200` `list[Note]`; leere Liste ohne Treffer |
| `GET`    | `/notes/{note_id}`  | –                   | `200` `Note`; `404` bei unbekannter id |
| `DELETE` | `/notes/{note_id}`  | –                   | `204` (leerer Body); `404` bei unbekannter id |

### Schemas

`NoteCreate`:

```json
{
  "titel": "Einkaufsliste",
  "inhalt": "Milch, Brot",
  "tags": ["privat"]
}
```

`Note`:

```json
{
  "id": 1,
  "titel": "Einkaufsliste",
  "inhalt": "Milch, Brot",
  "tags": ["privat"],
  "erstellt_am": "2026-10-08T12:00:00Z"
}
```

Für `titel` gilt: 1 bis 100 Zeichen. `tags` darf höchstens 5 Einträge enthalten.
