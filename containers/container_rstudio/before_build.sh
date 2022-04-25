#!/usr/bin/env bash

cd ../../projects

BUILDDIR=../containers/container_rstudio/

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

for DIR in project*
do
    mkdir -p $BUILDDIR/$DIR

    check_and_update $DIR/R_requirements.R $BUILDDIR/$DIR/R_requirements.R
    check_and_update $DIR/environment.yml $BUILDDIR/$DIR/environment.yml
done
