import random
import datetime

class MirageFilesystem:
    def __init__(self):
        self.common_files = [
            "backup.sql", "users.db", "config.php", "wp-config.php",
            "id_rsa", "wallet.dat", "environment.prod", "notes.txt"
        ]
        self.common_dirs = [
             "public_html", "www", "bin", "etc", "var", "tmp", "uploads", "backup"
        ]

    def generate_listing(self, path):
        """Generates a fake directory listing."""
        file_list = []

        # Always add specific enticing files mixed with random ones
        num_files = random.randint(3, 8)
        selected_files = random.sample(self.common_files, k=min(num_files, len(self.common_files)))

        # Add some directories
        num_dirs = random.randint(1, 4)
        selected_dirs = random.sample(self.common_dirs, k=min(num_dirs, len(self.common_dirs)))

        # Format for FTP LIST command (Unix ls -l style)
        # drwxr-xr-x    2 ftp      ftp          4096 Jun 15 02:23 www

        current_year = datetime.datetime.now().year

        lines = []

        for d in selected_dirs:
            date_str = self._random_date()
            line = f"drwxr-xr-x    2 ftp      ftp          4096 {date_str} {d}"
            lines.append(line)

        for f in selected_files:
            size = random.randint(1024, 1024 * 1024 * 5) # 1KB to 5MB
            date_str = self._random_date()
            line = f"-rw-r--r--    1 ftp      ftp     {size:>9} {date_str} {f}"
            lines.append(line)

        return "\r\n".join(lines) + "\r\n"

    def _random_date(self):
        """Returns a date string like 'Jun 15 02:23'"""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = random.choice(months)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{month} {day:02d} {hour:02d}:{minute:02d}"

    def get_file_content(self, filename):
        """Returns fake content for files."""
        return b"This is a honeypot file. The content is fake but the access is logged."
