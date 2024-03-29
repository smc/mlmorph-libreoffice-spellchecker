# Malayalam spelling checker extension for Libreoffice

This is Malayalam spelling checker extension for Libreoffice based on mlmoprh - Malayalam morphology analyser

## Requirements

- LibreOffice 4.1 or later (must come with Python 3 or later)
- Make, sed, find and zip for packaging.

## Instructions for packaging

- Install all of the required software listed above.
- Run ```make```. This will build the extensions package under dist folder

## Installation

Run ```make install```

![Libreoffice language options](doc/mlmorph-libreoffice-options.jpg)

![Spellchecking in Libreoffice](doc/mlmorph-libreoffice-spellcheck.png)


## Debugging

Define `MLMORPH_DEBUG` environment variable as follows

```
export MLMORPH_DEBUG=1
```
Then start libreoffice as `libreoffice --writer`

## Thanks

This extension used the [libreoffice-voikkio](https://github.com/voikko/libreoffice-voikko/) project as reference. Thanks to its author Harri Pitkänen.

## License

This package is distributed under the terms of MIT License