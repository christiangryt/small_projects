#set page(
  width: 21cm,
  height: 29.7cm,
  margin: 0.5cm
)

#show link: underline
#show link: set text(fill: blue)

#let component(sted, beskrivelse, periode, rolle: none) = {
  eval(sted, mode: "markup")
  h(0.5em)

  if rolle != none {
    eval(rolle, mode: "markup")
  }

  v(-0.7em)
  grid(
    columns: (1fr, auto),
    gutter: 2%,

    eval(beskrivelse, mode: "markup"),
    eval(periode, mode: "markup"),
  )
}

#let title_thing(title) = {
  heading(level: 2, title)
  line(length:100%)
}

// Her kan jeg sikkert gjøre en forenkling hvor jeg bare looper over det jeg har
// Av typer kwargs om jeg gidder
#let personalia(
  navn,
  addresse_gate,
  addresse_by,
  email,
  nummer,
  studentadresse_gate,
  studentadresse_by,
  kontakt,
  studentadresse
) = {

  align(center, {
    set text(size: 20pt)
    eval(navn, mode: "markup")
    v(-0.5em)
  })

  grid(
    columns: 2,
    gutter: 1fr,

    {figure(
      image("CV-bilde-2025_circle_crop.png", width: 50%),
    )},

    {align(horizon, {
      set grid(
        columns: (1fr, auto),
        gutter: 10%,
      )

      heading(level: 2)[#kontakt]

      grid(
        {
          addresse_gate
          linebreak()
          addresse_by
        },

        {
          email
          linebreak()
          text(style: "italic")[#nummer]
        }
      )

      heading(level: 2)[#studentadresse]

      studentadresse_gate
      linebreak()
      studentadresse_by

      heading(level: 2)[Github]
      link("https://github.com/christiangryt/small_projects")[Small Projects]
    })}
  )
}

#let cv = json("cv.json")
//#let cv = json("cv-eng.json")
#let info = cv.personalia

#personalia(
  info.name,
  info.addresse_gate,
  info.addresse_by,
  info.email,
  info.phone,
  info.studentaddresse_gate,
  info.studentaddresse_by,
  info.kontakt,
  info.studentaddresse
)

#for section in cv.sections {

  title_thing(section.name)

  if type(section.items) == array {
    for entry in section.items {
      component(
        entry.place,
        entry.description,
        entry.period,
        rolle: entry.role,
      )
    }
  }
  else {
    section.items
  }
}
