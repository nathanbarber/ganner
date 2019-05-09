#!/bin/bash 

log () {
    echo "GEN ==> $1"
}

log "Transferring uploaded images to compute/.source"
touch compute/.source/foo
rm compute/.source/*
cp uploaded/$1/* compute/.source

log "Initiating -> Generative Adversarial Network"


log "Done - Exiting"