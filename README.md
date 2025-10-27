<div align=right>Table of Contents↗️</div>

<h1 align=center><code>just</code></h1>

<div align=center>
  <a href=https://crates.io/crates/just>
    <img src=https://img.shields.io/crates/v/just.svg alt="crates.io version">
  </a>
  <a href=https://github.com/casey/just/actions>
    <img src=https://github.com/casey/just/actions/workflows/ci.yaml/badge.svg alt="build status">
  </a>
  <a href=https://github.com/casey/just/releases>
    <img src=https://img.shields.io/github/downloads/casey/just/total.svg alt=downloads>
  </a>
  <a href=https://discord.gg/ezYScXR>
    <img src=https://img.shields.io/discord/695580069837406228?logo=discord alt="chat on discord">
  </a>
  <a href=mailto:casey@rodarmor.com?subject=Thanks%20for%20Just!>
    <img src=https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg alt="say thanks">
  </a>
</div>
<br>

`just` is a handy way to save and run project-specific commands.

This readme is also available as a [book](https://just.systems/man/en/).

(中文文档在 [这里](https://github.com/casey/just/blob/master/README.中文.md),
快看过来!)

Commands, called recipes, are stored in a file called `justfile` with syntax
inspired by `make`:

![screenshot](https://raw.githubusercontent.com/casey/just/master/screenshot.png)

You can then run them with `just RECIPE`:



`just` has a ton of useful features, and many improvements over `make`:

- `just` is a command runner, not a build system, so it avoids much of
  [`make`'s complexity and idiosyncrasies](#what-are-the-idiosyncrasies-of-make-that-just-avoids).
  No need for `.PHONY` recipes!

- Linux, MacOS, and Windows are supported with no additional dependencies.
  (Although if your system doesn't have an `sh`, you'll need to
  [choose a different shell](#shell).)

- Errors are specific and informative, and syntax errors are reported along
  with their source context.

- Recipes can accept [command line arguments](#recipe-parameters).

- Wherever possible, errors are resolved statically. Unknown recipes and
  circular dependencies are reported before anything runs.

- `just` [loads `.env` files](#dotenv-settings), making it easy to populate
  environment variables.

- Recipes can be [listed from the command line](#listing-available-recipes).

- Command line completion scripts are
  [available for most popular shells](#shell-completion-scripts).

- Recipes can be written in
  [arbitrary languages](#writing-recipes-in-other-languages), like Python or NodeJS.

- `just` can be invoked from any subdirectory, not just the directory that
  contains the `justfile`.

- And [much more](https://just.systems/man/en/)!

If you need help with `just` please feel free to open an issue or ping me on
[Discord](https://discord.gg/ezYScXR). Feature requests and bug reports are
always welcome!

Installation
------------

### Prerequisites

`just` should run on any system with a reasonable `sh`, including Linux, MacOS,
and the BSDs.

On Windows, `just` works with the `sh` provided by
[Git for Windows](https://git-scm.com),
[GitHub Desktop](https://desktop.github.com), or
[Cygwin](http://www.cygwin.com).

If you'd rather not install `sh`, you can use the `shell` setting to use the
shell of your choice.

Like PowerShell:



…or `cmd.exe`:



You can also set the shell using command-line arguments. For example, to use
PowerShell, launch `just` with `--shell powershell.exe --shell-arg -c`.

(PowerShell is installed by default on Windows 7 SP1 and Windows Server 2008 R2
S1 and later, and `cmd.exe` is quite fiddly, so PowerShell is recommended for
most Windows users.)

### Packages

<table>
  <thead>
    <tr>
      <th>Operating System</th>
      <th>Package Manager</th>
      <th>Package</th>
      <th>Command</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href=https://alpinelinux.org>Alpine Linux</a></td>
      <td><a href=https://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management>apk-tools</a></td>
      <td><a href=https://pkgs.alpinelinux.org/package/edge/community/x86_64/just>just</a></td>
      <td><code>apk add just</code></td>
    </tr>
    <tr>
      <td><a href=https://www.archlinux.org>Arch Linux</a></td>
      <td><a href=https://wiki.archlinux.org/title/Pacman>pacman</a></td>
      <td><a href=https://archlinux.org/packages/extra/x86_64/just/>just</a></td>
      <td><code>pacman -S just</code></td>
    </tr>
    <tr>
      <td><a href=https://debian.org>Debian</a> and <a href=https://ubuntu.com>Ubuntu</a> derivatives</td>
      <td><a href=https://mpr.makedeb.org>MPR</a></td>
      <td><a href=https://mpr.makedeb.org/packages/just>just</a></td>
      <td>
        <code>git clone https://mpr.makedeb.org/just</code><br>
        <code>cd just</code><br>
        <code>makedeb -si</code>
      </td>
    </tr>
    <tr>
      <td><a href=https://debian.org>Debian</a> and <a href=https://ubuntu.com>Ubuntu</a> derivatives</td>
      <td><a href=https://docs.makedeb.org/prebuilt-mpr>Prebuilt-MPR</a></td>
      <td><a href=https://mpr.makedeb.org/packages/just>just</a></td>
      <td>
        <sup><b>You must have the <a href=https://docs.makedeb.org/prebuilt-mpr/getting-started/#setting-up-the-repository>Prebuilt-MPR set up</a> on your system in order to run this command.</b></sup><br>
        <code>sudo apt install just</code>
      </td>
    </tr>
    <tr>
      <td><a href=https://getfedora.org>Fedora Linux</a></td>
      <td><a href=https://dnf.readthedocs.io/en/latest/>DNF</a></td>
      <td><a href=https://src.fedoraproject.org/rpms/rust-just>just</a></td>
      <td><code>dnf install just</code></td>
    </tr>
    <tr>
      <td><a href=https://www.freebsd.org>FreeBSD</a></td>
      <td><a href=https://www.freebsd.org/doc/handbook/pkgng-intro.html>pkg</a></td>
      <td><a href=https://www.freshports.org/deskutils/just/>just</a></td>
      <td><code>pkg install just</code></td>
    </tr>
    <tr>
      <td><a href=https://www.gentoo.org>Gentoo Linux</a></td>
      <td><a href=https://wiki.gentoo.org/wiki/Portage>Portage</a></td>
      <td><a href=https://github.com/gentoo-mirror/guru/tree/master/dev-build/just>guru/dev-build/just</a></td>
      <td>
        <code>eselect repository enable guru</code><br>
        <code>emerge --sync guru</code><br>
        <code>emerge dev-build/just</code>
      </td>
    </tr>
    <tr>
      <td><a href=https://en.wikipedia.org/wiki/MacOS>macOS</a></td>
      <td><a href=https://www.macports.org>MacPorts</a></td>
      <td><a href=https://ports.macports.org/port/just/summary>just</a></td>
      <td><code>port install just</code></td>
    </tr>
    <tr>
      <td><a href=https://en.wikipedia.org/wiki/Microsoft_Windows>Microsoft Windows</a></td>
      <td><a href=https://chocolatey.org>Chocolatey</a></td>
      <td><a href=https://github.com/michidk/just-choco>just</a></td>
      <td><code>choco install just</code></td>
    </tr>
    <tr>
      <td><a href=https://en.wikipedia.org/wiki/Microsoft_Windows>Microsoft Windows</a></td>
      <td><a href=https://scoop.sh>Scoop</a></td>
      <td><a href=https://github.com/ScoopInstaller/Main/blob/master/bucket/just.json>just</a></td>
      <td><code>scoop install just</code></td>
    </tr>
    <tr>
      <td><a href=https://en.wikipedia.org/wiki/Microsoft_Windows>Microsoft Windows</a></td>
      <td><a href=https://learn.microsoft.com/en-us/windows/package-manager/>Windows Package Manager</a></td>
      <td><a href=https://github.com/microsoft/winget-pkgs/tree/master/manifests/c/Casey/Just>Casey/Just</a></td>
      <td><code>winget install --id Casey.Just --exact</code></td>
    </tr>
    <tr>
      <td><a href=https://nixos.org/nixos/>NixOS</a></td>
      <td><a href=https://nixos.org/nix/>Nix</a></td>
      <td><a href=https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/tools/just/default.nix>just</a></td>
      <td><code>nix-env -iA nixos.just</code></td>
    </tr>
    <tr>
      <td><a href=https://opensuse.org>openSUSE</a></td>
      <td><a href=https://en.opensuse.org/Portal:Zypper>Zypper</a></td>
      <td><a href=https://build.opensuse.org/package/show/Base:System/just>just</a></td>
      <td><code>zypper in just</code></td>
    </tr>
    <tr>
      <td><a href=https://getsol.us>Solus</a></td>
      <td><a href=https://getsol.us/articles/package-management/basics/en>eopkg</a></td>
      <td><a href=https://dev.getsol.us/source/just/>just</a></td>
      <td><code>eopkg install just</code></td>
    </tr>
    <tr>
      <td><a href=https://github.com/casey/just/releases>Various</a></td>
      <td><a href=https://asdf-vm.com>asdf</a></td>
      <td><a href=https://github.com/olofvndrhr/asdf-just>just</a></td>
      <td>
        <code>asdf plugin add just</code><br>
        <code>asdf install just &lt;version&gt;</code>
      </td>
    </tr>
    <tr>
      <td><a href=https://forge.rust-lang.org/release/platform-support.html>Various</a></td>
      <td><a href=https://www.rust-lang.org>Cargo</a></td>
      <td><a href=https://crates.io/crates/just>just</a></td>
      <td><code>cargo install just</code></td>
    </tr>
    <tr>
      <td><a href=https://docs.conda.io/en/latest/miniconda.html#system-requirements>Various</a></td>
      <td><a href=https://docs.conda.io/projects/conda/en/latest/index.html>Conda</a></td>
      <td><a href=https://anaconda.org/conda-forge/just>just</a></td>
      <td><code>conda install -c conda-forge just</code></td>
    </tr>
    <tr>
      <td><a href=https://docs.brew.sh/Installation>Various</a></td>
      <td><a href=https://brew.sh>Homebrew</a></td>
      <td><a href=https://formulae.brew.sh/formula/just>just</a></td>
      <td><code>brew install just</code></td>
    </tr>
    <tr>
      <td><a href=https://nixos.org/download.html#download-nix>Various</a></td>
      <td><a href=https://nixos.org/nix/>Nix</a></td>
      <td><a href=https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/tools/just/default.nix>just</a></td>
      <td><code>nix-env -iA nixpkgs.just</code></td>
    </tr>
    <tr>
      <td><a href=https://snapcraft.io/docs/installing-snapd>Various</a></td>
      <td><a href=https://snapcraft.io>Snap</a></td>
      <td><a href=https://snapcraft.io/just>just</a></td>
      <td><code>snap install --edge --classic just</code></td>
    </tr>
    <tr>
      <td><a href=https://voidlinux.org>Void Linux</a></td>
      <td><a href=https://wiki.voidlinux.org/XBPS>XBPS</a></td>
      <td><a href=https://github.com/void-linux/void-packages/blob/master/srcpkgs/just/template>just</a></td>
      <td><code>xbps-install -S just</code></td>
    </tr>
  </tbody>
</table>

![package version table](https://repology.org/badge/vertical-allrepos/just.svg)

### Pre-Built Binaries

Pre-built binaries for Linux, MacOS, and Windows can be found on
[the releases page](https://github.com/casey/just/releases).

You can use the following command on Linux, MacOS, or Windows to download the
latest release, just replace `DEST` with the directory where you'd like to put
`just`:



For example, to install `just` to `~/bin`:



Note that `install.sh` may fail on GitHub Actions, or in other environments
where many machines share IP addresses. `install.sh` calls GitHub APIs in order
to determine the latest version of `just` to install, and those API calls are
rate-limited on a per-IP basis. To make `install.sh` more reliable in such
circumstances, pass a specific tag to install with `--tag`.

### GitHub Actions

Developers may be interested in running the same `just` commands that they use
locally on continuous integration platforms such as GitHub Actions. For example,
every time that a contributor creates a pull request, a GitHub Action could run
`just test` on the three major operating systems to provide feedback to both the
contributor and reviewers that tests are passing.

Demonstrate how to install and use just in GitHub Actions on the three major
operating systems without needing third-party GitHub Actions. Put the following
code into a `.github/workflows/just_test.yml` file.



Or with [extractions/setup-just](https://github.com/extractions/setup-just):



Or with [taiki-e/install-action](https://github.com/taiki-e/install-action):



### Release RSS Feed

An [RSS feed](https://en.wikipedia.org/wiki/RSS) of `just` releases is available [here](https://github.com/casey/just/releases.atom).

### Node.js Installation

[just-install](https://npmjs.com/package/just-install) can be used to automate
installation of `just` in Node.js applications.

`just` is a great, more robust alternative to npm scripts. If you want to
include `just` in the dependencies of a Node.js application, `just-install`
will install a local, platform-specific binary as part of the `npm install`
command. This removes the need for every developer to install `just`
independently using one of the processes mentioned above. After installation,
the `just` command will work in npm scripts or with npx. It's great for teams
who want to make the set up process for their project as easy as possible.

For more information, see the
[just-install README file](https://github.com/brombal/just-install#readme).

Backwards Compatibility
-----------------------

With the release of version 1.0, `just` features a strong commitment to
backwards compatibility and stability.

Future releases will not introduce backwards incompatible changes that make
existing `justfile`s stop working, or break working invocations of the
command-line interface.

This does not, however, preclude fixing outright bugs, even if doing so might
break `justfiles` that rely on their behavior.

There will never be a `just` 2.0. Any desirable backwards-incompatible changes
will be opt-in on a per-`justfile` basis, so users may migrate at their
leisure.

Features that aren't yet ready for stabilization are gated behind the
`--unstable` flag. Features enabled by `--unstable` may change in backwards
incompatible ways at any time. Unstable features can also be enabled by setting
the environment variable `JUST_UNSTABLE` to any value other than `false`, `0`,
or the empty string.

Editor Support
--------------

`justfile` syntax is close enough to `make` that you may want to tell your
editor to use `make` syntax highlighting for `just`.

### Vim and Neovim

#### `vim-just`

The [vim-just](https://github.com/NoahTheDuke/vim-just) plugin provides syntax
highlighting for `justfile`s.

Install it with your favorite package manager, like
[Plug](https://github.com/junegunn/vim-plug):



Or with Vim's built-in package support:



#### `tree-sitter-just`

[tree-sitter-just](https://github.com/IndianBoy42/tree-sitter-just) is an
[Nvim Treesitter](https://github.com/nvim-treesitter/nvim-treesitter) plugin
for Neovim.

#### Makefile Syntax Highlighting

Vim's built-in makefile syntax highlighting isn't perfect for `justfile`s, but
it's better than nothing. You can put the following in `~/.vim/filetype.vim`:



Or add the following to an individual `justfile` to enable `make` mode on a
per-file basis:



### Emacs

[just-mode](https://github.com/leon-barrett/just-mode.el) provides syntax
highlighting and automatic indentation of `justfile`s. It is available on
[MELPA](https://melpa.org/) as [just-mode](https://melpa.org/#/just-mode).

[justl](https://github.com/psibi/justl.el) provides commands for executing and
listing recipes.

You can add the following to an individual `justfile` to enable `make` mode on
a per-file basis:



### Visual Studio Code

An extension for VS Code by [skellock](https://github.com/skellock) is
[available here](https://marketplace.visualstudio.com/items?itemName=skellock.just)
([repository](https://github.com/skellock/vscode-just)), but is no longer
actively developed.

You can install it from the command line by running:



An more recently active fork by [sclu1034](https://github.com/sclu1034) is
available [here](https://github.com/sclu1034/vscode-just).

### JetBrains IDEs

A plugin for JetBrains IDEs by [linux_china](https://github.com/linux-china) is
[available here](https://plugins.jetbrains.com/plugin/18658-just).

### Kakoune

Kakoune supports `justfile` syntax highlighting out of the box, thanks to
TeddyDD.

### Helix

[Helix](https://helix-editor.com/) supports `justfile` syntax highlighting
out-of-the-box since version 23.05.

### Sublime Text

The [Just package](https://github.com/nk9/just_sublime) by
[nk9](https://github.com/nk9) with `just` syntax and some other tools is
available on [PackageControl](https://packagecontrol.io/packages/Just).

### Micro

[Micro](https://micro-editor.github.io/) supports Justfile syntax highlighting
out of the box, thanks to [tomodachi94](https://github.com/tomodachi94).

### Other Editors

Feel free to send me the commands necessary to get syntax highlighting working
in your editor of choice so that I may include them here.

Quick Start
-----------

See [the installation section](#installation) for how to install `just` on your
computer. Try running `just --version` to make sure that it's installed
correctly.

For an overview of the syntax, check out
[this cheatsheet](https://cheatography.com/linux-china/cheat-sheets/justfile/).

Once `just` is installed and working, create a file named `justfile` in the
root of your project with the following contents:



When you invoke `just` it looks for file `justfile` in the current directory
and upwards, so you can invoke it from any subdirectory of your project.

The search for a `justfile` is case insensitive, so any case, like `Justfile`,
`JUSTFILE`, or `JuStFiLe`, will work. `just` will also look for files with the
name `.justfile`, in case you'd like to hide a `justfile`.

Running `just` with no arguments runs the first recipe in the `justfile`:



One or more arguments specify the recipe(s) to run:



`just` prints each command to standard error before running it, which is why
`echo 'This is a recipe!'` was printed. This is suppressed for lines starting
with `@`, which is why `echo 'This is another recipe.'` was not printed.

Recipes stop running if a command fails. Here `cargo publish` will only run if
`cargo test` succeeds:



Recipes can depend on other recipes. Here the `test` recipe depends on the
`build` recipe, so `build` will run before `test`:





Recipes without dependencies will run in the order they're given on the command
line:



Dependencies will always run first, even if they are passed after a recipe that
depends on them:



Examples
--------

A variety of example `justfile`s can be found in the
[examples directory](https://github.com/casey/just/tree/master/examples).

Features
--------

### The Default Recipe

When `just` is invoked without a recipe, it runs the first recipe in the
`justfile`. This recipe might be the most frequently run command in the
project, like running the tests:



You can also use dependencies to run multiple recipes by default:



If no recipe makes sense as the default recipe, you can add a recipe to the
beginning of your `justfile` that lists the available recipes:



### Listing Available Recipes

Recipes can be listed in alphabetical order with `just --list`:



`just --summary` is more concise:



Pass `--unsorted` to print recipes in the order they appear in the `justfile`:







If you'd like `just` to default to listing the recipes in the `justfile`, you
can use this as your default recipe:



Note that you may need to add `--justfile {{justfile()}}` to the line above.
Without it, if you executed `just -f /some/distant/justfile -d .` or
`just -f ./non-standard-justfile`, the plain `just --list` inside the recipe
would not necessarily use the file you provided. It would try to find a
justfile in your current path, maybe even resulting in a `No justfile found`
error.

The heading text can be customized with `--list-heading`:



And the indentation can be customized with `--list-prefix`:



The argument to `--list-heading` replaces both the heading and the newline
following it, so it should contain a newline if non-empty. It works this way so
you can suppress the heading line entirely by passing the empty string:



### Aliases

Aliases allow recipes to be invoked on the command line with alternative names:





### Settings

Settings control interpretation and execution. Each setting may be specified at
most once, anywhere in the `justfile`.

For example:



#### Table of Settings

| Name | Value | Default | Description |
|------|-------|---------|-------------|
| `allow-duplicate-recipes` | boolean | `false` | Allow recipes appearing later in a `justfile` to override earlier recipes with the same name. |
| `dotenv-filename` | string | - | Load a `.env` file with a custom name, if present. |
| `dotenv-load` | boolean | `false` | Load a `.env` file, if present. |
| `dotenv-path` | string | - | Load a `.env` file from a custom path, if present. Overrides `dotenv-filename`. |
| `export` | boolean | `false` | Export all variables as environment variables. |
| `fallback` | boolean | `false` | Search `justfile` in parent directory if the first recipe on the command line is not found. |
| `ignore-comments` | boolean | `false` | Ignore recipe lines beginning with `#`. |
| `positional-arguments` | boolean | `false` | Pass positional arguments. |
| `shell` | `[COMMAND, ARGS…]` | - | Set the command used to invoke recipes and evaluate backticks. |
| `tempdir` | string | - | Create temporary directories in `tempdir` instead of the system default temporary directory. |
| `windows-powershell` | boolean | `false` | Use PowerShell on Windows as default shell. (Deprecated. Use `windows-shell` instead. |
| `windows-shell` | `[COMMAND, ARGS…]` | - | Set the command used to invoke recipes and evaluate backticks. |

Boolean settings can be written as:



Which is equivalent to:



#### Allow Duplicate Recipes

If `allow-duplicate-recipes` is set to `true`, defining multiple recipes with
the same name is not an error and the last definition is used. Defaults to
`false`.





#### Dotenv Settings

If `dotenv-load`, `dotenv-filename` or `dotenv-path` is set, `just` will load
environment variables from a file.

If `dotenv-path` is set, `just` will look for a file at the given path.

Otherwise, `just` looks for a file named `.env` by default, unless
`dotenv-filename` set, in which case the value of `dotenv-filename` is used.
This file can be located in the same directory as your `justfile` or in a
parent directory.

The loaded variables are environment variables, not `just` variables, and so
must be accessed using `$VARIABLE_NAME` in recipes and backticks.

For example, if your `.env` file contains:



And your `justfile` contains:



`just serve` will output:



#### Export

The `export` setting causes all `just` variables to be exported as environment
variables. Defaults to `false`.





#### Positional Arguments

If `positional-arguments` is `true`, recipe arguments will be passed as
positional arguments to commands. For linewise recipes, argument `$0` will be
the name of the recipe.

For example, running this recipe:



Will produce the following output:



When using an `sh`-compatible shell, such as `bash` or `zsh`, `$@` expands to
the positional arguments given to the recipe, starting from one. When used
within double quotes as `"$@"`, arguments including whitespace will be passed
on as if they were double-quoted. That is, `"$@"` is equivalent to `"$1" "$2"`…
When there are no positional parameters, `"$@"` and `$@` expand to nothing
(i.e., they are removed).

This example recipe will print arguments one by one on separate lines:



Running it with _two_ arguments:



#### Shell

The `shell` setting controls the command used to invoke recipe lines and
backticks. Shebang recipes are unaffected.



`just` passes the command to be executed as an argument. Many shells will need
an additional flag, often `-c`, to make them evaluate the first argument.

##### Windows Shell

`just` uses `sh` on Windows by default. To use a different shell on Windows,
use `windows-shell`:



See
[powershell.just](https://github.com/casey/just/blob/master/examples/powershell.just)
for a justfile that uses PowerShell on all platforms.

##### Windows PowerShell

*`set windows-powershell` uses the legacy `powershell.exe` binary, and is no
longer recommended. See the `windows-shell` setting above for a more flexible
way to control which shell is used on Windows.*

`just` uses `sh` on Windows by default. To use `powershell.exe` instead, set
`windows-powershell` to true.



##### Python 3



##### Bash



##### Z Shell



##### Fish



##### Nushell



If you want to change the default table mode to `light`:



*[Nushell](https://github.com/nushell/nushell) was written in Rust, and **has
cross-platform support for Windows / macOS and Linux**.*

### Documentation Comments

Comments immediately preceding a recipe will appear in `just --list`:





### Variables and Substitution

Variables, strings, concatenation, path joining, and substitution using `{{…}}`
are supported:



#### Joining Paths

The `/` operator can be used to join two strings with a slash:





Note that a `/` is added even if one is already present:





Absolute paths can also be constructed<sup>1.5.0</sup>:





The `/` operator uses the `/` character, even on Windows. Thus, using the `/`
operator should be avoided with paths that use universal naming convention
(UNC), i.e., those that start with `\?`, since forward slashes are not
supported with UNC paths.

#### Escaping `{{`

To write a recipe containing `{{`, use `{{{{`:



(An unmatched `}}` is ignored, so it doesn't need to be escaped.)

Another option is to put all the text you'd like to escape inside of an
interpolation:



Yet another option is to use `{{ "{{" }}`:



### Strings

Double-quoted strings support escape sequences:





Strings may contain line breaks:



Single-quoted strings do not recognize escape sequences:





Indented versions of both single- and double-quoted strings, delimited by
triple single- or triple double-quotes, are supported. Indented string lines
are stripped of a leading line break, and leading whitespace common to all
non-blank lines:



Similar to unindented strings, indented double-quoted strings process escape
sequences, and indented single-quoted strings ignore escape sequences. Escape
sequence processing takes place after unindentation. The unindentation
algorithm does not take escape-sequence produced whitespace or newlines into
account.

### Ignoring Errors

Normally, if a command returns a non-zero exit status, execution will stop. To
continue execution after a command, even if it fails, prefix the command with
`-`:





### Functions

`just` provides a few built-in functions that might be useful when writing
recipes.

#### System Information

- `arch()` — Instruction set architecture. Possible values are: `"aarch64"`,
  `"arm"`, `"asmjs"`, `"hexagon"`, `"mips"`, `"msp430"`, `"powerpc"`,
  `"powerpc64"`, `"s390x"`, `"sparc"`, `"wasm32"`, `"x86"`, `"x86_64"`, and
  `"xcore"`.
- `num_cpus()`<sup>1.15.0</sup> - Number of logical CPUs.
- `os()` — Operating system. Possible values are: `"android"`, `"bitrig"`,
  `"dragonfly"`, `"emscripten"`, `"freebsd"`, `"haiku"`, `"ios"`, `"linux"`,
  `"macos"`, `"netbsd"`, `"openbsd"`, `"solaris"`, and `"windows"`.
- `os_family()` — Operating system family; possible values are: `"unix"` and
  `"windows"`.

For example:





The `os_family()` function can be used to create cross-platform `justfile`s
that work on various operating systems. For an example, see
[cross-platform.just](https://github.com/casey/just/blob/master/examples/cross-platform.just)
file.

#### Environment Variables

- `env_var(key)` — Retrieves the environment variable with name `key`, aborting
  if it is not present.





- `env_var_or_default(key, default)` — Retrieves the environment variable with
  name `key`, returning `default` if it is not present.
- `env(key)`<sup>1.15.0</sup> — Alias for `env_var(key)`.
- `env(key, default)`<sup>1.15.0</sup> — Alias for `env_var_or_default(key, default)`.

#### Invocation Directory

- `invocation_directory()` - Retrieves the absolute path to the current
  directory when `just` was invoked, before  `just` changed it (chdir'd) prior
  to executing commands. On Windows, `invocation_directory()` uses `cygpath` to
  convert the invocation directory to a Cygwin-compatible `/`-separated path.
  Use `invocation_directory_native()` to return the verbatim invocation
  directory on all platforms.

For example, to call `rustfmt` on files just under the "current directory"
(from the user/invoker's perspective), use the following rule:



Alternatively, if your command needs to be run from the current directory, you
could use (e.g.):



- `invocation_directory_native()` - Retrieves the absolute path to the current
  directory when `just` was invoked, before  `just` changed it (chdir'd) prior
  to executing commands.

#### Justfile and Justfile Directory

- `justfile()` - Retrieves the path of the current `justfile`.

- `justfile_directory()` - Retrieves the path of the parent directory of the
  current `justfile`.

For example, to run a command relative to the location of the current
`justfile`:



#### Just Executable

- `just_executable()` - Absolute path to the `just` executable.

For example:





#### Just Process ID

- `just_pid()` - Process ID of the `just` executable.

For example:






#### String Manipulation

- `quote(s)` - Replace all single quotes with `'\''` and prepend and append
  single quotes to `s`. This is sufficient to escape special characters for
  many shells, including most Bourne shell descendants.
- `replace(s, from, to)` - Replace all occurrences of `from` in `s` to `to`.
- `replace_regex(s, regex, replacement)` - Replace all occurrences of `regex`
  in `s` to `replacement`. Regular expressions are provided by the
  [Rust `regex` create](https://docs.rs/regex/latest/regex/). See the
  [syntax documentation](https://docs.rs/regex/latest/regex/#syntax) for usage
  examples. Capture groups are supported. The `replacement` string uses
  [Replacement string syntax](https://docs.rs/regex/latest/regex/struct.Regex.html#replacement-string-syntax).
- `trim(s)` - Remove leading and trailing whitespace from `s`.
- `trim_end(s)` - Remove trailing whitespace from `s`.
- `trim_end_match(s, pat)` - Remove suffix of `s` matching `pat`.
- `trim_end_matches(s, pat)` - Repeatedly remove suffixes of `s` matching
  `pat`.
- `trim_start(s)` - Remove leading whitespace from `s`.
- `trim_start_match(s, pat)` - Remove prefix of `s` matching `pat`.
- `trim_start_matches(s, pat)` - Repeatedly remove prefixes of `s` matching
  `pat`.

#### Case Conversion

- `capitalize(s)`<sup>1.7.0</sup> - Convert first character of `s` to uppercase
  and the rest to lowercase.
- `kebabcase(s)`<sup>1.7.0</sup> - Convert `s` to `kebab-case`.
- `lowercamelcase(s)`<sup>1.7.0</sup> - Convert `s` to `lowerCamelCase`.
- `lowercase(s)` - Convert `s` to lowercase.
- `shoutykebabcase(s)`<sup>1.7.0</sup> - Convert `s` to `SHOUTY-KEBAB-CASE`.
- `shoutysnakecase(s)`<sup>1.7.0</sup> - Convert `s` to `SHOUTY_SNAKE_CASE`.
- `snakecase(s)`<sup>1.7.0</sup> - Convert `s` to `snake_case`.
- `titlecase(s)`<sup>1.7.0</sup> - Convert `s` to `Title Case`.
- `uppercamelcase(s)`<sup>1.7.0</sup> - Convert `s` to `UpperCamelCase`.
- `uppercase(s)` - Convert `s` to uppercase.

#### Path Manipulation

##### Fallible

- `absolute_path(path)` - Absolute path to relative `path` in the working
  directory. `absolute_path("./bar.txt")` in directory `/foo` is
  `/foo/bar.txt`.
- `canonicalize(path)`<sup>1.24.0</sup> - Canonicalize `path` by resolving symlinks and removing
  `.`, `..`, and extra `/`s where possible.
- `extension(path)` - Extension of `path`. `extension("/foo/bar.txt")` is
  `txt`.
- `file_name(path)` - File name of `path` with any leading directory components
  removed. `file_name("/foo/bar.txt")` is `bar.txt`.
- `file_stem(path)` - File name of `path` without extension.
  `file_stem("/foo/bar.txt")` is `bar`.
- `parent_directory(path)` - Parent directory of `path`.
  `parent_directory("/foo/bar.txt")` is `/foo`.
- `without_extension(path)` - `path` without extension.
  `without_extension("/foo/bar.txt")` is `/foo/bar`.

These functions can fail, for example if a path does not have an extension,
which will halt execution.

##### Infallible

- `clean(path)` - Simplify `path` by removing extra path separators,
  intermediate `.` components, and `..` where possible. `clean("foo//bar")` is
  `foo/bar`, `clean("foo/..")` is `.`, `clean("foo/./bar")` is `foo/bar`.
- `join(a, b…)` - *This function uses `/` on Unix and `\` on Windows, which can
  be lead to unwanted behavior. The `/` operator, e.g., `a / b`, which always
  uses `/`, should be considered as a replacement unless `\`s are specifically
  desired on Windows.* Join path `a` with path `b`. `join("foo/bar", "baz")` is
  `foo/bar/baz`. Accepts two or more arguments.

#### Filesystem Access

- `path_exists(path)` - Returns `true` if the path points at an existing entity
  and `false` otherwise. Traverses symbolic links, and returns `false` if the
  path is inaccessible or points to a broken symlink.

##### Error Reporting

- `error(message)` - Abort execution and report error `message` to user.

#### UUID and Hash Generation

- `blake3(string)`<sup>1.25.0</sup> - Return [BLAKE3] hash of `string` as hexadecimal string.
- `blake3_file(path)`<sup>1.25.0</sup> - Return [BLAKE3] hash of file at `path` as hexadecimal
  string.
- `sha256(string)` - Return the SHA-256 hash of `string` as hexadecimal string.
- `sha256_file(path)` - Return SHA-256 hash of file at `path` as hexadecimal
  string.
- `uuid()` - Generate a random version 4 UUID.

[BLAKE3]: https://github.com/BLAKE3-team/BLAKE3/

#### Semantic Versions

- `semver_matches(version, requirement)`<sup>1.16.0</sup> - Check whether a
  [semantic `version`](https://semver.org), e.g., `"0.1.0"` matches a
  `requirement`, e.g., `">=0.1.0"`, returning `"true"` if so and `"false"`
  otherwise.

##### XDG Directories<sup>1.23.0</sup>

These functions return paths to user-specific directories for things like
configuration, data, caches, executables, and the user's home directory. These
functions follow the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html),
and are implemented with the
[`dirs`](https://docs.rs/dirs/latest/dirs/index.html) create.

- `cache_directory()` - The user-specific cache directory.
- `config_directory()` - The user-specific configuration directory.
- `config_local_directory()` - The local user-specific configuration directory.
- `data_directory()` - The user-specific data directory.
- `data_local_directory()` - The local user-specific data directory.
- `executable_directory()` - The user-specific executable directory.
- `home_directory()` - The user's home directory.

### Recipe Attributes

Recipes may be annotated with attributes that change their behavior.

| Name | Description |
|------|-------------|
| `[confirm]`<sup>1.17.0</sup> | Require confirmation prior to executing recipe. |
| `[confirm("prompt")]`<sup>1.23.0</sup> | Require confirmation prior to executing recipe with a custom prompt. |
| `[linux]`<sup>1.8.0</sup> | Enable recipe on Linux. |
| `[macos]`<sup>1.8.0</sup> | Enable recipe on MacOS. |
| `[no-cd]`<sup>1.9.0</sup> | Don't change directory before executing recipe. |
| `[no-exit-message]`<sup>1.7.0</sup> | Don't print an error message if recipe fails. |
| `[no-quiet]`<sup>1.23.0</sup> | Override globally quiet recipes and always echo out the recipe. |
| `[private]`<sup>1.10.0</sup> | See [Private Recipes](#private-recipes). |
| `[unix]`<sup>1.8.0</sup> | Enable recipe on Unixes. (Includes MacOS). |
| `[windows]`<sup>1.8.0</sup> | Enable recipe on Windows. |

A recipe can have multiple attributes, either on multiple lines:



Or separated by commas on a single line<sup>1.14.0</sup>:



#### Enabling and Disabling Recipes<sup>1.8.0</sup>

The `[linux]`, `[macos]`, `[unix]`, and `[windows]` attributes are
configuration attributes. By default, recipes are always enabled. A recipe with
one or more configuration attributes will only be enabled when one or more of
those configurations is active.

This can be used to write `justfile`s that behave differently depending on
which operating system they run on. The `run` recipe in this `justfile` will
compile and run `main.c`, using a different C compiler and using the correct
output binary name for that compiler depending on the operating system:



#### Disabling Changing Directory<sup>1.9.0</sup>

`just` normally executes recipes with the current directory set to the
directory that contains the `justfile`. This can be disabled using the
`[no-cd]` attribute. This can be used to create recipes which use paths
relative to the invocation directory, or which operate on the current
directory.

For example, this `commit` recipe:



Can be used with paths that are relative to the current directory, because
`[no-cd]` prevents `just` from changing the current directory when executing
`commit`.

#### Requiring Confirmation for Recipes<sup>1.17.0</sup>

`just` normally executes all recipes unless there is an error. The `[confirm]`
attribute allows recipes require confirmation in the terminal prior to running.
This can be overridden by passing `--yes` to `just`, which will automatically
confirm any recipes marked by this attribute.

Recipes dependent on a recipe that requires confirmation will not be run if the
relied upon recipe is not confirmed, as well as recipes passed after any recipe
that requires confirmation.



#### Custom Confirmation Prompt<sup>1.23.0</sup>

The default confirmation prompt can be overridden with `[confirm(PROMPT)]`:



### Command Evaluation Using Backticks

Backticks can be used to store the result of commands:



Indented backticks, delimited by three backticks, are de-indented in the same
manner as indented strings:


    echo foo
    echo bar
  `

See the [Strings](#strings) section for details on unindenting.

Backticks may not start with `#!`. This syntax is reserved for a future
upgrade.

### Conditional Expressions

`if`/`else` expressions evaluate different branches depending on if two
expressions evaluate to the same value:





It is also possible to test for inequality:





And match against regular expressions:





Regular expressions are provided by the
[regex create](https://github.com/rust-lang/regex), whose syntax is documented on
[docs.rs](https://docs.rs/regex/1.5.4/regex/#syntax). Since regular expressions
commonly use backslash escape sequences, consider using single-quoted string
literals, which will pass slashes to the regex parser unmolested.

Conditional expressions short-circuit, which means they only evaluate one of
their branches. This can be used to make sure that backtick expressions don't
run when they shouldn't.



Conditionals can be used inside of recipes:



Note the space after the final `}`! Without the space, the interpolation will
be prematurely closed.

Multiple conditionals can be chained:





### Stopping execution with error

Execution can be halted with the `error` function. For example:



Which produce the following error when run:



### Setting Variables from the Command Line

Variables can be overridden from the command line.





Any number of arguments of the form `NAME=VALUE` can be passed before recipes:



Or you can use the `--set` flag:



### Getting and Setting Environment Variables

#### Exporting `just` Variables

Assignments prefixed with the `export` keyword will be exported to recipes as
environment variables:



Parameters prefixed with a `$` will be exported as environment variables:



Exported variables and parameters are not exported to backticks in the same scope.





When [export](#export) is set, all `just` variables are exported as environment
variables.

#### Getting Environment Variables from the environment

Environment variables from the environment are passed automatically to the
recipes.





#### Setting `just` Variables from Environment Variables

Environment variables can be propagated to `just` variables using the functions
`env_var()` and `env_var_or_default()`. See
[environment-variables](#environment-variables).

### Recipe Parameters

Recipes may have parameters. Here recipe `build` has a parameter called
`target`:



To pass arguments on the command line, put them after the recipe name:



To pass arguments to a dependency, put the dependency in parentheses along with
the arguments:



Variables can also be passed as arguments to dependencies:



A command's arguments can be passed to dependency by putting the dependency in
parentheses along with the arguments:



Parameters may have default values:



Parameters with default values may be omitted:



Or supplied:



Default values may be arbitrary expressions, but concatenations or path joins
must be parenthesized:



The last parameter of a recipe may be variadic, indicated with either a `+` or
a `*` before the argument name:



Variadic parameters prefixed with `+` accept _one or more_ arguments and expand
to a string containing those arguments separated by spaces:



Variadic parameters prefixed with `*` accept _zero or more_ arguments and
expand to a string containing those arguments separated by spaces, or an empty
string if no arguments are present:



Variadic parameters can be assigned default values. These are overridden by
arguments passed on the command line:



`{{…}}` substitutions may need to be quoted if they contain spaces. For
example, if you have the following recipe:



And you type:



`just` will run the command `lynx https://www.google.com/?q=cat toupee`, which
will get parsed by `sh` as `lynx`, `https://www.google.com/?q=cat`, and
`toupee`, and not the intended `lynx` and `https://www.google.com/?q=cat toupee`.

You can fix this by adding quotes:



Parameters prefixed with a `$` will be exported as environment variables:



### Running Recipes at the End of a Recipe

Normal dependencies of a recipes always run before a recipe starts. That is to
say, the dependee always runs before the depender. These dependencies are
called "prior dependencies".

A recipe can also have subsequent dependencies, which run after the recipe and
are introduced with an `&&`:



…running _b_ prints:



### Running Recipes in the Middle of a Recipe

`just` doesn't support running recipes in the middle of another recipe, but you
can call `just` recursively in the middle of a recipe. Given the following
`justfile`:



…running _b_ prints:



This has limitations, since recipe `c` is run with an entirely new invocation
of `just`: Assignments will be recalculated, dependencies might run twice, and
command line arguments will not be propagated to the child `just` process.

### Writing Recipes in Other Languages

Recipes that start with `#!` are called shebang recipes, and are executed by
saving the recipe body to a file and running it. This let's you write recipes in
different languages:





On Unix-like operating systems, including Linux and MacOS, shebang recipes are
executed by saving the recipe body to a file in a temporary directory, marking
the file as executable, and executing it. The OS then parses the shebang line
into a command line and invokes it, including the path to the file. For
example, if a recipe starts with `#!/usr/bin/env bash`, the final command that
the OS runs will be something like `/usr/bin/env bash
/tmp/PATH_TO_SAVED_RECIPE_BODY`. Keep in mind that different operating systems
split shebang lines differently.

Windows does not support shebang lines. On Windows, `just` splits the shebang
line into a command and arguments, saves the recipe body to a file, and invokes
the split command and arguments, adding the path to the saved recipe body as
the final argument. For example, on Windows, if a recipe starts with `#! py`,
the final command the OS runs will be something like `py
C:\Temp\PATH_TO_SAVED_RECIPE_BODY`.

### Safer Bash Shebang Recipes

If you're writing a `bash` shebang recipe, consider adding `set -euxo
pipefail`:



It isn't strictly necessary, but `set -euxo pipefail` turns on a few useful
features that make `bash` shebang recipes behave more like normal, linewise
`just` recipe:

- `set -e` makes `bash` exit if a command fails.

- `set -u` makes `bash` exit if a variable is undefined.

- `set -x` makes `bash` print each script line before it's run.

- `set -o pipefail` makes `bash` exit if a command in a pipeline fails. This is
  `bash`-specific, so isn't turned on in normal linewise `just` recipes.

Together, these avoid a lot of shell scripting gotchas.

#### Shebang Recipe Execution on Windows

On Windows, shebang interpreter paths containing a `/` are translated from
Unix-style paths to Windows-style paths using `cygpath`, a utility that ships
with [Cygwin](http://www.cygwin.com).

For example, to execute this recipe on Windows:



The interpreter path `/bin/sh` will be translated to a Windows-style path using
`cygpath` before being executed.

If the interpreter path does not contain a `/` it will be executed without
being translated. This is useful if `cygpath` is not available, or you wish to
pass a Windows-style path to the interpreter.

### Setting Variables in a Recipe

Recipe lines are interpreted by the shell, not `just`, so it's not possible to
set `just` variables in the middle of a recipe:



It is possible to use shell variables, but there's another problem. Every
recipe line is run by a new shell instance, so variables set in one line won't
be set in the next:



The best way to work around this is to use a shebang recipe. Shebang recipe
bodies are extracted and run as scripts, so a single shell instance will run
the whole thing:



### Sharing Environment Variables Between Recipes

Each line of each recipe is executed by a fresh shell, so it is not possible to
share environment variables between recipes.

#### Using Python Virtual Environments

Some tools, like [Python's venv](https://docs.python.org/3/library/venv.html),
require loading environment variables in order to work, making them challenging
to use with `just`. As a workaround, you can execute the virtual environment
binaries directly:



### Changing the Working Directory in a Recipe

Each recipe line is executed by a new shell, so if you change the working
directory on one line, it won't have an effect on later lines:



There are a couple ways around this. One is to call `cd` on the same line as
the command you want to run:



The other is to use a shebang recipe. Shebang recipe bodies are extracted and
run as scripts, so a single shell instance will run the whole thing, and thus a
`pwd` on one line will affect later lines, just like a shell script:



### Indentation

Recipe lines can be indented with spaces or tabs, but not a mix of both. All of
a recipe's lines must have the same type of indentation, but different recipes
in the same `justfile` may use different indentation.

Each recipe must be indented at least one level from the `recipe-name` but
after that may be further indented.

Here's a justfile with a recipe indented with spaces, represented as `·`, and
tabs, represented as `→`.





### Multi-Line Constructs

Recipes without an initial shebang are evaluated and run line-by-line, which
means that multi-line constructs probably won't do what you want.

For example, with the following `justfile`:



The extra leading whitespace before the second line of the `conditional` recipe
will produce a parse error:



To work around this, you can write conditionals on one line, escape newlines
with slashes, or add a shebang to your recipe. Some examples of multi-line
constructs are provided for reference.

#### `if` statements







#### `for` loops







#### `while` loops







#### Outside Recipe Bodies

Parenthesized expressions can span multiple lines:



Lines ending with a backslash continue on to the next line as if the lines were
joined by whitespace<sup>1.15.0</sup>:



Backslash line continuations can also be used in interpolations. The line
following the backslash must start with the same indentation as the recipe
body, although additional indentation is accepted.



### Command Line Options

`just` supports a number of useful command line options for listing, dumping,
and debugging recipes and variables:



Run `just --help` to see all the options.

### Private Recipes

Recipes and aliases whose name starts with a `_` are omitted from `just --list`:





And from `just --summary`:



The `[private]` attribute<sup>1.10.0</sup> may also be used to hide recipes or
aliases without needing to change the name:





This is useful for helper recipes which are only meant to be used as
dependencies of other recipes.

### Quiet Recipes

A recipe name may be prefixed with `@` to invert the meaning of `@` before each
line:



Now only the lines starting with `@` will be echoed:



All recipes in a Justfile can be made quiet with `set quiet`:



The `[no-quiet]` attribute overrides this setting:



Shebang recipes are quiet by default:





Adding `@` to a shebang recipe name makes `just` print the recipe before
executing it:





`just` normally prints error messages when a recipe line fails. These error
messages can be suppressed using the `[no-exit-message]`<sup>1.7.0</sup>
attribute. You may find this especially useful with a recipe that wraps a tool:





Add the attribute to suppress the exit error message when the tool exits with a
non-zero code:





### Selecting Recipes to Run With an Interactive Chooser

The `--choose` subcommand makes `just` invoke a chooser to select which recipes
to run. Choosers should read lines containing recipe names from standard input
and print one or more of those names separated by spaces to standard output.

Because there is currently no way to run a recipe that requires arguments with
`--choose`, such recipes will not be given to the chooser. Private recipes and
aliases are also skipped.

The chooser can be overridden with the `--chooser` flag. If `--chooser` is not
given, then `just` first checks if `$JUST_CHOOSER` is set. If it isn't, then
the chooser defaults to `fzf`, a popular fuzzy finder.

Arguments can be included in the chooser, i.e. `fzf --exact`.

Then open your browser to <http://127.0.0.1:8000> to see the result.

## Combining FastAPI and Air

Air is just a layer over FastAPI. So it is trivial to combine sophisticated HTML pages and a REST API into one app.

```python
import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

@app.get("/")
def landing_page():
    return air.Html(
        air.Head(air.Title("Awesome SaaS")),
        air.Body(
            air.H1("Awesome SaaS"),
            air.P(air.A("API Docs", target="_blank", href="/api/docs")),
        ),
    )


@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}

# Combining the Air and FastAPI apps into one
app.mount("/api", api)
```

## Combining FastAPI and Air using Jinja2

Want to use Jinja2 instead of Air Tags? We've got you covered.

```python
import air
from air.requests import Request
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

# Air's JinjaRenderer is a shortcut for using Jinja templates
jinja = air.JinjaRenderer(directory="templates")

@app.get("/")
def index(request: Request):
    return jinja(request, name="home.html")

@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}

# Combining the Air and and FastAPI apps into one
app.mount("/api", api)
```

Don't forget the Jinja template!

```html
<!doctype html
<html>
    <head>
        <title>Awesome SaaS</title>
    </head>
    <body>
        <h1>Awesome SaaS</h1>
        <p>
            <a target="_blank" href="/api/docs">API Docs</a>
        </p>
    </body>
</html>
```

> [!NOTE]
> Using Jinja with Air is easier than with FastAPI. That's because as much as we enjoy Air Tags, we also love Jinja!

## Sponsors

Maintenance of this project is made possible by all the [contributors](https://github.com/feldroy/air/graphs/contributors) and [sponsors](https://github.com/sponsors/feldroy).
If you would like to support this project and have your avatar or company logo appear below, please [sponsor us](https://github.com/sponsors/feldroy). 💖💨

<!-- SPONSORS -->

<!-- SPONSORS -->

Consider this low-barrier form of contribution yourself.
Your [support](https://github.com/sponsors/feldroy) is much appreciated.

## Contributing

For guidance on setting up a development environment and how to make a contribution to Air, see [Contributing to Air](https://github.com/feldroy/air/blob/main/CONTRIBUTING.md).

## Contributors

Thanks to all the contributors to the Air 💨 web framework!

<a href="https://github.com/feldroy/air/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=feldroy/air" />
</a>
