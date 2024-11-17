class FileHandler:
    @staticmethod
    def save_to_file(data, file_name):
        with open(file_name, 'w') as file:
            file.write(data)

    @staticmethod
    def read_from_file(file_name):
        with open(file_name, 'r') as file:
            return file.read()
