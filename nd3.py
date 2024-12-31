import os
import sys


def create_nd3_file(input_tar_gz, output_nd3):
    """
    Create an ND3 file with a 128-byte metadata header and embedded tar.gz data.

    Args:
        input_tar_gz (str): Path to the input .tar.gz file.
        output_nd3 (str): Path to the output .ND3 file.
    """
    print("Creating ND3 file...")
    if not os.path.isfile(input_tar_gz):
        print(f"Error: File {input_tar_gz} does not exist.")
        return

    try:
        # Define ND3 header metadata
        description = "ND3 File: Container for Depth, NIR, Color, and Calibration data"
        # ND3 header: 128 bytes
        nd3_header = (
            b"ND3"  # Magic number
            + b" " * 3  # Padding
            + description.encode("utf-8")[:120]  # Truncate if longer than 120 bytes
        )

        # Pad the header to exactly 128 bytes
        nd3_header = nd3_header.ljust(128, b" ")

        if len(nd3_header) != 128:
            raise ValueError("ND3 header must be exactly 128 bytes.")

        print("ND3 header created successfully.")

        # Read tar.gz content
        if not os.path.isfile(input_tar_gz):
            print(f"Error: Input file not found: {input_tar_gz}")
            return

        with open(input_tar_gz, "rb") as tar_gz_file:
            tar_gz_data = tar_gz_file.read()

        print(f"Read {len(tar_gz_data)} bytes from input file.")

        # Create ND3 file
        with open(output_nd3, "wb") as nd3_file:
            nd3_file.write(nd3_header)  # Write ND3 header
            nd3_file.write(tar_gz_data)  # Append tar.gz data

        print(f"ND3 file created successfully: {output_nd3}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    print("ND3 conversion script started.")
    if len(sys.argv) != 3:
        print("Usage: python create_nd3.py <input_tar_gz> <output_nd3>")
        sys.exit(1)

    input_tar_gz = sys.argv[1]
    output_nd3 = sys.argv[2]

    print(f"Input file: {input_tar_gz}")
    print(f"Output file: {output_nd3}")
    create_nd3_file(input_tar_gz, output_nd3)
