_matrix-commander-get-last-option ()
{
    local lastopt i

    for (( i = ${#COMP_WORDS[@]} - 1; i >= 0; i-- )); do
        if [[ "${COMP_WORDS[i]}" = -* ]]; then
            lastopt="${COMP_WORDS[i]}"
            break
        fi
    done

    echo $lastopt
}

_matrix-commander ()
{
    COMPREPLY=()
    local IFS=$'\n'
    local -a opts keys
    cur=${COMP_WORDS[COMP_CWORD]}

    # prev is generally not useful since nargs=+
    prev=${COMP_WORDS[COMP_CWORD-1]}
    opts=(
        -h --help
        -d --debug
        --log-level
        -c --credentials
        -r --room
        --room-create
        --room-join
        --room-leave
        --room-forget
        --room-invite
        --room-ban
        --room-unban
        --room-kick
        --user
        --name
        --topic
        -m --message
        -i --image
        -a --audio
        -f --file
        -w --html
        -z --markdown
        -k --code
        -p --split
        -j --config
        --proxy
        -n --notice
        -e --encrypted
        -s --store
        -l --listen
        -t --tail
        -y --listen-self
        --print-event-id
        -u --download-media
        -o --os-notify
        -v --verify
        -x --rename-device
        --version
    )
    # option
    if [[ "$cur" = -* ]]; then
        COMPREPLY=( $(compgen -W "${opts[*]}" -- "$cur") )
        return 0
    fi

    # argument to option
    opt=$(_matrix-commander-get-last-option)

    case "$opt" in
        --log-level)
            keys=(DEBUG INFO WARNING ERROR CRITICAL)
            COMPREPLY=( $(compgen -W "${keys[*]}" -- "$cur") )
            ;;
        -c|--credentials)
            COMPREPLY=( $(compgen -f -- "$cur") )
            ;;
        -i|--image|-a|--audio|-f|--file)
            # just allow all files since it is hard to distinguish
            COMPREPLY=( $(compgen -f -- "$cur") )
            ;;
        -s|--store)
            COMPREPLY=( $(compgen -d -- "$cur") )
            ;;
        -l|--listen)
            keys=(never once forever tail all)
            COMPREPLY=( $(compgen -W "${keys[*]}" -- "$cur") )
            ;;
        -j|--config)
            COMPREPLY=( $(compgen -f -- "$cur") )
            ;;
        -v|--verify)
            keys=(emoji)
            COMPREPLY=( $(compgen -W "${keys[*]}" -- "$cur") )
            ;;
        *)
            return 1
            ;;
    esac
}

complete -F _matrix-commander matrix-commander.py
