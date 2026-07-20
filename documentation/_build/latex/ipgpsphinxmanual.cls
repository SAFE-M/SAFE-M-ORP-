%% ipgpsphinxmanual.cls
%% ---------------------------------------------------------------------------
%% Classe LaTeX pour la documentation Sphinx du projet SAFE-M-ORP (IPGP).
%%
%% Basée sur `report` (contrairement à ipgplicence.cls qui charge `article` et
%% ne supporte donc pas \chapter, indispensable pour le docclass "manual" de
%% Sphinx). Reprend la charte graphique IPGP utilisée dans le diaporama Beamer
%% de soutenance (couleurs ipgpred / ipgpdark), et corrige le défaut classique
%% des classes report/book en mode "twoside" : l'insertion de pages blanches
%% avant chaque nouveau chapitre pour forcer un démarrage sur page impaire.
%%
%% Utilisation dans conf.py :
%%   latex_docclass = {'manual': 'ipgpsphinxmanual'}
%%   latex_elements = {'papersize': 'a4paper', 'pointsize': '11pt'}
%%
%% Le fichier .cls doit se trouver dans le même dossier que conf.py (ou dans
%% un chemin accessible via TEXINPUTS) pour que pdflatex/latexmk le trouve.
%% ---------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ipgpsphinxmanual}[2026/07/04 v1.0 Classe IPGP pour manuels Sphinx]

%% ---------------------------------------------------------------------------
%% Options de classe
%% - oneside par défaut : un manuel PDF lu à l'écran n'a pas besoin de pages
%%   recto/verso asymétriques. Utiliser l'option "twoside" si impression papier.
%% - openany TOUJOURS actif : c'est ce qui supprime les pages blanches. Sans
%%   cette option, `report`/`book` insèrent une page vide avant tout chapitre
%%   qui tomberait sur une page paire en mode twoside (comportement par défaut
%%   pensé pour l'impression recto/verso classique d'un livre).
%% ---------------------------------------------------------------------------
\newif\if@ipgptwoside
\@ipgptwosidefalse
\DeclareOption{twoside}{\@ipgptwosidetrue}
\DeclareOption{oneside}{\@ipgptwosidefalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

\if@ipgptwoside
  \PassOptionsToClass{twoside,openany}{report}
\else
  \PassOptionsToClass{oneside,openany}{report}
\fi

\LoadClass{report}

%% ---------------------------------------------------------------------------
%% Langue et typographie de base (repris de ipgplicence.cls)
%% ---------------------------------------------------------------------------
\RequirePackage[english,french]{babel}
\RequirePackage{iflang}
\def\frenchcontentsname{Sommaire}

\RequirePackage[T1]{fontenc}
\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{graphicx}
\RequirePackage[margin=2.5cm]{geometry}

%% ---------------------------------------------------------------------------
%% Palette IPGP (identique à celle du diaporama Beamer de soutenance)
%% ---------------------------------------------------------------------------
\RequirePackage[x11names]{xcolor}
\definecolor{ipgpred}{RGB}{163,29,45}
\definecolor{ipgpdark}{RGB}{60,20,25}

%% ---------------------------------------------------------------------------
%% Style des extraits de code (repris de ipgplicence.cls, recoloré ipgpred)
%% ---------------------------------------------------------------------------
\RequirePackage{listings}
\lstdefinestyle{ipgpstyle}{
  breakatwhitespace=false,
  commentstyle=\color{gray},
  keywordstyle=\color{ipgpred}\bfseries,
  numberstyle=\footnotesize\color{gray},
  stringstyle=\color{purple},
  identifierstyle=\color{SteelBlue4},
  basicstyle=\ttfamily\small,
  numbers=left,
  keepspaces=false,
  showspaces=false,
  showstringspaces=true,
}
\lstset{style=ipgpstyle}

\RequirePackage{booktabs}

%% ---------------------------------------------------------------------------
%% Liens hypertextes aux couleurs IPGP (au lieu du bleu par défaut)
%% ---------------------------------------------------------------------------
\RequirePackage[
  pdfstartview=FitH,
  bookmarks=true,
  bookmarksopen=true,
  breaklinks=true,
  colorlinks=true,
  linkcolor=ipgpred,anchorcolor=ipgpred,
  citecolor=ipgpred,filecolor=ipgpred,
  menucolor=ipgpred,
  urlcolor=ipgpred
]{hyperref}

\parskip 9pt plus2pt minus2pt
\parindent 0pt

%% ---------------------------------------------------------------------------
%% En-tête / pied de page façon "footline" du diaporama Beamer
%% ---------------------------------------------------------------------------
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.6pt}
\renewcommand{\footrulewidth}{0.6pt}
\renewcommand{\headrule}{{\color{ipgpred}\hrule height\headrulewidth}}
\renewcommand{\footrule}{{\color{ipgpred}\hrule height\footrulewidth}}
\fancyhead[L]{\small\itshape\color{ipgpdark}\leftmark}
\fancyhead[R]{\small\itshape\color{ipgpdark}SAFE-M-ORP}
\fancyfoot[C]{\small\color{ipgpred}\thepage}
\fancyhead[R]{\includegraphics[width=3cm]{figures/LOGO-SAFE-M.png}}

%% Page style "plain" (première page de chaque chapitre) : même identité
%% visuelle mais sans en-tête, pour ne pas répéter le titre du chapitre
%% juste en dessous de lui-même.
\fancypagestyle{plain}{%
  \fancyhf{}
  \fancyfoot[C]{\small\color{ipgpred}\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0.6pt}
  \renewcommand{\footrule}{{\color{ipgpred}\hrule height\footrulewidth}}
}

%% ---------------------------------------------------------------------------
%% Style des chapitres recoloré en rouge IPGP.
%% Placé dans \AtBeginDocument : Sphinx charge fncychap lui-même, APRES cette
%% classe, dans le préambule qu'il génère. Les macros de personnalisation
%% (\ChNameVar, \ChNumVar, \ChTitleVar) ne peuvent donc être redéfinies
%% qu'une fois fncychap réellement chargé, d'où l'usage de \AtBeginDocument
%% combiné à un test d'existence du package (compatibilité si la classe est
%% utilisée sans fncychap, par exemple pour un test hors-Sphinx).
%% ---------------------------------------------------------------------------
\AtBeginDocument{%
  \@ifpackageloaded{fncychap}{%
    \ChNameVar{\Large\sffamily\bfseries\color{ipgpred}}
    \ChNumVar{\Huge\sffamily\bfseries\color{ipgpred}}
    \ChTitleVar{\Huge\sffamily\bfseries\color{ipgpdark}}
  }{}%
}

\endinput
