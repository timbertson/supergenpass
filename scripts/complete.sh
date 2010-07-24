#!/bin/bash

function _supergenpass {
	local cur opts cmd
	cmd=supergenpass
	cmd=p
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	if [[ ${cur} == -* ]] ; then
		opts=`$cmd --help | grep -oe ' -[-_[:alnum:]]+'`
	else
		opts=`$cmd --domains`
	fi

	COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
	return 0
}

#example usage:
complete -F _supergenpass supergenpass
complete -F _supergenpass p
