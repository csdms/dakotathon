#!/usr/bin/env bash

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    base_url="https://dakota.sandia.gov/sites/default/files/distributions/public"
    filename="dakota-6.4-public-Darwin.i386.tar.gz"
else
    base_url="http://csdms.colorado.edu/pub/tools/dakota"
    filename="dakota-6.4.0.Linux-Ubuntu.x86_64.tar.gz"
fi

wget $base_url/$filename -O dakota.tar.gz

dakota_dir=$HOME/dakota
mkdir $dakota_dir && tar zxf dakota.tar.gz -C $dakota_dir --strip-components 1

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo apt-get install libblas-dev liblapack-dev g++ gfortran fort77 libtrilinos-dev
fi

export PATH="$dakota_dir/bin:$dakota_dir/test:$PATH"

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    export DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$dakota_dir/bin:$dakota_dir/lib"
else
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$dakota_dir/bin:$dakota_dir/lib"
fi
