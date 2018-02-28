#!/usr/bin/env bash
# Install Dakota and its dependencies.

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    base_url="https://csdms.colorado.edu/pub/tools/dakota"
    dakota_filename="dakota-6.4.0.Linux-Ubuntu.x86_64.tar.gz"
    deb_filename="libicu48_4.8.1.1-12+deb7u3_amd64.deb"
    wget $base_url/$deb_filename
    sudo apt-get install libblas-dev liblapack3
    sudo dpkg --install $deb_filename
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    base_url="https://dakota.sandia.gov/sites/default/files/distributions/public"
    dakota_filename="dakota-6.4-public-Darwin.i386.tar.gz"
fi

wget $base_url/$dakota_filename -O dakota.tar.gz

dakota_dir=$HOME/dakota-sandia
mkdir $dakota_dir && tar zxf dakota.tar.gz -C $dakota_dir --strip-components 1

export PATH="$dakota_dir/bin:$dakota_dir/test:$PATH"

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    export DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$dakota_dir/bin:$dakota_dir/lib"
else
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$dakota_dir/bin:$dakota_dir/lib"
fi
