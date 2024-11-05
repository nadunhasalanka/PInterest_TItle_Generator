import os

import g4f
import gspread
from google.oauth2.service_account import Credentials
from modules.base import Pinterest


class Writer(Pinterest):
    def __init__(self, project_folder):
        super().__init__(project_folder)


    def open_data(self, mode='video', google_sheet = True, table_id = None):
        if google_sheet:
            # if the value of the google_sheet argument is true , we will read data from table via API
            # Obtain Google Sheets credentials
            creds = self._get_google_creds()

            # authorize the connection using gspread
            client = gspread.authorize(creds)

            #Open the Google Sheets table using its key
            table = client.open_by_key(table_id)

            #Choose the appropriate worksheet based on the mode (image or video)
            if mode == 'image':
                worksheet = table.get_worksheet(2)
            elif mode == 'video':
                worksheet = table.get_worksheet(1)
            else:
                #Raise an error for an invalid mode
                raise ValueError(f"invalid mode: {mode}. Please choose between 'image' and 'video'")

            # Retrieve all values from the choosen worksheet
            all_values = worksheet.get_all_values()

            # Parse the rows and obtain the data based on the specified mode
            data = self._parse_rows(all_values, mode)

        else:
            #otherwise , we will  read data frpm a csv file
            if mode == 'image':
                filename = self.IMAGE_PROMPTS_FILE
            elif mode == 'video':
                filename = self.VIDEO_PROMPTS_FILE
            else:
                raise ValueError(f"Invalid mode: {mode}. Please set the mod to 'image' or or 'video'.")

            # Open the CSV file with the specified filename and retrieve data
            data = self.open_csv(filename)

        return data

    @staticmethod
    def _parse_rows(rows, mode):
        data = []
        for index, row in enumerate(rows):
            # Skip the first iteration
            if index == 0:
                continue

            row_dict = {
                'keyword': row[0],
                'title_prompt': row[1],
                'description_prompt': row[2],
            }
            #Add 'tips_prompt' to the library if the mode is 'image'
            if mode == 'image':
                row_dict['tips_prompt'] = row[3]
            data.append(row_dict)
        return data


    def _get_google_creds(self):
        #specify the path to the JSON key file
        json_key_path = os.path.join(self.data_path, 'keyfile.json')

        #define the required OAuth2.0 scopes for Google Sheets API
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        #create the credential object based on the JSON key File
        credentials = Credentials.from_service_account_file(json_key_path, scopes=scopes)

        return credentials

    def write_single_prompt(self, prompt):
        # Create a ChatCompletion instance from g4f module using the OpenAI GPT model
        # to generate content based on the provided prompt
        # the promt is set as a user message in the 'message' parameter.
        response = g4f.ChatCompletion.create(
            model = g4f.models.gpt_35_turbo,
            messages = [{'role' : 'user', 'content' : prompt}]
        )

        # return the generated response
        return response


    def write(self, row, mode='video'):
        # Check if the mode is valid
        if mode not in ['image', 'video']:
            raise ValueError(f"invalid mode: {mode}. Please choose between 'image' or 'video'.")

        # Initialize results dictionary with default values
        results = {
            'mode': mode,
            'file_path': '',
            'board_name': '',
            'pin_link': '',
        }

        try:
            #Extract keywords from the row or set it to an empty string if not present
            results['keyword'] = row.get('keyword', '')

            # Write title and log the preocess
            self._log_message('Writing title...')
            # Extract title prompt
            title_prompt = row.get('title_prompt', '')
            title = self.write_single_prompt(title_prompt)
            results['title'] = title.strip('"') if title else ''

            # Write desciption and log the process
            self._log_message('Writing description...')
            # Replace 'SELECTED TITLE; in the description with the generated title
            description_prompt = row.get('description_prompt', '') \
                .replace('SELECTED TITLE', title if title else row.get('keyword', ''))
            description = self.write_single_prompt(description_prompt)
            results['description'] = description.strip('"') if description else ''


            if mode == 'image':
                # Write tips for image and log the process
                self._log_message('Writing Tips...')
                # Replace 'SELECTED TITLE' in the tips prompt with the generated tittle
                tips_prompt = row.get('tips_prompt', '') \
                    .replace('SELECTED TITLE', title if title else row.get('keyword', ''))
                tips = self.write_single_prompt(tips_prompt)
                results['tips'] = tips.strip('"') if tips else ''
        except Exception as e:
            # Log an error id an exception occurs during writing
            self._log_error(f"Error while writing: ", e)

        # Determine the filename based on the mode and write the results to the corresponding CSV file
        filename = self.GENERATOR_DATA_FILE if mode == 'image' else self.UPLOADING_DATA_FILE
        self.write_csv(results, filename)




