# Conan package of Breakpad
[ ![Download](https://api.bintray.com/packages/arsen-studio/arsen-deps/breakpad%3Aarsen-studio/images/download.svg) ](https://bintray.com/arsen-studio/arsen-deps/breakpad%3Aarsen-studio/_latestVersion)

|Linux|Windows|OS X|
|-----|-------|----|
|[![pipeline status](https://gitlab.com/HeiGameStudio/ArsenEngine/dependencies/conan-breakpad/badges/stable/20181304/pipeline.svg)](https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad/commits/master)|[![Build status](https://ci.appveyor.com/api/projects/status/wajbow75kdy6f493/branch/stable/20181304?svg=true)](https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad/commits/master)|[![Build Status](https://travis-ci.org/ArsenStudio/conan-breakpad.svg?branch=stable%2F20181304)](https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad/commits/master)|

[Conan.io](https://conan.io) package for [Breakpad](https://chromium.googlesource.com/breakpad/breakpad/) library. This package includes main library and utilities.

The packages generated with this **conanfile** can be found in [bintray.com](https://bintray.com/arsen-studio/arsen-deps/breakpad%3Aarsen-studio).

## Setup
To configure Conan client to work with Arsen packages, you will need to add repository to the list of remotes. To add repository, use the following command: 
```
conan remote add arsen-deps https://api.bintray.com/conan/arsen-studio/arsen-deps 
```

### Basic

```
$ conan install breakpad/latest@arsen-studio/stable
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

```
[requires]
breakpad/latest@arsen-studio/stable

[options]
breakpad:shared=true # false

[generators]
txt
cmake
```

Complete the installation of requirements for your project running:

```
conan install .
```

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## Develop the package

### Build packages

    $ pip install conan_package_tools bincrafters_package_tools
    $ python build.py

### Upload packages to server

    $ conan upload breakpad/latest@arsen-studio/stable --all

## Issues

If you wish to report an issue, please do so here:

https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad/issues

For any pull or merge request, please do so here:

https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad/merge_requests


## License

[MIT LICENSE](LICENSE)