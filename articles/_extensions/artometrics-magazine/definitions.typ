// Artometrics magazine helpers. Included into the Typst document (a Pandoc
// template): write $$ wherever a literal dollar sign is required.

#let red = rgb("#E60000")
#let blue = rgb("#0047FF")
#let blue-glow = rgb("#4D8DFF")
#let ink = rgb("#141414")
#let paper = rgb("#FFFFFF")
#let night = rgb("#0A0A0A")
#let muted = rgb("#4A4A4A")

#let anaglyph(body, size: 78pt) = context {
  let sample = text(font: "DM Mono", size: size, fill: white, body)
  let sz = measure(sample)
  box(width: sz.width + 8pt, height: sz.height + 2pt)[
    #place(dx: 0pt, dy: 0.6pt, text(font: "DM Mono", size: size, fill: red, body))
    #place(dx: 4.5pt, dy: 0.6pt, text(font: "DM Mono", size: size, fill: blue-glow, body))
    #place(dx: 2.1pt, dy: 0pt, text(font: "DM Mono", size: size, fill: white, body))
  ]
}

#let rules() = {
  v(8pt)
  line(length: 100%, stroke: 2.2pt + red)
  v(3pt)
  line(length: 100%, stroke: 1.4pt + blue-glow)
  v(10pt)
}

#let magazine-cover(
  title: [],
  dek: [],
  issue: "01",
  kicker: [],
  stat: [],
  stat-label: [],
  stat-detail: [],
  byline: [],
) = {
  set page(
    paper: "us-letter",
    margin: (x: 0.68in, y: 0.58in),
    fill: night,
    header: none,
    footer: none,
    numbering: none,
  )
  set text(fill: white, font: "DM Sans")
  set par(justify: false, leading: 0.62em)
  block(width: 100%, height: 100%)[
    #grid(
      rows: (auto, 1fr, auto),
      [
        #text(font: "Chomsky", size: 54pt, fill: white)[Artometrics]
        #rules()
        #grid(columns: (auto, 1fr), column-gutter: 14pt)[
          #text(font: "DM Mono", size: 11pt, fill: blue-glow, tracking: 0.12em)[ISSUE #issue]
        ][
          #align(right)[#text(font: "DM Sans", size: 11pt, fill: white, tracking: 0.08em)[#kicker]]
        ]
      ],
      align(bottom)[
        #text(font: "DM Sans", weight: "bold", size: 32pt, fill: white, tracking: -0.02em)[#title]
        #v(12pt)
        #block(width: 92%)[
          #set text(size: 12.5pt, fill: rgb("#E4E4E4"))
          #dek
        ]
      ],
      [
        #anaglyph(stat, size: 64pt)
        #v(8pt)
        #text(font: "DM Sans", size: 11pt, fill: white)[#stat-label]
        #linebreak()
        #text(font: "DM Mono", size: 12pt, fill: blue-glow)[#stat-detail]
        #v(12pt)
        #text(font: "DM Mono", size: 8.5pt, fill: rgb("#BDBDBD"))[#byline]
      ],
    )
  ]
}

#let magazine-contents(dek: [], byline: []) = {
  text(font: "DM Sans", weight: "bold", size: 28pt)[Contents]
  v(8pt)
  block(width: 92%)[
    #set text(size: 11pt, fill: rgb("#333333"))
    #dek
  ]
  v(4pt)
  text(font: "DM Mono", size: 8.5pt, fill: blue)[#byline]
  v(16pt)
  context {
    let heads = query(heading.where(level: 2))
    for h in heads {
      if h.outlined == false { continue }
      let num = counter(page).at(h.location()).first()
      link(h.location())[
        #grid(columns: (1fr, 1.5em), column-gutter: 10pt)[
          #text(font: "DM Sans", size: 11pt, fill: ink)[#h.body]
        ][
          #align(right, text(font: "DM Mono", size: 10pt, fill: blue)[#str(num)])
        ]
      ]
      v(2pt)
      line(length: 100%, stroke: 0.4pt + rgb("#E6E6E6"))
      v(6pt)
    }
  }
}

