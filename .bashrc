#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Decorations
alias ls='ls --color=auto'
PS1="\[\e[0;34m\]\u@\h \[\e[m\e[1;37m\]\W\[\e[m\]> "

# Load aliases
if [ -f $HOME/.bash_aliases ]; then
	. $HOME/.bash_aliases
fi
