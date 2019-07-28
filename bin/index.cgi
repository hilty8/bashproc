#!/bin/bash -euxv

source "$(dirname $0)/conf"
exec 2> "${log_dir}/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
set -o pipefail

trap 'rm -f $tmp-*' EXIT

### VARIABLES ###
tmp=/tmp/$$
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')" # 例: post=title -> posts/title
md="${contents_dir}/${dir}/main.md"
[ -f "$md" ]

### MAKE METADATA ###
cat << FIN > $tmp-meta.yaml
---
created_time:  '$(date -f - < "${data_dir}/$dir/created_time")'
modified_time: '$(date -f - < "${data_dir}/$dir/modified_time")'
title:         '$(cat "${data_dir}/$dir/title")'
nav:           '$(cat "${data_dir}/$dir/nav")'
---
FIN

### OUTPUT ###
pandoc --template="${view_dir}/template.html" \
	-f markdown_github+yaml_metadata_block "$md" "$tmp-meta.yaml" |
	sed -r "/:\/\/|=\"\//!s;<(img src|a href)=\";&/$dir/;" |
	sed "s;/$dir/#;#;g"


