* Shared paths. Run at the top of every do-file:  do "code/stata/paths.do"
* Assumes Stata's working directory is the repo root.

global root     "`c(pwd)'"
global clean    "$root/data/clean"
global tables   "$root/output/tables"
global figures  "$root/output/figures"

* Overleaf project in the local Dropbox folder. Write final tables/figures here directly, e.g.
*   esttab using "$ov_tables/tab1.tex", replace
global overleaf   "`: env USERPROFILE'/Dropbox/Apps/Overleaf/[OVERLEAF PROJECT]"
global ov_tables  "$overleaf/[TABLES SUBFOLDER]"
global ov_figures "$overleaf/[FIGURES SUBFOLDER]"
