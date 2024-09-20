# dbfxsql


### ✨ Overview

This project aims to synchronize data between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) database. In order to do so, will provides a bi-directional data transfer mechanism, allowing to migrate data from DBF to SQL and vice versa.

&nbsp;

### 🔌 Installation

1. Clone he repository, `git clone https://github.com/j4breu/dbfxsql.git`
2. Create a virtual environment, `python -m venv .venv`
3. Activate the virtual environment, `source .venv/bin/activate`
4. Install dependencies, `pip install -r requirements.txt`
5. Run the app, `python run.py` or `python -m dbfxsql`

&nbsp;

### 💻 Usage


&nbsp;

### 📝 Roadmap

**Required:**
- [x] Create a CRUD to handle DBF and SQL
- [x] Transfer data between DBF and SQL
- [x] Make a CLI to manage DBF and SQL
- [x] Registry file changes in a pool
- [ ] Compare records to sync specific fields
- [x] Set up a cron job to sync data

**Desirable:**
- [x] Upload to Github
- [x] Handle dynamic fields between databases
- [x] Send the location into the queries
- [x] Handle dynamic parameters as input
- [x] Assign the proper type to the values
- [x] Allow add fields in DBF (incremental id)
- [x] Get database folder paths from .env
- [x] Change detection in folders/files
- [x] Make a video to explain the project
- [x] Use config file to delimiter databases/tables/fields
- [ ] Allow get specific fields from a SELECT query
- [ ] Validate Key Error for an invalid field
- [ ] Validate the length and all other similar names for types in DBF and SQL
- [ ] Allow relations+2 tables in the config file
- [ ] Standarize the input by file and tables
- [ ] Sync tables before the sync (initialization)
- [ ] Implement BEFORE triggers for SQL's table changes
- [ ] Generate logs for exceptions and errors
- [ ] Add a LIMIT option to the queries
- [ ] Add a FIELDS option to filter the select queries
- [ ] Make some tests to validate the code
- [ ] Set paths in a interactive shell
- [ ] Move from Sqlite to MSQL server
- [ ] Write a documentation
- [ ] Apply CQRS patterns
- [ ] Share as a library
- [ ] Create a GUI to manage DBF and SQL

&nbsp;

### 👐 Contribute

> Improvements?

- Don't hesitate to create a PR.

> Problems?

- Feel free to open a new issue!

&nbsp;

### ❤️  Gratitude

Thanks to the following projects developing this project is possible:

- [ethanfurman/dbf](https://github.com/ethanfurman/dbf): pure python dbf reader/writer
