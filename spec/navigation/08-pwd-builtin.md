# The pwd builtin

## Instructions

### Your Task

In this stage, you'll implement the `pwd` builtin.

### The `pwd` Builtin

The [`pwd`](https://en.wikipedia.org/wiki/Pwd) (print working directory) builtin prints the full, absolute path of the current working directory to stdout.

When your shell starts, its current working directory is typically the directory from which it was executed. Your `pwd` implementation needs to retrieve this information from the operating system and print it.

For example:

```shell
$ pwd
/home/user/projects
$ pwd
/usr/local/bin
```

### Tests

The tester will execute your program like this:

```shell
./your_program.sh
```

It will then send a `pwd` command to your shell:

```shell
$ pwd
/path/to/current/directory
$
```

The tester will verify that the `pwd` command correctly displays the current working directory.

### Notes

- The `pwd` command must print the full absolute path of the current working directory.
