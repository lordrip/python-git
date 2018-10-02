#!/usr/bin/env python3
import sys
import re
import platform
import subprocess

clear_screen_command = 'cls' if platform.system() == 'Windows' else 'clear'
# subprocess.call(clear_screen_command)

# Receive the filename with the temporary git commit msg.
msg_file = sys.argv[1]

msg_filehandle = open(msg_file)
with msg_filehandle as f:
    commit_msg_parts = f.readlines()
    commit_msg = ''.join(commit_msg_parts)

if not commit_msg:
    sys.exit(1)
else:
    execute = subprocess.run(['git', 'branch'], stdout=subprocess.PIPE)
    branch_list = execute.stdout \
                         .decode('utf-8') \

    # Extract issue part from active branch for branch list
    #   * bugfix/APM-123456-test-branch-for-commit-msg
    #     ^^^^^^^^^^^^^^^^^
    #     master
    regex = re.compile(r'(?<=\*\s).+APM-[0-9]*', re.MULTILINE)
    issue_id = ''.join(re.findall(regex, branch_list))

    msg_filehandle = open(msg_file, 'w')
    with msg_filehandle as f:
        complete_commit_msg = '{} {}'.format(issue_id, commit_msg).strip()
        f.write(complete_commit_msg)

sys.exit(0)
