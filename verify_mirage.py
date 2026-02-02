import ftplib
import sys
import time

def verify_mirage():
    try:
        print("Connecting to MirageFTP...")
        ftp = ftplib.FTP()
        ftp.connect('127.0.0.1', 2121)
        print(f"Banner: {ftp.welcome}")

        print("Logging in...")
        ftp.login('admin', 'password123')

        print("Listing root directory...")
        files = []
        ftp.dir(files.append)
        for f in files:
            print(f"  {f}")

        if not files:
            print("FAILURE: No files listed.")
            sys.exit(1)

        print("Changing directory to /var/www...")
        ftp.cwd('/var/www')

        print("Listing /var/www...")
        files_subdir = []
        ftp.dir(files_subdir.append)
        for f in files_subdir:
            print(f"  {f}")

        if not files_subdir:
            print("FAILURE: No files listed in subdir.")
            sys.exit(1)

        # Try to download a file if one exists
        if files_subdir:
            # Parse filename from last part of the line
            target_file = files_subdir[0].split()[-1]
            print(f"Attempting to download {target_file}...")

            def handle_binary(data):
                print(f"Received {len(data)} bytes")

            ftp.retrbinary(f"RETR {target_file}", handle_binary)

        print("Quitting...")
        ftp.quit()
        print("SUCCESS: MirageFTP verification passed.")

    except Exception as e:
        print(f"FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Give the server a moment to start if run immediately after
    time.sleep(1)
    verify_mirage()
