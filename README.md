# QR Master
QRMaster is an application that allows you to generate QR codes in a simple yet professional way.
QRMaster, es una aplicación desarrollada en python que permite generar códigos QR de manera simple pero profesional.

## Download
```bash
 git clone https://github.com/remizero/qrmaster.git
```

## Install
```bash
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
```

## Run
```bash
 python3 qrgen.py --options options.json
```

## Options

```json
{
 "project": {
 "name": "my_project",
 "content": {
 "type": "url",
 "url": "https://example.com"
 }
 }
}
```