#let magazine-back(url: [], issue: "01", running: [], dek: []) = {
  pagebreak(weak: true)
  set page(
    paper: "us-letter",
    margin: (x: 0.7in, y: 0.62in),
    fill: night,
    header: none,
    footer: none,
    numbering: none,
  )
  set text(fill: white, font: "DM Sans")
  set par(justify: false)
  v(2.4in)
  text(font: "Chomsky", size: 48pt)[Artometrics]
  rules()
  text(font: "DM Mono", size: 11pt, fill: blue-glow, tracking: 0.14em)[ISSUE #issue  ·  #running]
  v(16pt)
  text(font: "DM Sans", weight: "bold", size: 20pt)[#dek]
  v(1.6in)
  text(font: "DM Mono", size: 16pt, fill: white)[#url]
  v(8pt)
  text(size: 9.5pt, fill: rgb("#C8C8C8"))[The figures in this issue are the figures on the site.]
}

#let lede(body) = block(width: 100%, above: 4pt, below: 10pt)[
  #set text(size: 12.25pt)
  #set par(leading: 0.72em)
  #body
]

#let credit(body) = block(above: 1pt, below: 7pt)[
  #set text(font: "DM Sans", size: 7.5pt, style: "italic", fill: muted)
  #set par(justify: false, leading: 0.42em, spacing: 0.25em)
  #body
]

#let logo(body) = block(below: 8pt, breakable: false)[
  #set image(width: 1.2in)
  #body
]

#let person(body) = block(below: 8pt, breakable: false)[
  #set image(width: 1.12in)
  #body
]

#let studiocard(body) = block(
  width: 100%,
  inset: (x: 8pt, y: 8pt),
  breakable: true,
  fill: rgb("#F7F7F7"),
  stroke: (left: 2.6pt + red),
)[
  #set par(justify: false)
  #body
]

#let card(stat, body) = block(
  width: 100%,
  inset: (x: 12pt, y: 9pt),
  breakable: false,
  fill: white,
  stroke: (left: 3pt + red, rest: 0.4pt + rgb("#E6E6E6")),
  above: 7pt,
)[
  #grid(
    columns: (1.35in, 1fr),
    column-gutter: 12pt,
    align: (left + horizon, left + horizon),
    text(font: "DM Mono", size: 20pt, fill: blue)[#stat],
    body,
  )
]

#let sidebox(kicker, body) = block(
  width: 100%,
  inset: 11pt,
  breakable: false,
  fill: rgb("#F3F6FF"),
  stroke: (left: 3pt + blue),
  above: 8pt,
  below: 8pt,
)[
  #text(font: "DM Mono", size: 8pt, fill: red, tracking: 0.08em)[#kicker]
  #v(5pt)
  #body
]

#let pull(body) = block(
  width: 100%,
  inset: (left: 12pt, right: 6pt, y: 8pt),
  breakable: false,
  stroke: (left: 3.5pt + red),
  above: 10pt,
  below: 10pt,
)[
  #body
]

#let spread(copy, side) = block(width: 100%, above: 6pt, below: 8pt)[
  #grid(columns: (1.42fr, 0.82fr), column-gutter: 0.24in, copy, side)
]

#let checksum(body) = block(width: 100%, inset: 12pt, fill: night, above: 8pt, below: 8pt)[
  #set text(font: "DM Mono", size: 8.5pt, fill: white)
  #set par(justify: false, leading: 0.55em)
  #body
]

#let versions(body) = block(
  width: 100%,
  inset: 10pt,
  fill: rgb("#F6F6F6"),
  stroke: (left: 2.5pt + blue),
  above: 8pt,
)[
  #set text(font: "DM Mono", size: 7.5pt)
  #set par(justify: false, leading: 0.45em)
  #show raw.where(block: true): it => {
    set text(font: "DM Mono", size: 7pt)
    block(width: 100%, breakable: true)[
      #for row in it.text.split("\n") {
        row
        linebreak()
      }
    ]
  }
  #body
]

#let editorsnote(body) = block(
  width: 100%,
  inset: (x: 2pt, y: 10pt),
  stroke: (top: 1.6pt + red),
  above: 12pt,
)[
  #set text(style: "italic", size: 9.5pt)
  #body
]

#let titlecard(body) = block(
  width: 100%,
  inset: 8pt,
  breakable: false,
  stroke: (top: 2pt + red),
  fill: rgb("#FAFAFA"),
)[
  #set par(justify: false)
  #set text(size: 9pt)
  #body
]
