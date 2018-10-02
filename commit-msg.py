#!/usr/bin/env python3
import sys
import platform
import subprocess

clear_screen_command = 'cls' if platform.system() == 'Windows' else 'clear'
subprocess.call(clear_screen_command)

# Checking for not staged files, if there's files pending, exit the script
git_command = ['git', '--no-pager', 'status', '-s']
execute = subprocess.run(git_command, stdout=subprocess.PIPE)
modified_files = execute.stdout \
                        .decode('utf-8') \
                        .split('\n')
modified_files = [ file[3:] for file in modified_files if file ]

print(modified_files)

if len(modified_files):
    print('Files have been found in the work area, please stash or commit them first and run this command again.\n')
    sys.exit(1)
