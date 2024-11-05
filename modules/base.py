import csv
import os
import logging

class Pinterest:
    UPLOADING_DATA_FILE = "uploading_data.csv"
    GENERATOR_DATA_FILE = "generator_data.csv"
    IMAGE_PROMPTS_FILE = "image_prompts.csv"
    VIDEO_PROMPTS_FILE = "video_prompts.csv"

    def __init__(self, project_folder):
        self.project_path = os.path.join(os.path.abspath('projects'), project_folder)
        self.prompts_path = os.path.join(self.project_path, 'prompts')
        self.data_path = os.path.abspath('data')

        # Ensure that the folders exist
        os.makedirs(self.project_path, exist_ok=True)
        os.makedirs(self.prompts_path, exist_ok=True)
        os.makedirs(self.data_path, exist_ok=True)

    def open_csv(self, filename):
        data_file_path = self._get_data_file_path(filename)
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f'File {filename} does not exist: {data_file_path}')

        delimiter = self._check_csv_delimiter(data_file_path)
        result = []
        with open(data_file_path, 'r', encoding='utf-8', newline='') as data:
            heading = next(data)  # skip header
            reader = csv.reader(data, delimiter=delimiter)

            for row in reader:
                if filename == self.VIDEO_PROMPTS_FILE:
                    row_dict = {'keyword': row[0], 'title_prompt': row[1], 'description_prompt': row[2]}
                    result.append(row_dict)
                elif filename == self.IMAGE_PROMPTS_FILE:
                    row_dict = {'keyword': row[0], 'title_prompt': row[1], 'description_prompt': row[2], 'tips_prompt': row[3]}
                    result.append(row_dict)
        return result

    def write_csv(self, data, filename):
        data_file_path = self._get_data_file_path(filename)
        file_exists = os.path.exists(data_file_path)
        file_empty = file_exists and os.stat(data_file_path).st_size == 0

        uploading_data_header = ['mode', 'keyword', 'title', 'description', 'file_path', 'board_name', 'pin_link']
        order = ['mode', 'keyword', 'title', 'description', 'file_path', 'board_name', 'pin_link']
        if filename == self.GENERATOR_DATA_FILE:
            order.insert(4, 'tips')

        if not file_exists or file_empty:
            self._write_header(data_file_path, uploading_data_header)

        try:
            with open(data_file_path, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=order, delimiter=';')
                writer.writerow(data)
            self._log_message(f"Data has been successfully written to {filename}.\n")
        except KeyError as e:
            self._log_error("Missing data fields.", e)

    @staticmethod
    def _write_header(file_path, header):
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(header)

    @staticmethod
    def _check_csv_delimiter(file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            if ',' in first_line:
                return ','
            elif ';' in first_line:
                return ';'
            else:
                return ','

    def _get_data_file_path(self, filename):
        if filename in [self.VIDEO_PROMPTS_FILE, self.IMAGE_PROMPTS_FILE]:
            return os.path.join(self.prompts_path, filename)
        else:
            return os.path.join(self.project_path, filename)

    @staticmethod
    def _log_message(message):
        print(message)  # Placeholder for logging

    @staticmethod
    def _log_error(message, error):
        red_color = "\033[91m"
        reset_color = "\033[0m"
        print(f'{red_color}{message}{reset_color}\n{error}\n')
