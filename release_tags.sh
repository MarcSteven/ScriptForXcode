“#!/bin/sh
VERSION=`grep VERSION setup.py | head -1 | sed 's/.*"\(.*\)".*/\1/'`
git tag $VERSION
git push origin $VERSION”

Excerpt From: Akos Hochrein. “Designing Microservices with Django.” Apple Books. 
