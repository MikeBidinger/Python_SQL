from os import sep
from utils import (
    file_selection_dialog,
    read_sql,
    write_csv,
    prompt_message,
    format_string,
)


def main():
    csv = CSV()
    csv.load_data()
    csv_paths = csv.write_csv()
    paths = "\n".join(csv_paths)
    prompt_message(
        "CSV file generated",
        f"The CSV file is generated successfully and written to:\n\n{paths}",
    )


class CSV:
    def __init__(self):
        # Constants
        self.limit = 0
        self.tab = "    "
        # Source variables
        self.sql_path = ""
        self.data = []
        self.db_name = ""
        self.tables = {}
        self.values = {}
        # Script constants:
        self.schema_script = "CREATE SCHEMA IF NOT EXISTS "
        self.table_script = "CREATE TABLE IF NOT EXISTS "
        self.insert_script = "INSERT INTO "
        self.values_script = "VALUES ("

    def load_data(self):
        self._set_source_data()
        self._set_tables()
        self._set_values()

    def write_csv(self):
        files = []
        directory = self.sql_path.rsplit(sep, 1)[0]
        for table in self.tables:
            matrix = [self.tables[table]]
            for record in self.values[table]:
                row = []
                for field in matrix[0]:
                    row.append(record.get(field, ""))
                matrix.append(row)
            file = write_csv(matrix, f"{directory}{sep}{self.db_name}.{table}.csv")
            files.append(file)
        return files

    def _set_source_data(self):
        self.sql_path = file_selection_dialog(
            [("SQL Files", "*.sql")], "Select a SQL file to convert to CSV"
        )
        self.data = read_sql(self.sql_path)

    def _set_tables(self):
        # Set DB name
        for row_db, row in enumerate(self.data):
            if row.startswith(self.schema_script):
                self.db_name = row.replace(self.schema_script, "").split(";", 1)[0]
                break
        # Set tables
        for row_table, row in enumerate(self.data[row_db + 1 :]):
            if row.startswith(self.table_script):
                # Set table name
                table = ""
                table = (
                    row.replace(f"{self.table_script}{self.db_name}.", "")
                    .split("(", 1)[0]
                    .strip()
                )
                # Set table fields
                fields = []
                for row in self.data[row_db + row_table + 2 :]:
                    if row.endswith(";"):
                        break
                    elif (
                        row == ""
                        or row.startswith("--")
                        or row.startswith("(")
                        or row.startswith("\n")
                    ):
                        continue
                    else:
                        fields.append(format_string(row.strip().split(" ", 1)[0]))
                # Set table
                self.tables[table] = fields

    def _set_values(self):
        # Set table values
        for row_insert, row in enumerate(self.data):
            if row.startswith(self.insert_script):
                record = {}
                # Set table name
                table = row.split("(", 1)[0].replace(
                    f"{self.insert_script}{self.db_name}.", ""
                )
                if table not in self.values:
                    self.values[table] = []
                # Set table values for according fields
                fields = []
                values = []
                for row in self.data[row_insert + 1 :]:
                    if row.endswith(")"):
                        fields = row.strip()[:-1].split(", ")
                    elif row.strip().startswith(self.values_script) and row.endswith(
                        ");"
                    ):
                        values = (
                            row.strip()[:-2].replace(self.values_script, "").split(", ")
                        )
                        for field, value in zip(fields, values):
                            record[format_string(field)] = format_string(value)
                        self.values[table].append(record)
                        break


if __name__ == "__main__":
    main()
