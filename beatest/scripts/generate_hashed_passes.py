import csv

from tqdm import tqdm

from extensions import bcrypt


def get_hashed_passes_csv(input_path, output_path):
    """
    Generate the hashed passwords from a csv file
    and save it to an output file.


    :param input_path: path to a csv that contains two columns.
        first being the email and second being the plaintext password.

    :param output_path: path to a csv that will contain two columns.
        first being the email and second being the hashed password.
    :return:
    """
    with open(input_path) as input_file:
        csv_reader = csv.reader(input_file)
        num_rows = len(list(csv_reader))
        input_file.seek(0)

        with open(output_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for row in tqdm(csv_reader, total=num_rows):
                email, password = row
                password = bcrypt.generate_password_hash(password).decode()

                csv_writer.writerow([email, password])
