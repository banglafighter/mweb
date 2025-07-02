### In the name of God, the Most Gracious, the Most Merciful.

# MWeb - Manageable Web Framework of Python
Python Manageable Web Framework (MWeb). MWeb is a DRY full-stack framework based on PWeb framework.


<br/><br/><br/>
## Documentation

### Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):
```bash
pip install -U mweb
```

### Create a project using CLI
```bash
mwebcli project init -n <specify_project_name>
```
It will automatically create a project with the name. For example, the project name is **example** then it will create
an example directory and initialize the project in it.

### Run the project 
```bash
cd <specify_project_name>

# If windows then active the virtual environment using below command
venv\Scripts\activate

# For Linux or MacOS
source venv\bin\activate

# Run project using below command
python mweb_app.py
```
The project will run in http://127.0.0.1:1212



<br/><br/>

**Please find [the Documentation](https://mweb.banglafighter.org/) with example from [hmtmcse.com/mweb](https://hmtmcse.com/mweb)**


<br/><br/><br/>
## Donate
[Bangla Fighter](https://banglafighter.com/) develops and supports MWeb and the libraries it uses. To grow
the community of contributors and users, and allow the maintainers to devote more time to the projects.

<a target="_blank" href="https://www.buymeacoffee.com/banglafighter" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me Us Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


<br/><br/><br/>
## Contributing
For guidance on setting up a development environment and how to make a contribution to MWeb, see the contributing guidelines.


<br/><br/><br/>
## Links
* **Changes :** [https://mweb.banglafighter.org/release/latest](https://mweb.banglafighter.org/release/latest)
* **PyPI Releases :** [https://pypi.org/project/mweb](https://pypi.org/project/mweb)
* **Source Code :** [https://github.com/banglafighter/mweb](https://github.com/banglafighter/mweb)
* **Issue Tracker :** [https://github.com/banglafighter/mweb/issues](https://github.com/banglafighter/mweb/issues)
* **Website :** [https://mweb.banglafighter.org](https://mweb.banglafighter.org)


<br/><br/><br/>

## Modules & Responsibilities

| Package Name      | Actual Name                       | Description                                                                                                                                         |
|-------------------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `mweb`            | MWeb                              | MWeb - Manageable Web Framework for Python                                                                                                          |
| `mweb-orm`        | MWeb Object-Relational Mapper     | MWeb Object-Relational Mapper, based on SQLAlchemy, is an open-source SQL toolkit and object-relational mapper.                                     |
| `mweb-cli`        | MWeb Command Line Interface       | Command line interface tools for MWeb application, which make MWeb work easy and automatic from terminal or CMD.                                    |
| `mweb-auth`       | MWeb Authentication               | MWeb authentication system, which allows managing application basic level authentication, but it can be extended.                                   |
| `mweb-crud`       | MWeb Create, Read, Update, Delete | Helps to easily perform Create, Read, Update, & Delete operations for REST-API and server-side rendering data processing, and can generate OpenAPI. |
| `mweb-ssr`        | MWeb Server Side Renderer         | Server-side rendered UI, forms, table headers, items per page, pagination, and Jinja customization.                                                 |
| `mweb-builtin`    | MWeb Built-In Functionality       | Built-in helpers for email, task scheduling, and other useful features needed for development.                                                      |
| `mweb-http`       | MWeb HTTP Client                  | Responsible for connecting to MWeb using HTTP; understands API calls and responses with authentication.                                             |
| `mweb-ui`         | MWeb Bootstrap UI                 | Server-side rendered UI, built on the latest Bootstrap version.                                                                                     |
| `mweb-react`      | MWeb React UI                     | React-based UI framework.                                                                                                                           |
| `mw-common`       | MWeb Common Utilities             | Provides common utilities to simplify development tasks.                                                                                            |
| `mw-file-content` | MWeb File & Content Helper        | Library for performing text read/write operations and file/directory manipulation.                                                                  |
| `mweb-dev`        | MWeb Source Development           | This project is helps to source development of the MWeb Framework.                                                                                  |
