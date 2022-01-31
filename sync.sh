#!/bin/bash

rsync -av --delete --exclude-from='.rsyncignore' . aws:./webserver_django
