#!/usr/bin/env bash

cd ../../projects

BUILDDIR=../containers/container_gpu/

check_and_update () {
    ORIGFILE=$1
    BUILDFILE=$2
    if [ ! -f $BUILDFILE ]
    then 
      cp $ORIGFILE $BUILDFILE
    fi

    diff -q $ORIGFILE $BUILDFILE
    
    if [ $? != 0 ]
    then
      echo "updating file in $DIR"
      cp $ORIGFILE $BUILDFILE
    else
      echo "no need to update file in $DIR"
    fi
}

DIR=project2
mkdir -p $BUILDDIR/$DIR

check_and_update $DIR/environment.yml $BUILDDIR/$DIR/environment.yml
