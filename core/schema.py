
schemaObj = {
  "type": "object",
  "properties": {
    "project": {
      "type": "object",
      "required": ["name", "content"],
      "properties": {
        "name": { "type": "string" },
        "content": {
          "type": "object",
          "required": ["type", "data"],
          "properties": {
            "type": {
              "type": "string",
              "enum": ["url", "wifi", "geo", "vcard", "mecard", "email", "epc"]
            },
            "data": {
              "type": "object"
            }
          },
          "allOf": [
            {
              "if": {
                "properties": { "type": { "const": "url" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                      "url": { "type": "string" }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "wifi" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["ssid"],
                    "properties": {
                      "ssid": { "type": "string" },
                      "password": { "type": ["string", "null"] },
                      "security": { "type": ["string", "null"] }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "geo" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["lat", "lng"],
                    "properties": {
                      "lat": { "type": "number" },
                      "lng": { "type": "number" }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "vcard" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["name", "displayname"],
                    "properties": {
                      "name": { "type": "string" },
                      "displayname": { "type": "string" },
                      "email": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "phone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "fax":   { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "videophone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "memo": { "type": ["string", "null"] },
                      "nickname": { "type": ["string", "null"] },
                      "birthday": { "type": ["string", "null"] },
                      "url": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "pobox": { "type": ["string", "null"] },
                      "street": { "type": ["string", "null"] },
                      "city": { "type": ["string", "null"] },
                      "region": { "type": ["string", "null"] },
                      "zipcode": { "type": ["string", "null"] },
                      "country": { "type": ["string", "null"] },
                      "org": { "type": ["string", "null"] },
                      "lat": { "type": ["number", "null"] },
                      "lng": { "type": ["number", "null"] },
                      "source": { "type": ["string", "null"] },
                      "rev": { "type": ["string", "null"] },
                      "title": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "photo_uri": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "cellphone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "homephone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "workphone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "mecard" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                      "name": { "type": "string" },
                      "reading": { "type": ["string", "null"] },
                      "email": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "phone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "videophone": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "memo": { "type": ["string", "null"] },
                      "nickname": { "type": ["string", "null"] },
                      "birthday": { "type": ["string", "null"] },
                      "url": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "pobox": { "type": ["string", "null"] },
                      "roomno": { "type": ["string", "null"] },
                      "houseno": { "type": ["string", "null"] },
                      "city": { "type": ["string", "null"] },
                      "prefecture": { "type": ["string", "null"] },
                      "zipcode": { "type": ["string", "null"] },
                      "country": { "type": ["string", "null"] }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "email" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["to"],
                    "properties": {
                      "to": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }] },
                      "cc": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "bcc": { "anyOf": [{ "type": "string" }, { "type": "array", "items": { "type": "string" } }, { "type": "null" }] },
                      "subject": { "type": ["string", "null"] },
                      "body": { "type": ["string", "null"] }
                    }
                  }
                }
              }
            },
            {
              "if": {
                "properties": { "type": { "const": "epc" } }
              },
              "then": {
                "properties": {
                  "data": {
                    "type": "object",
                    "required": ["name", "iban", "amount"],
                    "properties": {
                      "name": { "type": "string" },
                      "iban": { "type": "string" },
                      "amount": { "type": ["number", "string"] },
                      "text": { "type": ["string", "null"] },
                      "reference": { "type": ["string", "null"] },
                      "bic": { "type": ["string", "null"] },
                      "purpose": { "type": ["string", "null"] },
                      "encoding": {
                        "anyOf": [
                          { "type": "string", "enum": ["UTF-8", "ISO 8859-1", "ISO 8859-2", "ISO 8859-4", "ISO 8859-5", "ISO 8859-7", "ISO 8859-10", "ISO 8859-15"] },
                          { "type": "integer", "enum": [1, 2, 3, 4, 5, 6, 7, 8] }
                        ]
                      }
                    }
                  }
                }
              }
            }
          ]
        },
        "output": {
          "type": "object",
          "required": ["formats"],
          "properties": {
            "formats": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["svg", "png", "eps", "pdf", "txt", "xbm", "ppm"]
              },
              "minItems": 1
            },
            "params": {
              "type": "object",
              "properties": {
                "scale": {
                  "type": "number",
                  "minimum": 1
                },
                "border": {
                  "type": "integer",
                  "minimum": 0
                },
                "unit": {
                  "type": "string",
                  "enum": ["px", "mm", "cm", "in"]
                },
                "dark": {
                  "type": "string"
                },
                "light": {
                  "type": "string"
                }
              },
              "additionalProperties": False
            }
          },
          "additionalProperties": False
        },
        "logo": {
          "type": "object",
          "properties": {
            "path": { "type": "string" }
          },
          "additionalProperties": False
        },
        "frame": {
          "type": "object",
          "properties": {
            "margin": { "type": "number", "minimum": 0 },
            "text_height": { "type": "number", "minimum": 0 },
            "background_color": { "type": "string" },
            "border_color": { "type": "string" },
            "border_width": { "type": "number", "minimum": 0 },
            "title": { "type": "string" },
            "title_font_size": { "type": "number", "minimum": 1 },
            "title_font_family": { "type": "string" },
            "title_color": { "type": "string" },
            "message": { "type": "string" },
            "message_font_size": { "type": "number", "minimum": 1 },
            "message_color": { "type": "string" }
          },
          "additionalProperties": False
        },
        "pdf": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "title_font": { "type": "string" },
            "title_size": { "type": "number", "minimum": 1 },
            "title_style": { "type": "string", "enum": ["", "B", "I", "U"] },
            "info_font": { "type": "string" },
            "info_size": { "type": "number", "minimum": 1 },
            "include_date": { "type": "boolean" },
            "date_format": { "type": "string" },
            "document_name": { "type": "string" },
            "image_path": { "type": "string" },
            "image_width": { "type": "number", "minimum": 0 },
            "image_x": { "type": "number" },
            "image_y": { "type": "number" },
            "output_name": { "type": "string" }
          },
          "additionalProperties": False
        },
        "art": {
          "type": "object"
        },
        "report": {
          "type": "object",
          "properties": {
            "include_date": { "type": "boolean" },
            "date_format": { "type": "string" },

            "metadata": {
              "type": "object",
              "properties": {
                "author": {
                  "type": "string",
                  "description": "Nombre del autor del informe"
                },
                "title": {
                  "type": "string",
                  "description": "Título del informe"
                },
                "subject": {
                  "type": "string",
                  "description": "Asunto del informe"
                },
                "keywords": {
                  "type": "string",
                  "description": "Palabras clave del informe"
                },
                "creator": {
                  "type": "string",
                  "description": "Nombre del creador del informe"
                }
              },
              "required": ["author", "title"],
              "additionalProperties": False
            },

            "title": {
              "type": "object",
              "properties": {
                "font": { "type": "string" },
                "size": { "type": "number" },
                "style": { "type": "string", "enum": ["", "B", "I", "U"] }
              },
              "required": ["font", "size", "style"]
            },

            "subtitle": {
              "type": "object",
              "properties": {
                "font": { "type": "string" },
                "size": { "type": "number" },
                "style": { "type": "string", "enum": ["", "B", "I", "U"] }
              },
              "required": ["font", "size", "style"]
            },

            "paragraph": {
              "type": "object",
              "properties": {
                "font": { "type": "string" },
                "size": { "type": "number" },
                "style": { "type": "string", "enum": ["", "B", "I", "U"] }
              },
              "required": ["font", "size", "style"]
            },

            "header": {
              "type": "object",
              "properties": {
                "color": {
                  "type": "array",
                  "items": { "type": "integer", "minimum": 0, "maximum": 255 },
                  "minItems": 3,
                  "maxItems": 3
                },
                "company_name": { "type": "string" },
                "company_logo": { "type": "string" }
              },
              "required": ["color", "company_name"]
            },

            "footer": {
              "type": "object",
              "properties": {
                "color": {
                  "type": "array",
                  "items": { "type": "integer", "minimum": 0, "maximum": 255 },
                  "minItems": 3,
                  "maxItems": 3
                },
                "contact": { "type": "string" },
                "website": { "type": "string" },
                "social": {
                  "type": "object",
                  "properties": {
                    "linkedin": { "type": "string" },
                    "facebook": { "type": "string" },
                    "instagram": { "type": "string" },
                    "X": { "type": "string" },
                    "youtube": { "type": "string" },
                    "github": { "type": "string" },
                    "gitlab": { "type": "string" }
                  },
                  "additionalProperties": False
                }
              },
              "required": ["color", "contact", "website"]
            }
          },
          "required": ["title", "subtitle", "paragraph", "header", "footer"]
        }
      },
      "additionalProperties": False
    }
  },
  "required": ["project"],
  "additionalProperties": False
}
