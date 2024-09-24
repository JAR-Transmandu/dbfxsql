# dbfxsql


### ✨ Overview

A tool that enables bi-directional data synchronization between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) databases. It facilitates seamless data migration from DBF to SQL and vice versa.

&nbsp;

### 🔌 Installation

1. Clone he repository:

```bash
git clone https://github.com/j4breu/dbfxsql.git
```

2. Change to the project directory:

```bash
cd dbfxsql
```

3. Install Poetry (if not alredy installed)

```bash
pip install poetry
```

4. Install project dependencies:

```bash
poetry install
```

5. Run the application:

```bash
poetry run python run.py
```

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
- [ ] Compare records to sync specific fields
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
      <li>[ ] Automatic SQL database creation during SQL table creation.</li>
      <li>[ ] Replace dictionaries with classes during synchronization.</li>
      <li>[ ] Force SQL -> DBF "synchronization" (read all tables).</li>
      <li>[ ] Support for other database systems beyond SQLite. (MSQL Server).</li>
      <li>[ ] Implement BEFORE triggers for SQL table changes.</li>
      <li>[ ] Allow setting folder paths via CLI commands.</li>
      <li>[ ] Upload a configuration file via CLI commands.</li>
      <li>[ ] Validate the existence of fields in the DBF.</li>
      <li>[ ] Separate incremental logic from the "add" feature.</li>
      <li>[ ] Add LIMIT and FIELDS options for filtering queries.</li>
      <li>[ ] Perform table synchronization before initial data migration.</li>
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

- [ethanfurman/dbf](https://github.com/ethanfurman/dbf): pure python dbf reader/writer
