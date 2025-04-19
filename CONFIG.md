# CONFIG.md

## Configuration File Reference (`options.json`)

This document provides a complete and detailed overview of the structure, valid values, and usage of the `options.json` configuration file used by QRMaster. This file allows full control over the behavior and outcome of the QR code generation process. The file must be a valid JSON object and is required for most of the application's commands. The application has an options.json file validation command that will allow you to check its validity.

To validate the configuration file, access this link.

---

## 📁 Root Structure

The root of the configuration contains a single key:

```json
{
  "project": {
    "name": "",
    "content": { ... },
    "output": { ... },
    "logo": { ... },
    "art": { ... },
    "frame": { ... },
    "pdf": { ... },
    "report": { ... }
  }
}
```

---

## 🔹 `project` (object) - **Required**

This is the main container for the project settings. It includes all the necessary configurations for content, output, design, and document generation.

### `project.name` (string)
Name of the project used to define directories and output files.

**Example**:
```json
"name": "client"
```

---

## 🔸 `content` (object) - **Required**

Specifies the QR content to be encoded.

### Fields:
- `type` (string): Type of content
	- **Allowed values:**  
	  - `"url"`  
	  - `"text"`  
	  - `"email"`  
	  - `"wifi"`  
	  - `"geo"`  
	  - `"mecard"`  
	  - `"vcard"`  
	  - `"epc"`

- `data` (object): Specific fields based on content type

**Example**:
```json
"content": {
  "type": "url",
  "data": {
    "url": "https://github.com/remizero/qrmaster"
  }
}
```

---

## 🖨️ `output` (object) - **Optional**

Defines the output formats and styling parameters.

### `formats` (array of strings)
List of formats to export: `svg`, `png`, `pdf`

### `params` (object)
- `scale` (number): Size scaling factor
- `border` (int): Border size in modules
- `unit` (string): Output unit (e.g., `px`, `mm`)
- `dark` (string): Dark color of the QR code

**Example**:
```json
"output": {
  "formats": ["svg", "png", "pdf"],
  "params": {
    "scale": 10,
    "border": 5,
    "unit": "px",
    "dark": "black"
  }
}
```

---

## 🖼️ `logo` (object) - **Optional**

Defines the options for embedding a logo into the QR code.

### Fields:
- `path` (string): path to image file.

**Example**:
```json
"logo": {
  "path": "path/to/logo.png"
}
```

---

## 🖼️ `frame` (object) - **Optional**

Defines the visual frame surrounding the QR code.

### Fields:
- `margin` (int)
- `text_height` (int)
- `background_color` (string)
- `border_color` (string)
- `border_width` (int)
- `title` (string)
- `title_font_size` (int)
- `title_font_family` (string)
- `title_color` (string)
- `message` (string)
- `message_font_size` (int)
- `message_color` (string)

---

## 📄 `pdf` (object) - **Optional**

Defines the layout and content of the generated printable PDF.

### Fields:
- `title`, `subtitle`, `document_name` (string)
- `title_font`, `info_font` (string)
- `title_size`, `info_size` (int)
- `title_style` (string): e.g., `B`, `I`, `U`
- `include_date` (bool)
- `date_format` (string)
- `image_path` (string)
- `image_width`, `image_x`, `image_y` (int)
- `output_name` (string)

---

## 🖌️ `art` (object) - *Reserved for future artistic customization*
Currently unused.

---

## 📊 `report` (object) - **Optional**

Settings for the generation of a technical PDF report.

### `metadata` (object)
- `author`, `title`, `subject`, `keywords`, `creator` (string)

### `include_date` (bool), `date_format` (string)

### `title`, `subtitle`, `paragraph` (objects)
- `font` (string)
- `size` (int)
- `style` (string)

### `header` (object)
- `color` ([R, G, B])
- `company_name` (string)
- `company_logo` (string)

### `footer` (object)
- `color` ([R, G, B])
- `contact` (string)
- `website` (string)
- `social` (object): Contains social network handles (e.g., `linkedin`, `facebook`, `github`, etc.)

---

## ✅ Notes
- All string color values must be valid CSS-compatible color formats (`#RRGGBB`, `black`, etc.)
- Dates use Python-compatible `strftime` formats.

---

## 📌 Example Snippet
```json
{
  "project": {
    "name": "client",
    "content": {
      "type": "url",
      "data": {
        "url": "https://github.com/remizero/qrmaster"
      }
    }
  }
}
```
```

