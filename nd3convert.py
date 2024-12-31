import os
import sys

def validate_and_extract_tar_gz(nd3_file, output_dir):
    """
    Extracts the tar.gz content from an ND3 file, ensuring validity.

    Args:
        nd3_file (str): Path to the .ND3 file.
        output_dir (str): Directory to save the extracted .tar.gz file.
    """
    if not os.path.isfile(nd3_file):
        print(f"Error: File {nd3_file} does not exist.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(nd3_file, "rb") as f:
            # Skip the 128-byte ND3 header
            header = f.read(128)
            if not header.startswith(b"ND3"):
                print(f"Error: {nd3_file} does not appear to be a valid ND3 file.")
                return

            # Read the rest of the file (tar.gz data)
            tar_gz_data = f.read()

        # Verify tar.gz signature
        if not tar_gz_data[:2] == b'\x1f\x8b':  # gzip magic number
            print("Error: No valid tar.gz data found in the ND3 file.")
            return

        # Write the tar.gz data to an output file
        output_file_name = os.path.basename(nd3_file).replace(".ND3", ".tar.gz")
        output_path = os.path.join(output_dir, output_file_name)
        with open(output_path, "wb") as f:
            f.write(tar_gz_data)

        print(f"Successfully extracted {nd3_file} to {output_path}")

        # Verify the tar.gz file by attempting to extract it
        print("Validating tar.gz file...")
        os.system(f"tar -tzf {output_path} > /dev/null 2>&1")
        print("Validation complete: tar.gz file is valid.")

    except Exception as e:
        print(f"Error: Failed to extract {nd3_file}. Details: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python nd3_to_targz.py <input_nd3_file> <output_dir>")
        sys.exit(1)

    nd3_file = sys.argv[1]
    output_dir = sys.argv[2]

    validate_and_extract_tar_gz(nd3_file, output_dir)
