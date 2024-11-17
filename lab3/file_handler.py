class FileHandler:
    def __init__(self, rc5_cbc):
        self.rc5_cbc = rc5_cbc

    def encrypt_file(self, input_filename, output_filename, iv):
        with open(input_filename, 'rb') as infile:
            plaintext = infile.read()

        encrypted_data = self.rc5_cbc.encrypt(plaintext, iv)

        with open(output_filename, 'wb') as outfile:
            outfile.write(encrypted_data)

    def decrypt_file(self, input_filename, output_filename):
        with open(input_filename, 'rb') as infile:
            iv_ciphertext = infile.read()

        # Extract the IV and ciphertext
        iv = iv_ciphertext[:self.rc5_cbc.block_size]
        ciphertext = iv_ciphertext[self.rc5_cbc.block_size:]

        if len(ciphertext) % self.rc5_cbc.block_size != 0:
            raise ValueError("Ciphertext size is not a multiple of the block size")

        decrypted_data = self.rc5_cbc.decrypt(ciphertext, iv)

        with open(output_filename, 'wb') as outfile:
            outfile.write(decrypted_data)