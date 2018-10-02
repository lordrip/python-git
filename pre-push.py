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

if len(modified_files):
    print('Files have been found in the work area, please stash or commit them first and run this command again.\n')
    sys.exit(1)

for line in sys.stdin:
    git_params = line.replace('\n','') \
                     .split(' ')

    # This will be 40 zeroes when we're trying to push in a new branch
    empty_sha = '0' * 40
    local_sha = git_params[1]
    remote_sha = None if git_params[3] == empty_sha else git_params[3]

    git_command = ['git', '--no-pager', 'diff', '--name-only', local_sha, remote_sha]
    execute = subprocess.run(git_command, stdout=subprocess.PIPE)
    modified_files = execute.stdout \
                            .decode('utf-8') \
                            .split('\n')

    # Gather all the unique extensions for modified files in order to execute the configured commands
    modified_extensions = list(set(
            [ file.split('.')[-1] for file in modified_files if len(file.split('.')) > 1 ]
        ))

    for extension in modified_extensions:
        extension_config = 'pre-push.{}.command'.format(extension)
        git_command = ['git', 'config', extension_config]
        execute = subprocess.run(git_command, stdout=subprocess.PIPE)
        pre_push_pipeline = execute.stdout \
                                   .decode('utf-8') \
                                   .replace('\n', '') \
                                   .split(';')
        pre_push_pipeline = [pipeline_command.strip() for pipeline_command in pre_push_pipeline]

        for pipeline_command in pre_push_pipeline:
            if pipeline_command is not '':
                print(' [{ext}] "{cmd}" '.format(ext=extension, cmd=pipeline_command).center(80, '='))
                git_command = pipeline_command.split(' ')
                execute = subprocess.call(git_command)

                if execute:
                    print('\n' * 2)
                    print('Aborting push because [{cmd}] is returning a non-zero value'.format(cmd=pipeline_command))
                    sys.exit(execute)
        print('\n' * 2)

sys.exit(0)
