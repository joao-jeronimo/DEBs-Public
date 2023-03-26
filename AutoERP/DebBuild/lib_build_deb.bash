
rsynch_full_path() {
    export src="$1"
    export dst="$2"
    
    # Calculate the destination filepath so that we can mkdir it:
    export dstdir="`dirname $dst`"
    # Mksure the dir exists:
    mkdir -p "$dstdir"
    # Rsync asked stuff:
    rsync -rlt --delete --itemize-changes -Rv "$src" "$dst"
}
