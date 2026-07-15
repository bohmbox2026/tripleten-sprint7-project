# tripleten-sprint7-project

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Projecto de ciencia de datos para el bootcamp de tripleten. 

Una aplicacion web siguiendo el esquema de organizacion de la libreria cookiecutter-data-science (CCDS).
La intencion de hacerlo de esta forma fue para ayudar en la organizacion del proyecto y tambien para exponerme a lo que esta libreria incluye, que es un enfoque estandarizado de crear proyectos de datos.

Dado que el objetivo principal de este proyecto es facilitar la implementacion de un proyecto web, la mayor parte del codigo generado en python fue asistida con un LLM.

El proyecto fue subido exitosamente a github.com y a render.com y los enlace tanto del repositorio como de la aplicacion son los siguientes:

github: https://github.com/bohmbox2026/tripleten-sprint7-project.git

render: https://tripleten-sprint7-project-oxdt.onrender.com


## Organizacion de los archivos

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- **Aqui se localiza el archivo de datos**: "vehicles_us.csv"
│
│
├── notebooks          <- Jupyter notebooks. 
│   ├── EDA.ipynb      <- **Este es el notebook de la exploracion de datos**
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         tripleten_sprint7_project and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── tripleten_sprint7_project   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes tripleten_sprint7_project a Python module
    │
    ├── app.py                  <- **Este es el archivo principal de la aplicacion con el codigo del dashboard**
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

