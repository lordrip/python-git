# python3 - git hooks

## Installation
> 1) Clone the repo
> 2) Copy the desired hook file to `.git/hooks` folder of your repo
> 3) Make the script executable with `chmod +x [git-hook-file-name]`
> 4) Configure as desire

## Prepush git hook `[pre-push.py]`
> This hook is for execute a command when specific file extension are being modified.
> f.i. when we're working on `.TS` files and we want to execute the linting after pushing
> the branch.

#### Config:
>`git config pre-push.[ extension ].command="commands; commands;"`
>
> examples:
>
> `git config pre-push.ts.command="ng build;"`
>
> `git config pre-push.ts.command="ng lint; ng test;"`
