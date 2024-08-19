from utils import (
    file_selection_dialog,
    read_csv,
    write_file,
    prompt_message,
    is_date,
    is_datetime,
)


def main():
    sql = PostgreSQL()
    sql.load_data()
    sql_path = sql.write_script()
    prompt_message(
        "SQL scrip generated",
        f"The SQL statement script is generated successfully and written to:\n\n{sql_path}",
    )


class PostgreSQL:
    def __init__(self):
        # Constants
        self.limit = 0
        self.tab = "    "
        self.null = "NULL"
        self.bit = "BIT"
        self.num = "NUMERIC"
        self.float = "FLOAT"
        self.datetime = "TIMESTAMP"
        self.date = "DATE"
        self.char = "CHARACTER"
        self.data_types = {
            self.bit: 1,
            self.num: 2,
            self.float: 3,
            self.datetime: 4,
            self.date: 5,
            self.char: 6,
        }
        self.field_suffix = "_field"
        self.preserved_keywords = [
            "ID",
            "POSITION",
            "LOCATION",
        ]
        # Optional constants
        self.p_key = ""
        # Source variables
        self.csv_path = ""
        self.db_name = ""
        self.table_name = ""
        self.data = []
        self.fields = {}
        # Script variables:
        # - Create schema statement
        self.schema_script = "CREATE SCHEMA IF NOT EXISTS [DB_NAME]\n"
        self.schema_script += f"{self.tab}AUTHORIZATION dbadmin;\n\n"
        # - Create table statement
        self.table_script = "DROP TABLE IF EXISTS [TABLE_NAME];\n"
        self.table_create = "CREATE TABLE IF NOT EXISTS [TABLE_NAME]\n(\n"
        # - Create insert statements
        self.insert_script = "DELETE FROM [TABLE_NAME];\n"

    def load_data(self):
        self._set_source_variables()
        self._set_schema_script()
        self._set_insert_script()
        self._set_table_script()

    def write_script(self):
        sql_script = self.schema_script + self.table_script + self.insert_script
        return write_file(sql_script, self.csv_path.rsplit(".", 1)[0] + ".sql")

    def _set_source_variables(self):
        self.csv_path = file_selection_dialog(
            [("CSV Files", "*.csv")], "Select a CSV file to convert to PostgreSQL"
        )
        self.table_name = self.csv_path.split("/")[-1].rsplit(".", 1)[0]
        self.db_name = self.table_name.rsplit(".", 1)[0]
        self.data = read_csv(self.csv_path, encoding="utf-8-sig")
        self.fields = self._set_source_fields()

    def _set_source_fields(self):
        fields = {}
        if self.limit > 0:
            limit = self.limit
        else:
            limit = len(self.data[0])
        for field in self.data[0][:limit]:
            if (
                field.upper() in self.data_types.keys()
                or field.upper() in self.preserved_keywords
            ):
                fields[f"{field}{self.field_suffix}"] = ""
            else:
                fields[field] = ""
        return fields

    def _set_schema_script(self):
        self.schema_script = self.schema_script.replace("[DB_NAME]", self.db_name)

    def _set_table_script(self):
        self.table_script = self.table_script.replace("[TABLE_NAME]", self.table_name)
        # Write create table statement script
        self.table_script += self.table_create.replace("[TABLE_NAME]", self.table_name)
        for field, data_type in self.fields.items():
            self.table_script += f"{self.tab}{field} {data_type},\n"
        table_key = self.table_name.split(".")[-1] + "_pkey"
        if self.p_key == "":
            self.p_key = list(self.fields.keys())[0]
        self.table_script += f"CONSTRAINT {table_key} PRIMARY KEY ({self.p_key}));\n\n"

    def _set_insert_script(self):
        self.insert_script = self.insert_script.replace("[TABLE_NAME]", self.table_name)
        fields_str = ", ".join(list(self.fields.keys()))
        # Get values and write insert statements for each row within the data
        for row in self.data[1:]:
            insert_str = f"INSERT INTO {self.table_name}(\n"
            insert_str += f"{self.tab}{fields_str})\n"
            insert_str += f"{self.tab}VALUES ("
            for idx, field in enumerate(self.fields.keys()):
                value = row[idx]
                insert_str += self._validate_data_type(value, field)
            else:
                insert_str = f"{insert_str[:-2]});\n"
            self.insert_script += insert_str

    def _validate_data_type(self, value: str, field: str):
        if value == "":
            value = self.null
        # NULL
        if value == self.null:
            self._compare_data_type(field, self.bit)
            return f"{value}, "
        # Numeric
        elif value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            self._compare_data_type(field, self.num)
            return f"{value}, "
        # Float
        elif value.replace(".", "", 1).isdigit() or (
            value.startswith("-") and value.replace(".", "", 1)[1:].isdigit()
        ):
            self._compare_data_type(field, self.float)
            return f"{value}, "
        # Datetime
        elif is_datetime(value):
            self._compare_data_type(field, self.datetime)
            return f"'{value}', "
        # Date
        elif is_date(value):
            self._compare_data_type(field, self.date)
            return f"'{value}', "
        # Character
        else:
            self._compare_data_type(field, self.char, len(value))
            return f"'{value}', "

    def _compare_data_type(self, field: str, val_type: str, val_len: int = 0):
        data_type_str = self.fields[field]
        try:
            data_type, data_len = self.fields[field].replace(")", "").split("(")
        except ValueError:
            data_type = self.fields[field]
            data_len = -1
        # Undefined
        if data_type_str == "":
            self._set_data_type(field, val_type, val_len)
        # Differences
        elif self.data_types[val_type] > self.data_types[data_type]:
            self._set_data_type(field, val_type, val_len)
        elif self.data_types[val_type] == self.data_types[data_type] and data_len != -1:
            if val_len > int(data_len):
                self._set_data_type(field, val_type, val_len)
        # NULL
        elif val_type == self.bit and data_type != self.bit and 0 < int(data_len) < 4:
            self.fields[field] = f"{data_type}(4)"

    def _set_data_type(self, field: str, val_type: str, val_len: int):
        if val_len > 0:
            self.fields[field] = f"{val_type}({val_len})"
        else:
            self.fields[field] = val_type


if __name__ == "__main__":
    main()
