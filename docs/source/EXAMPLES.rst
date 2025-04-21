Examples for ``options.json``
=============================

This file contains a set of example configurations for QRMaster’s
``options.json`` file. These examples illustrate how to use different
features and combinations of options to generate QR codes tailored to
your needs.

--------------

📦 Basic Example (Minimal Configuration)
----------------------------------------

.. code:: json

   {
     "project": {
       "name": "basic-project",
       "content": {
         "type": "url",
         "data": {
           "url": "https://example.com"
         }
       }
     }
   }

This configuration generates a basic QR code pointing to a URL and saves
it in SVG format.

--------------

⚙️ Advanced Example (Multiple Formats and Style)
------------------------------------------------

.. code:: json

   {
     "project": {
       "name": "advanced-project",
       "content": {
         "type": "wifi",
         "data": {
           "ssid": "MyNetwork",
           "password": "securepass123",
           "encryption": "WPA",
           "hidden": false
         }
       },
       "output": {
         "formats": ["svg", "png", "pdf"],
         "params": {
           "scale": 10,
           "border": 4,
           "unit": "mm",
           "dark": "#000000"
         }
       },
       "frame": {
         "margin": 15,
         "text_height": 50,
         "background_color": "#ffffff",
         "border_color": "#000000",
         "border_width": 5,
         "title": "WiFi QR",
         "title_font_size": 14,
         "title_font_family": "Helvetica",
         "title_color": "#000000",
         "message": "Scan to connect",
         "message_font_size": 10,
         "message_color": "#666"
       }
     }
   }

This example includes style customization and frame configuration along
with multiple output formats.

--------------

🧩 Full Configuration Example (All Optional Nodes and Content Variants)
-----------------------------------------------------------------------

.. code:: json

   {
     "project": {
       "name": "full-project",
       "content": {
         "type": "vcard",
         "data": {
           "name": "Jane Smith",
           "email": "jane@company.com",
           "phone": "+11234567890",
           "company": "Company Ltd",
           "job": "Manager",
           "website": "https://company.com",
           "address": "123 Office Park"
         }
       },
       "output": {
         "formats": ["svg", "png", "pdf"],
         "params": {
           "scale": 8,
           "border": 5,
           "unit": "px",
           "dark": "#333333"
         }
       },
       "logo": {
         "path": "path/to/logo.png"
       },
       "frame": {
         "margin": 10,
         "text_height": 60,
         "background_color": "white",
         "border_color": "#005baa",
         "border_width": 4,
         "title": "Business Contact",
         "title_font_size": 16,
         "title_font_family": "Arial",
         "title_color": "#005baa",
         "message": "Scan to add contact",
         "message_font_size": 12,
         "message_color": "#555"
       },
       "pdf": {
         "title": "Business Card QR",
         "title_font": "Arial",
         "title_size": 16,
         "title_style": "B",
         "info_font": "Arial",
         "info_size": 12,
         "include_date": true,
         "date_format": "%d/%m/%Y",
         "document_name": "Contact Sheet",
         "image_path": "business_qr.png",
         "image_width": 150,
         "image_x": 10,
         "image_y": 50,
         "output_name": "business_card.pdf"
       },
       "report": {
         "metadata": {
           "author": "QRMaster",
           "title": "Informe técnico",
           "subject": "Full Example Report",
           "keywords": "QR, report",
           "creator": "QRMaster"
         },
         "include_date": true,
         "date_format": "%d/%m/%Y",
         "title": {
           "font": "Arial",
           "size": 24,
           "style": "B"
         },
         "subtitle": {
           "font": "Arial",
           "size": 16,
           "style": "B"
         },
         "paragraph": {
           "font": "Arial",
           "size": 12,
           "style": ""
         },
         "header": {
           "color": [50, 50, 90],
           "company_name": "Company",
           "company_logo": "logo.svg"
         },
         "footer": {
           "color": [50, 50, 90],
           "contact": "support@company.com",
           "website": "https://company.com",
           "social": {
             "linkedin": "@company",
             "facebook": "@company",
             "instagram": "@company"
           }
         }
       }
     }
   }

--------------

📂 Content Type Variants
------------------------

Each of the following examples uses a different content type:

1. ``url``
~~~~~~~~~~

.. code:: json

   {
     "type": "url",
     "data": {
       "url": "https://example.com"
     }
   }

2. ``email``
~~~~~~~~~~~~

.. code:: json

   {
     "type": "email",
     "data": {
       "to": "user@example.com",
       "subject": "Hello",
       "body": "This is a test."
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_make_email_data

3. ``wifi``
~~~~~~~~~~~

.. code:: json

   {
     "type": "wifi",
     "data": {
       "ssid": "MyWiFi",
       "password": "password123",
       "encryption": "WPA",
       "hidden": false
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_wifi_data

4. ``geo``
~~~~~~~~~~

.. code:: json

   {
     "type": "geo",
     "data": {
       "latitude": 40.7128,
       "longitude": -74.0060
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_geo_data

5. ``mecard``
~~~~~~~~~~~~~

.. code:: json

   {
     "type": "mecard",
     "data": {
       "name": "John Smith",
       "phone": "+123456789",
       "email": "john@example.com",
       "note": "VIP Client"
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_mecard_data

6. ``vcard``
~~~~~~~~~~~~

.. code:: json

   {
     "type": "vcard",
     "data": {
       "name": "Jane Smith",
       "email": "jane@company.com",
       "phone": "+11234567890",
       "company": "Company Ltd",
       "job": "Manager",
       "website": "https://company.com",
       "address": "123 Office Park"
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_vcard_data

7. ``epc`` (SEPA QR for payments)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   {
     "type": "epc",
     "data": {
       "name": "Recipient Name",
       "iban": "DE89370400440532013000",
       "amount": 50.00,
       "text": "Invoice #1234",
       "bic": "COBADEFFXXX"
     }
   }

..

   | ℹ️ **Note**: To learn about all the parameters available for this
     type of content, please refer to the official Segno documentation:
   | https://segno.readthedocs.io/en/stable/api.html#segno.helpers.make_epc_qr

--------------

   You can combine any of these content types with the features
   demonstrated in the basic or advanced examples.
