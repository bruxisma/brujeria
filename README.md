<p align="center">
  <img src="https://github.com/slurps-mad-rips/brujeria/blob/master/docs/logo.png?raw=true">
</p>

# Overview

Brujería is a python library that simplifies development workflow for native
extensions. It does this by providing import hooks that allow you to compile
your extensions on import (much like [cppimport]) so you can play around with
the API in a REPL. Lastly, it provides some hooks so that using these from
tools like [poetry] are just a single line. It does all of this via CMake, but
in a way to reduce the need to touch CMake in the first place.

Brujería currently utilizes [IXM](https://ixm.one) to reduce the overhead of
maintaining a CMake project.

## Features

Currently, Brujería provides the following:

 * [x] Automatic discovery of C and C++ extensions.
 * [x] Basic MinGW Support (CPython does not guarantee this)
 * [x] Works on Windows, macOS, and Linux
 * [x] The ability to mix C *and* C++ in a single extension (`distutils`/
       `setuptools` do not currently permit this)
 * [ ] Basic [poetry] integration via preprovided `build` function.
 * [ ] `pyproject.toml` integration for configuration settings

## Why the name?

Brujería is a spanish word for "witchcraft". Given the strange, mystic, and
sometimes arcane steps that distutils and setuptools must take when building
native extensions, it only makes sense that a library that takes advantage of
various undocumented hooks might be labelled Black Magic.

[build_ext]: https://git.io/vAz6X
[cppimport]: https://github.com/tbenthompson/cppimport
[poetry]: https://poetry.eustace.io
[CMake]: https://cmake.org
