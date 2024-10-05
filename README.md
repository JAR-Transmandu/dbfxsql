# dbfxsql


### ✨ Overview

A tool that enables bi-directional data synchronization between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) databases. It facilitates seamless data migration from DBF to SQL and vice versa.

&nbsp;

### 🔌 Installation

1. Clone the repository:

```bash
git clone https://github.com/j4breu/dbfxsql.git
```

2. Install Poetry (if not alredy installed)

```bash
pip install poetry
```

3. Set up the environment:

```bash
cd dbfxsql
poetry shell
poetry install
```

4. Fullfill the environment variables:

```bash
cp .env.example .env
vim .env
```

5. Run the tool:

```bash
python run.py # python -m dbfxsql
```

<details>
  <summary><strong>As a library:</strong></summary>
  <br>
  <ol>

1. Clone the repository:

```bash
git clone https://github.com/j4breu/dbfxsql.git
```

2. Install the project as a Python library:

```bash
cd dbfxsql
pip install .
````

3. Run the tool:

```bash
dbfxsql
```
  </ol>
</details>
&nbsp;

### 💻 Usage

**Detailed Usage Instructions Coming Soon!**

Comprehensive documentation with usage instructions and code examples will be available in a separate file shortly. Stay tuned!

**Early Code Example:**

This early version of the code demonstrates a basic interaction with the tool.

[Link to Asciinema code example](https://asciinema.org/a/675516)

&nbsp;

### 📝 Roadmap

**Required:**
- [x] CRUD operations for both DBF and SQL databases.
- [x] Bi-directional data transfer between DBF and SQL.
- [x] Command-Line Interface (CLI) for managing DBF and SQL tasks.
- [x] Detecting changes in folders.
- [x] Compare records to sync specific fields
- [x] Set up a cron job to sync data

<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[x] Uploading the project to GitHub.</li>
      <li>[x] Handling dynamic fields between databases.</li>
      <li>[x] Specifying database location in queries.</li>
      <li>[x] Handling dynamic input parameters.</li>
      <li>[x] Assigning proper data types to input values.</li>
      <li>[x] Allowing adding fields in DBF (incremental ID support).</li>
      <li>[x] Retrieving database folder paths from a `.env` file.</li>
      <li>[x] Creating a project explainer video.</li>
      <li>[x] Configuring database/table/field delimiters via a config file.</li>
      <li>[x] Don't update a DBF record if it hasn't changed.</li>
      <li>[x] Get the records of all relationships in the config file.</li>
      <li>[x] Force SQL -> DBF "synchronization" (read all tables).</li>
      <li>[ ] Optimize Insert/Delete queries using Update queries.</li>
      <li>[ ] Suppress id in fields if their value it's the same in condition.</li>
      <li>[ ] Use a decorator for the listening command.</li>
      <li>[ ] Add listen and compare commands.</li>
      <li>[ ] Automatic SQL database creation during SQL table creation.</li>
      <li>[ ] Replace dictionaries with classes during synchronization.</li>
      <li>[ ] Support for other database systems beyond SQLite. (MSQL Server).</li>
      <li>[ ] Implement BEFORE triggers for SQL table changes.</li>
      <li>[ ] Allow setting folder paths via CLI commands.</li>
      <li>[ ] Upload a configuration file via CLI commands.</li>
      <li>[ ] Validate the existence of fields in the DBF.</li>
      <li>[ ] Separate incremental logic from the "add" feature.</li>
      <li>[ ] Add LIMIT and FIELDS options for filtering queries.</li>
      <li>[ ] Perform table migration before initial data synchronization.</li>
      <li>[ ] Generate logs for exceptions and errors.</li>
      <li>[ ] Standardize input by file and tables.</li>
      <li>[ ] Validate KeyErrors for invalid fields.</li>
      <li>[ ] Validate type lengths and names for consistency between DBF and SQL.</li>
      <li>[ ] Support for relationships between two or more tables in the config file.</li>
      <li>[ ] Unit tests for code validation.</li>
      <li>[ ] Comprehensive project documentation.</li>
      <li>[ ] Implementation of CQRS (Command Query Responsibility Segregation) patterns.</li>
      <li>[ ] Sharing as a Python library.</li>
      <li>[ ] Development of a GUI for managing DBF and SQL.</li>
  </ul>
</details>

&nbsp;

### 👐 Contribute

> Improvements?

- Don't hesitate to create a PR.

> Problems?

- Feel free to open a new issue!

&nbsp;

### ❤️  Gratitude

Special thanks to the following project for making this tool possible:

- [dbf Python library](https://github.com/ethanfurman/dbf/tree/master/dbf): Pure Python DBF reader/writer by [Ethan Furman](https://github.com/ethanfurman)
