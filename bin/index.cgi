#!/bin/bash -euxv

source "$(dirname $0)/conf"

# ログ出力
exec 2> "${log_dir}/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"

#dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${QUERY_STRING} | sed 's;=;s/;')"
#md="${contents_dir}/${dir}/main.md"
md="${contents_dir}/posts/template/main.md"

# 出力
pandoc --template="${view_dir}/template.html" -f markdown_github+yaml_metadata_block "$md"


