.. QRMaster documentation master file, created by
   sphinx-quickstart on Sun Apr 20 19:44:24 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

QRMaster: A Flexible QR Code Generator – v1.0.0
===============================================

QRMaster is a modular and extensible tool designed for creating and customizing QR codes with various content types, including URLs, email addresses, WiFi credentials, geolocation data, meCard, vCard, EPC, and more.

Built on top of the powerful **Segno** QR code generator library, QRMaster provides a developer-friendly experience with a clean architecture, centralized configuration, and advanced output capabilities. It is ideal for technical users, designers, and developers who need precision, automation, and professional output for both digital and printed QR code assets.

Whether you're creating a single code or batch-generating hundreds with metadata, QRMaster is built to scale with your workflow.

Features
========

- ✅ Generate QR codes for multiple data types: URLs, email, WiFi, geo, vCard, meCard, EPC, and more.
- 🖼️ Output in multiple formats: SVG, PNG, and printable PDF.
- 🎨 Fully customizable QR designs: control scale, border, color, background, and quiet zones.
- 🧩 Supports embedded logos, style layering, custom frames, and metadata injection.
- 📄 Generates ready-to-print PDF sheets and detailed technical documentation.
- ⚙️ CLI-first approach with centralized `JSON` configuration support.
- 📦 Packaged for Python distribution: installable via `pip`, usable as a command-line tool or importable module.
- 🔧 Built for modularity, testability, and clean separation of concerns.

Quickstart
==========

To get started, install the package, prepare your `options.json` file, and run:

.. code-block:: console

   python3 -m qrmaster generate --config options.json

For full usage details, examples, and reference, see the accompanying pages:

- :doc:`CONFIG <CONFIG>`
- :doc:`EXAMPLES <EXAMPLES>`
- :doc:`INSTALL <INSTALL>`
- :doc:`RUN <RUN>`

Explore. Customize. Generate.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   CONFIG
   EXAMPLES
   INSTALL
   RUN
