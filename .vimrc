syntax on
set tabstop=4
set number
set relativenumber
set statusline=%m%f
set laststatus=2
highlight LineNr ctermfg=darkgrey

nnoremap tn :tabnew<Space>
nnoremap tk :tabnext<CR>
nnoremap tj :tabprev<CR>
nnoremap th :tabfirst<CR>
nnoremap tl :tablast<CR>

" --------- Plugins ----------
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')

" surround.vim (https://vimawesome.com/plugin/surround-vim)
Plug 'tpope/vim-surround'


" supertab (https://vimawesome.com/plugin/supertab)
Plug 'ervandew/supertab'

" Initialize plugin system
call plug#end()

