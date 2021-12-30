#!/bin/bash

rsync -av --exclude-from='.rsyncignore' . aws:./webserver_django
