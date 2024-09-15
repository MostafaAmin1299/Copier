import os
import shutil
import time
from datetime import datetime, timedelta

class Copier:
    def __init__(self):
        self.source_folders = []
        self.destination_folders = []
        self.base_destination_folder = None
        self.schedule_hours = None
        self.log_file = 'logs'

    def get_inputs(self):
        print('Starting the Copier ....')
        self.base_destination_folder = input('Enter the Base Destination Folder (Path): ')

        while True:
            source_folder = fr'{input("SOURCE_FOLDER (Path): ")}'
            self.source_folders.append(source_folder)

            destination_folder = input('DESTINATION_FOLDER (only name): ')
            self.destination_folders.append(destination_folder)

            more = input('Add more source folder? (y/n): ')
            if more.lower() != 'y':
                break

        # Schedule in hours
        while True:
            try:
                self.schedule_hours = int(input('Schedule (Hours): '))
                break
            except ValueError:
                print('Only numbers are allowed!!\n')
                

    # Function to open and write in the log file
    def log_copied_file(self, text):
        if not os.path.exists(self.log_file):
            os.makedirs(self.log_file)
        # Get the current date in YYYY-MM-DD format
        today_date = datetime.now().strftime('%Y-%m-%d')
        # Create the full path for the log file
        log_file = os.path.join(self.log_file, f'log_{today_date}.txt')
    
        with open(log_file, 'a') as log:
            log.write(f'{text}\n')

    # Function to copy files and directories modified in the last 'schedule_hours' hours
    def copy_files(self):
        # Calculate the time
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=self.schedule_hours)

        # Create a new folder with the current date to the today destination folders if it doesn't exist
        today_date = datetime.now().strftime('%Y-%m-%d')
        destination_day_folder = os.path.join(self.base_destination_folder, today_date)
        
        if not os.path.exists(destination_day_folder):
            os.makedirs(destination_day_folder)


        # Loop through the source folders
        for i, source_folder in enumerate(self.source_folders):
            #Check if the source folder is exist
            if not os.path.exists(source_folder):
                self.log_copied_file(f'No source folder with this name: {source_folder}\n')
                print(f'No source folder with this name: {source_folder}\n')
                continue

            # Create a subfolder for each source folder within the day folder
            subfolder_name = self.destination_folders[i]
            destination_subfolder = os.path.join(destination_day_folder, subfolder_name)

            self.log_copied_file(f'From {source_folder} To {destination_subfolder}\n')

            # Ensure the subfolder exists
            if not os.path.exists(destination_subfolder):
                os.makedirs(destination_subfolder)

            # Recursively copy files and directories
            for root, dirs, files in os.walk(source_folder):
                # Compute destination directory based on the root directory
                relative_path = os.path.relpath(root, source_folder)
                destination_root = os.path.join(destination_subfolder, relative_path)
            

                # Ensure the destination root exists
                if not os.path.exists(destination_root):
                    os.makedirs(destination_root)

                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    dest_file = os.path.join(destination_root, file_name)
                    try:
                    	# Get the last modified time of the file
                        file_mod_time = os.path.getmtime(source_file)
                        file_mod_datetime = datetime.fromtimestamp(file_mod_time)
                    except Exception as e:
                        print(f'Error copying {file_name}: {e}\n')
                        self.log_copied_file(f'Get the last modified time of the file {file_name}: {e}\n')
						
                    # Check if the file modification date is within the specified range
                    if start_time <= file_mod_datetime <= end_time:
                        try:
                            shutil.copy2(source_file, dest_file)  # Copy and overwrite if exists
                            self.log_copied_file(f'Copied: {file_name} to {destination_root}')
                        except Exception as e:
                            print(f'Error copying {file_name}: {e}\n')
                            self.log_copied_file(f'Error copying {file_name}: {e}')

            print(f'Copied: from {source_folder} to {destination_subfolder}\n')
            self.log_copied_file(f'\n{source_folder} files done\n---------')

    # Function to schedule the copying process
    def schedule_copy(self):
        while True:
            self.log_copied_file('============================================================================')
            self.log_copied_file(f'{datetime.now()} - Starting new cycle ...\n')

            print('============================================================================\n')
            print(f'{datetime.now()} - Starting new cycle ...\n')

            self.copy_files()
            print(f"Task completed. Next run will be in {self.schedule_hours} hours.\n")
            self.log_copied_file(f"Task completed. Next run will be in {self.schedule_hours} hours.\n")

            time.sleep(self.schedule_hours * 3600)  # Wait for the specified schedule (in hours)

# Main function to start the process
if __name__ == "__main__":
    copier = Copier()
    copier.get_inputs()
    copier.schedule_copy()
