import re


class Converter:

    def convert(self, file, ext):
        """
        Enter a file you want to convert to either JSON or CSV. If you want to
        convert a JSON file to CSV enter CSV as the extension (ext)\n
        Example:
        file="MOCK_DATA.json", ext="CSV"
        """
        converter = self._get_converter(ext)
        with open(file, "r") as file:
            return converter(file)

    def _get_converter(self, ext):
        if ext == 'CSV':
            return self._convert_to_CSV
        elif ext == 'JSON':
            return self._convert_to_JSON
        else:
            raise ValueError(format)

    def _convert_to_CSV(self, file):
        user_file = JSON2CSV(file)
        return user_file.format_file()

    def _convert_to_JSON(self, file):
        user_file = CSV2JSON(file)
        return user_file.open_file()


class CSV2JSON:

    csv_dict = {}
    csv_data = []

    def __init__(self, file):
        self.file = file

    def json_start(self):
        return """[{"""

    def json_middle(self):
        return """},\n{"""

    def json_end(self):
        return """}]"""

    def open_file(self):

        self.csv = self.file.read()
        self.csv_rows = self.csv.split('\n')
        # list comp to remove empty items from the list
        self.csv_rows = [space for space in self.csv_rows if space not in ('')]
        
        self.csv_headers = self.csv_rows[0].split(',')
        
        for header in self.csv_headers:
            self.csv_dict[header] = []
        
        for row in self.csv_rows[1:]:
            self.csv_data.append(row.split(','))
        self._count_rows_and_headers()
        self._csv_dict()
        self._dict_json()
       
    def _count_rows_and_headers(self):
        # Calculate the number items, minus the headers
        self.number_of_items = len(self.csv.split(',')) - len(self.csv_rows) + 1
        self.number_of_rows = len(self.csv_rows[1:])
     
    def _csv_dict(self):
        # IF INDEX1 IS MORE THAN THE NUMBER OF ROWS THEN INDEX2 GOES UP BY ONE
        index1 = 0
        index2 = 0
        # Moves CSV into dict
        while True:
            if index1 == self.number_of_rows:
                index1 = 0
                index2 += 1
                if index2 == len(self.csv_headers):
                    break
            self.csv_dict[self.csv_headers[index2]].append(self.csv_data[index1][index2])
            index1 += 1
    
    def _dict_json(self):
        with open("test.json", 'w') as f:
            # formats to JSON
            index1 = 0
            index2 = 0
            while True:
                if index2 == 0:
                    f.write(self.json_start())
                if index2 == len(self.csv_headers):
                    index1 += 1
                    index2 = 0
                    if index1 == self.number_of_rows:
                        f.write(self.json_end())
                        break
                    else:
                        f.write(self.json_middle())
                if index2 == len(self.csv_headers) - 1:
                    last_line = f'"{self.csv_headers[index2]}":"{self.csv_dict[self.csv_headers[index2]][index1]}"'
                    f.write(last_line)
                else:
                    line = f'\t "{self.csv_headers[index2]}":"{self.csv_dict[self.csv_headers[index2]][index1]}",'.strip()           
                    f.write(line)
                index2 += 1


class JSON2CSV:

    json_data = []
    json_headers = []
    
    def __init__(self, file):
        self.file = file

    def format_file(self):
        # self.json = re.sub(r'[\[\]{}}\n:]', "", self.file.read())
        self.json = self.file.readlines()
        for line in self.json:
            line = re.sub(r'[\[\]{}}\n:]', "", line).split('"')
            for item in line:
                if item != "," and item != "":
                    if "," in item:
                        if "," == item[-1]:
                            self.json_data.append(item.replace(",", ""))
                        else:
                            self.json_data.append(f'"{item}"')
                    else:
                        self.json_data.append(item)
        for headers in range(0, len(self.json_data), 2):
            if self.json_data[headers] not in self.json_headers:
                self.json_headers.append(self.json_data[headers])
            else:
                break
        for item in self.json_data:
            if item in self.json_headers:
                self.json_data.remove(item)
        self.number_of_rows = len(self.json)
        self.row_length = len(self.json_headers)
        return self._to_csv()
        
    def _to_csv(self):
        with open("test1.csv", "w") as f:
            # row_number = row number
            row_number = 0
            # numbers of items in the entire JSON file
            items = 0
            item_counter = 0
            f.write(",".join(self.json_headers))
            f.write("\n")
        
            while row_number != self.number_of_rows:
                f.write(f"{self.json_data[items]},")
                items += 1
                item_counter += 1
                if item_counter == self.row_length - 1:
                    f.write(f"{self.json_data[items]}")
                    f.write("\n")
                    items += 1
                    row_number += 1
                    item_counter = 0
