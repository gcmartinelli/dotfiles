#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
#PS1='[\u@\h \W]\$ '
PS1="\[\e[0;34m\]\u@\h \[\e[m\e[1;37m\]\W\[\e[m\]> "  
#neofetch
alias config='/usr/bin/git --git-dir=$HOME/dotfiles --work-tree=$HOME'
