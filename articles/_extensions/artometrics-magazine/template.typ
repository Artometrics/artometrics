// Pandoc template for the Artometrics magazine PDF.
// This file replaces Quarto's Typst template, so it must emit the body.
// A literal dollar sign in Typst source has to be written as a doubled dollar.

#let horizontalrule = line(start: (25%, 0%), end: (75%, 0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
    ])
    .join()
}

$for(header-includes)$
$header-includes$

$endfor$

#set document(
  title: "$title$",
  author: ("$author$",),
)

#set text(lang: "en", region: "US", font: "DM Sans", size: 10.5pt, fill: rgb("#141414"), hyphenate: true)
#set par(justify: true, leading: 0.68em, spacing: 0.72em)
#set heading(numbering: none)
#set list(indent: 0.4em, body-indent: 0.35em)
#show strong: set text(weight: "bold")
#show emph: set text(style: "italic")
#show raw: set text(font: "DM Mono", size: 8.5pt)
#show regex("\\d[\\d,]*\\.?\\d*%?"): set text(font: "DM Mono")
#show link: it => {
  set text(fill: rgb("#0047FF"))
  show regex("[/\\-_#?&=]"): token => token + sym.zws
  it
}

#show heading.where(level: 2): it => block(width: 100%, above: 1.05em, below: 0.45em, breakable: false)[
  #set par(justify: false)
  #text(font: "DM Sans", weight: "bold", size: 16.5pt, fill: rgb("#141414"))[#it.body]
  #v(3pt)
  #line(length: 100%, stroke: 0.7pt + rgb("#4D8DFF"))
  #v(-6.2pt)
  #line(length: 1.7in, stroke: 2.3pt + rgb("#E60000"))
]
#show heading.where(level: 3): it => block(above: 0.85em, below: 0.28em, breakable: false)[
  #set par(justify: false)
  #text(font: "DM Sans", weight: "bold", size: 12pt)[#it.body]
]

#set figure(gap: 7pt)
#show figure.caption: set text(size: 8.5pt, fill: rgb("#222222"))
#show figure.where(kind: image): set block(breakable: false)
#show figure.where(kind: table): it => block(width: 100%, breakable: true, it.body)
#show image: set block(breakable: false)
#set table(
  inset: (x: 3.5pt, y: 3.2pt),
  stroke: (x: none, y: 0.3pt + rgb("#E4E4E4")),
  fill: (_, y) => if y == 0 { rgb("#111111") },
)
#show table: set text(size: 7.4pt)
#show table.cell.where(y: 0): set text(fill: white, weight: "bold", size: 7.2pt)

#set page(
  paper: "us-letter",
  margin: (top: 0.72in, bottom: 0.58in, left: 0.62in, right: 0.62in),
  numbering: "1",
  header: none,
  footer: none,
)

$body$

$for(include-after)$
$include-after$

$endfor$
