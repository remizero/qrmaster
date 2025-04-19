# Usage

QRMaster is currently controlled via command line. All commands expect a structured configuration JSON file as input. Below are the available commands and usage examples.


## Command Line Interface (CLI)


### Generate a QR Code

To generate a QR code, use the following command:

```bash
python main.py generate --config path/to/config.json
```


### Generate a Report

To generate a technical report about the project:

```bash
python main.py report --config path/to/config.json
```


### Validate Configuration

To validate the configuration file:

```bash
python main.py validate --config path/to/config.json
```


### View Logs

To view the logs:

```bash
python main.py viewLog --path path/to/logfile.log
```


### View last 10 lines

```bash
python cli.py view-log --tail 10
```


### View with pagination (less style)

```bash
python cli.py view-log --paginate
```


### View the log of a specific project

```bash
python cli.py view-log --path projects/qr_evento/state.log --tail 20
```


### Clear Logs

To clear the logs:

```bash
python main.py clearLog --path path/to/logfile.log
```


## Graphical User Interface (GUI)

Coming soon...
