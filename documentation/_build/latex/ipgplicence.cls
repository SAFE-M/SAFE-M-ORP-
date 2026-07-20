%% ipgplicence.cls - Version 1 - Mai 2020 - FM, AF et GM

\NeedsTeXFormat{LaTeX2e} 
\ProvidesPackage{ipgplicence}

\RequirePackage[english,french]{babel} % Last language, language by default
\RequirePackage{iflang}
\def\frenchcontentsname{Sommaire}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt,twoside]{article}

\RequirePackage[utf8x]{inputenc}
\RequirePackage[T1]{fontenc}

\RequirePackage{amsmath,amsfonts,amssymb}
\RequirePackage{graphicx}
\RequirePackage[margin=2cm]{geometry}
\RequirePackage{listings}
\lstdefinestyle{mystyle}{
breakatwhitespace=false,
    commentstyle=\color{gray},
    keywordstyle=\color{Green4},
    numberstyle=\footnotesize\color{gray},
    stringstyle=\color{purple},
    identifierstyle=\color{SteelBlue4},
    basicstyle=\ttfamily\small,
    numbers=left,
    keepspaces=false,                 
    numbers=left,                           
    showspaces=false,                
    showstringspaces=true,
    }
\lstset{style=mystyle}

\RequirePackage[x11names]{xcolor}
\RequirePackage{booktabs}


\RequirePackage[%
 pdfstartview=FitH,%
 bookmarks=true,%
 bookmarksopen=true,%
 breaklinks=true,%
 colorlinks=true,%
 linkcolor=blue,anchorcolor=blue,%
 citecolor=blue,filecolor=blue,%
 menucolor=blue,%
 urlcolor=blue]{hyperref}
 
 \parskip 9pt plus2pt minus2pt
 \parindent 0pt