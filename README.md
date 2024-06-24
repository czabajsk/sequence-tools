Sequence Tools
==============================

Simple implementations of selected sequence alignments algorithms

Project Organization
------------

    ├── .github
    │   └── workflows        <- Configuration for GitHub Actions workflows
    │       ├── black.yml    <- Configuration for code formatting using Black
    │       ├── mypy.yml     <- Configuration for type checking using MyPy
    │       ├── pylint.yml   <- Configuration for linting code using Pylint
    │       └── pytest.yml   <- Configuration for running tests using Pytes
    │
    ├── notebooks            <- Jupyter notebooks
    │   ├── .gitkeep
    │   └── NeedmanWunschDemo.ipynb  <- Notebook demonstrating the Needleman-Wunsch algorithm
    │
    ├── src                  <- Source code for use in this project
    │   ├── app              <- Frontend part of the application
    │   │   ├── assets
    │   │   │   └── custom-styles.css    <- Custom CSS styles for the application
    │   │   ├── app.py       <- Main application file
    │   │   ├── home_page.py <- Code for the home page of the application
    │   │   └── info_page.py <- Code for the informational page of the application
    │   │
    │   └── features         <- Backend part of the application
    │       ├── needleman_wunsch.py       <- Implementation of the Needleman-Wunsch algorithm              
    │       └── test_needleman_wunsch.py  <- Tests for the Needleman-Wunsch algorithm
    │
    ├── .pylintrc
    ├── .gitignore
    ├── LICENSE
    ├── Makefile             <- Makefile with commands like `make data` or `make train`
    ├── README.md            <- The top-level README for developers using this project
    ├── requirements.in
    ├── requirements.txt     <- The requirements file for reproducing the analysis environment
    └── setup.py             <- Makes project pip installable (pip install -e .) so src can be imported

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
