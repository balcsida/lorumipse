#!/bin/bash -x

script_dir=$(dirname $0)
root_dir=$script_dir/..
gunicorn -w 4 -b 0.0.0.0:9999 webapp.server:app
