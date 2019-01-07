# General Setup Instructions for pi development
* Put this code in $(HOME)/.bashrc 
  ```
  bashdir=$HOME/bashrc.d
  for f in `ls $bashdir`; do
    source $bashdir/$f
  done
  ```
* `cd $HOME`
* `ln -s $HOME/GitProjects/iAltar/setup/bashrc.d`
