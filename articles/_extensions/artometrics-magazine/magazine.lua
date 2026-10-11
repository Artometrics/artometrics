-- Artometrics magazine furniture. The article .qmd stays the source of the
-- words and figures. This filter adds the cover, contents, running header,
-- and back cover, and turns classed divs into Typst or HTML layout.

local function is_typst()
  return FORMAT == "typst"
end

local function is_html()
  return FORMAT == "html" or FORMAT == "html5"
end

local function meta_str(meta, ...)
  local value = meta
  for _, key in ipairs({ ... }) do
    if type(value) ~= "table" then
      return ""
    end
    value = value[key]
    if value == nil then
      return ""
    end
  end
  return pandoc.utils.stringify(value)
end

local function html_escape(s)
  return (s
    :gsub("&", "&amp;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;")
    :gsub('"', "&quot;"))
end

local function typst_escape(s)
  s = s:gsub("\\", "\\\\")
  s = s:gsub("([#$*_`@<>%[%]])", "\\%1")
  return s
end

local function has_class(el, name)
  return el.classes and el.classes:includes(name)
end

local function to_typst(blocks)
  if #blocks == 0 then
    return ""
  end
  return pandoc.write(pandoc.Pandoc(blocks), "typst")
end

local MONTHS = {
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
}

local function format_date(s)
  local y, m, d = s:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)")
  if not y then
    return s
  end
  return string.format("%d %s %s", tonumber(d), MONTHS[tonumber(m)] or m, y)
end

local function magazine_fields(meta)
  local mag = meta.magazine or {}
  local title = meta_str(meta, "title")
  local description = meta_str(meta, "description")
  local author = meta_str(meta, "author")
  local date = format_date(meta_str(meta, "date"))
  return {
    title = title,
    description = description,
    author = author,
    date = date,
    issue = meta_str(mag, "issue"),
    kicker = meta_str(mag, "kicker"),
    running = meta_str(mag, "running"),
    stat = meta_str(mag, "hero-stat"),
    stat_label = meta_str(mag, "hero-label"),
    stat_detail = meta_str(mag, "hero-detail"),
    url = meta_str(mag, "url"),
  }
end

local BREAKER = {
  ["chart-page"] = true,
  ["spread"] = true,
  ["pullquote"] = true,
  ["exec-summary"] = true,
  ["sidebox"] = true,
  ["checksum"] = true,
  ["versions"] = true,
  ["editors-note"] = true,
  ["title-cards"] = true,
  ["single"] = true,
  ["studio-card"] = true,
  ["lede"] = true,
  ["logo"] = true,
  ["person"] = true,
  ["cover"] = true,
  ["contents"] = true,
  ["back-cover"] = true,
  ["cards"] = true,
}

local function is_flow(block)
  local t = block.t
  if t == "Para" or t == "Plain" or t == "BulletList" or t == "OrderedList"
    or t == "BlockQuote" or t == "LineBlock" then
    return true
  end
  if t == "Header" and block.level >= 3 then
    return true
  end
  if t == "Div" then
    for _, class in ipairs(block.classes) do
      if BREAKER[class] then
        return false
      end
    end
    return true
  end
  return false
end

local function flow_length(blocks)
  local n = 0
  for _, block in ipairs(blocks) do
    n = n + #pandoc.utils.stringify(block)
  end
  return n
end

local function group_columns(blocks)
  local out = pandoc.List()
  local flow = pandoc.List()

  local function flush()
    if #flow == 0 then
      return
    end
    local length = flow_length(flow)
    if is_typst() then
      local written = to_typst(flow)
      if length >= 340 or #flow >= 2 then
        out:insert(pandoc.RawBlock("typst", "#columns(2, gutter: 0.28in)[\n" .. written .. "\n]"))
      elseif written:match("%S") then
        out:insert(pandoc.RawBlock("typst", written))
      end
    elseif length >= 340 or #flow >= 2 then
      out:insert(pandoc.RawBlock("html", '<div class="cols">'))
      for _, block in ipairs(flow) do
        out:insert(block)
      end
      out:insert(pandoc.RawBlock("html", "</div>"))
    else
      for _, block in ipairs(flow) do
        out:insert(block)
      end
    end
    flow = pandoc.List()
  end

  for _, block in ipairs(blocks) do
    if is_flow(block) then
      flow:insert(block)
    else
      flush()
      out:insert(block)
    end
  end
  flush()
  return out
end

local function collect_h2(blocks, acc)
  for _, block in ipairs(blocks) do
    if block.t == "Header" and block.level == 2 and not has_class(block, "unlisted") then
      table.insert(acc, block)
    elseif block.t == "Div" and block.content then
      collect_h2(block.content, acc)
    elseif block.t == "BlockQuote" or block.t == "BulletList" or block.t == "OrderedList" then
      -- headings are not nested in these for this magazine
    end
  end
end

local function typst_front(fields)
  local byline = typst_escape(fields.author .. "  ·  " .. fields.date .. "  ·  " .. fields.kicker)
  local cover = table.concat({
    "#magazine-cover(",
    "  title: [" .. typst_escape(fields.title) .. "],",
    "  dek: [" .. typst_escape(fields.description) .. "],",
    "  issue: [" .. typst_escape(fields.issue) .. "],",
    "  kicker: [" .. typst_escape(fields.kicker) .. "],",
    "  stat: [" .. typst_escape(fields.stat) .. "],",
    "  stat-label: [" .. typst_escape(fields.stat_label) .. "],",
    "  stat-detail: [" .. typst_escape(fields.stat_detail) .. "],",
    "  byline: [" .. byline .. "],",
    ")",
    "#pagebreak()",
    "#set page(",
    "  paper: \"us-letter\",",
    "  margin: (top: 0.74in, bottom: 0.58in, left: 0.62in, right: 0.62in),",
    "  fill: white,",
    "  numbering: \"1\",",
    "  header: context {",
    "    set text(size: 8pt)",
    "    grid(columns: (1fr, 1fr),",
    "      text(font: \"DM Sans\", weight: \"bold\", fill: rgb(\"#E60000\"), tracking: 0.14em)[ARTOMETRICS],",
    "      align(right, text(font: \"DM Mono\", fill: rgb(\"#0047FF\"))[ISSUE "
      .. typst_escape(fields.issue) .. "  ·  " .. typst_escape(fields.running) .. "])",
    "    )",
    "  },",
    "  footer: context {",
    "    set text(size: 8pt, font: \"DM Mono\")",
    "    grid(columns: (1fr, auto),",
    "      text(fill: rgb(\"#333333\"))[" .. typst_escape(fields.url:gsub("https://", "")) .. "],",
    "      text(fill: rgb(\"#141414\"))[#counter(page).display()]",
    "    )",
    "  },",
    ")",
    "#counter(page).update(1)",
    "#magazine-contents(",
    "  dek: [" .. typst_escape(fields.description) .. "],",
    "  byline: [" .. byline .. "],",
    ")",
  }, "\n")
  local back = table.concat({
    "#magazine-back(",
    "  url: [" .. typst_escape(fields.url) .. "],",
    "  issue: [" .. typst_escape(fields.issue) .. "],",
    "  running: [" .. typst_escape(fields.running) .. "],",
    "  dek: [" .. typst_escape(fields.title) .. "],",
    ")",
  }, "\n")
  return cover, back
end

local function html_front(fields, blocks)
  local heads = {}
  collect_h2(blocks, heads)
  local items = {}
  for _, heading in ipairs(heads) do
    local id = heading.identifier or ""
    local text = html_escape(pandoc.utils.stringify(heading))
    if id ~= "" then
      table.insert(items, '<li><a href="#' .. html_escape(id) .. '"><span>' .. text .. "</span></a></li>")
    end
  end
  local url_label = html_escape(fields.url:gsub("https://", ""))
  local cover = table.concat({
    '<span class="running-url">' .. url_label .. "</span>",
    '<section class="cover">',
    '<p class="wordmark">Artometrics</p>',
    '<div class="rules"></div>',
    '<p class="issue-row"><span class="issue-no">ISSUE ' .. html_escape(fields.issue) .. '</span>',
    '<span class="kicker">' .. html_escape(fields.kicker) .. "</span></p>",
    '<h1 class="cover-title">' .. html_escape(fields.title) .. "</h1>",
    '<p class="dek">' .. html_escape(fields.description) .. "</p>",
    '<p class="hero-stat">' .. html_escape(fields.stat) .. "</p>",
    '<p class="hero-label">' .. html_escape(fields.stat_label) .. "</p>",
    '<p class="hero-detail">' .. html_escape(fields.stat_detail) .. "</p>",
    '<p class="byline">' .. html_escape(fields.author) .. " · " .. html_escape(fields.date) .. "</p>",
    "</section>",
    '<nav class="contents">',
    "<p class=\"contents-title\">Contents</p>",
    '<p class="dek">' .. html_escape(fields.description) .. "</p>",
    '<p class="byline">' .. html_escape(fields.author) .. " · " .. html_escape(fields.date) .. " · " .. html_escape(fields.kicker) .. "</p>",
    "<ol>",
    table.concat(items, "\n"),
    "</ol>",
    "</nav>",
  }, "\n")
  local back = table.concat({
    '<section class="back-cover">',
    '<p class="wordmark">Artometrics</p>',
    '<div class="rules"></div>',
    '<p class="issue-no">ISSUE ' .. html_escape(fields.issue) .. " · " .. html_escape(fields.running) .. "</p>",
    '<p class="back-title">' .. html_escape(fields.title) .. "</p>",
    '<p class="back-url">' .. html_escape(fields.url) .. "</p>",
    '<p class="back-note">The figures in this issue are the figures on the site.</p>',
    "</section>",
  }, "\n")
  return cover, back
end

local function wrap_typst(name, blocks)
  return pandoc.RawBlock("typst", "#" .. name .. "[\n" .. to_typst(blocks) .. "\n]")
end

function Div(div)
  if not is_typst() then
    return nil
  end
  -- Parents read these divs themselves.
  if has_class(div, "stat") or has_class(div, "kicker") or has_class(div, "cards")
    or has_class(div, "copy") or has_class(div, "side") or has_class(div, "title-card") then
    return nil
  end

  if has_class(div, "card") then
    local stat = ""
    local rest = pandoc.List()
    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child, "stat") then
        stat = pandoc.utils.stringify(child)
      else
        rest:insert(child)
      end
    end
    return pandoc.RawBlock("typst", "#card[" .. typst_escape(stat) .. "][\n" .. to_typst(rest) .. "\n]")
  end

  if has_class(div, "pullquote") then
    local stat = ""
    local rest = pandoc.List()
    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child, "stat") then
        stat = pandoc.utils.stringify(child)
      else
        rest:insert(child)
      end
    end
    local lead = ""
    if stat ~= "" then
      lead = "#text(font: \"DM Mono\", size: 26pt, fill: rgb(\"#E60000\"))[" .. typst_escape(stat) .. "]\n#v(3pt)\n"
    end
    return pandoc.RawBlock("typst", "#pull[\n" .. lead .. to_typst(rest) .. "\n]")
  end

  if has_class(div, "sidebox") then
    local kicker = "Note"
    local rest = pandoc.List()
    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child, "kicker") then
        kicker = pandoc.utils.stringify(child)
      else
        rest:insert(child)
      end
    end
    return pandoc.RawBlock("typst", "#sidebox[" .. typst_escape(kicker:upper()) .. "][\n" .. to_typst(rest) .. "\n]")
  end

  if has_class(div, "spread") then
    local copy, side = pandoc.List(), pandoc.List()
    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child, "copy") then
        copy = child.content
      elseif child.t == "Div" and has_class(child, "side") then
        side = child.content
      end
    end
    local side_main = pandoc.List()
    local persons = {}
    for _, child in ipairs(side) do
      if child.t == "RawBlock" and child.text:match("^#person%[") then
        table.insert(persons, child.text)
      else
        side_main:insert(child)
      end
    end
    local typ = "#spread[\n" .. to_typst(copy) .. "\n][\n" .. to_typst(side_main) .. "\n]"
    if #persons > 0 then
      local cols = {}
      local cells = {}
      for _, text in ipairs(persons) do
        table.insert(cols, "1.85in")
        table.insert(cells, "[\n" .. text .. "\n]")
      end
      typ = typ .. "\n#block(breakable: false, width: 100%, above: 8pt)[\n"
        .. "#grid(columns: (" .. table.concat(cols, ", ") .. "), column-gutter: 0.16in, row-gutter: 8pt,\n"
        .. table.concat(cells, ",\n") .. "\n)\n]"
    end
    return pandoc.RawBlock("typst", typ)
  end

  if has_class(div, "title-cards") then
    local cells = {}
    for _, child in ipairs(div.content) do
      if child.t == "Div" and has_class(child, "title-card") then
        table.insert(cells, "#titlecard[\n" .. to_typst(child.content) .. "\n]")
      end
    end
    if #cells == 0 then
      return wrap_typst("block", div.content)
    end
    return pandoc.RawBlock(
      "typst",
      "#columns(2, gutter: 0.16in)[\n" .. table.concat(cells, "\n") .. "\n]"
    )
  end

  if has_class(div, "chart-page") then
    return pandoc.RawBlock(
      "typst",
      "#pagebreak(weak: true)\n#align(center)[\n" .. to_typst(div.content) .. "\n]\n#pagebreak(weak: true)\n"
    )
  end

  if has_class(div, "exec-summary") then
    return pandoc.RawBlock(
      "typst",
      "#pagebreak(weak: true)\n" .. to_typst(div.content) .. "\n#pagebreak(weak: true)\n"
    )
  end

  if has_class(div, "single") then
    return pandoc.RawBlock("typst", "#pagebreak(weak: true)\n" .. to_typst(div.content))
  end

  if has_class(div, "studio-card") then
    local main = pandoc.List()
    local extras = pandoc.List()
    for _, child in ipairs(div.content) do
      if child.t == "RawBlock" and child.text:match("^#person%[") then
        extras:insert(child)
      elseif child.t == "Div" and has_class(child, "person") then
        extras:insert(child)
      else
        main:insert(child)
      end
    end
    local blocks = pandoc.List()
    blocks:insert(pandoc.RawBlock("typst", "#studiocard[\n" .. to_typst(main) .. "\n]"))
    for _, extra in ipairs(extras) do
      blocks:insert(extra)
    end
    return blocks
  end

  local wrappers = {
    credit = "credit",
    logo = "logo",
    person = "person",
    lede = "lede",
    checksum = "checksum",
    versions = "versions",
    ["editors-note"] = "editorsnote",
  }
  for class, fn in pairs(wrappers) do
    if has_class(div, class) then
      return wrap_typst(fn, div.content)
    end
  end
  return nil
end

local function fraction_widths(n)
  if n == 7 then
    return { 0.17, 0.07, 0.13, 0.08, 0.10, 0.09, 0.36 }
  elseif n == 6 then
    return { 0.20, 0.08, 0.10, 0.18, 0.12, 0.32 }
  elseif n == 5 then
    return { 0.26, 0.12, 0.16, 0.22, 0.24 }
  end
  local widths = {}
  for i = 1, n do
    widths[i] = 1 / n
  end
  return widths
end

local function tighten_table(tbl)
  local n = #tbl.colspecs
  if n == 0 then
    return
  end
  local widths = fraction_widths(n)
  for i = 1, n do
    local align = tbl.colspecs[i][1]
    tbl.colspecs[i] = { align, widths[i] }
  end
end

function Table(tbl)
  if not is_typst() then
    return nil
  end
  tighten_table(tbl)
  return tbl
end

function Header(el)
  if not is_typst() then
    return nil
  end
  if has_class(el, "unlisted") then
    local text = typst_escape(pandoc.utils.stringify(el))
    return pandoc.RawBlock("typst", "#heading(level: " .. el.level .. ", outlined: false)[" .. text .. "]")
  end
  if has_class(el, "page-break") then
    local written = pandoc.write(pandoc.Pandoc({ pandoc.Header(el.level, el.content, pandoc.Attr(el.identifier)) }), "typst")
    return {
      pandoc.RawBlock("typst", "#pagebreak(weak: true)"),
      pandoc.RawBlock("typst", written),
    }
  end
  return nil
end

function Str(el)
  if not is_html() or not el.text:find("%d") then
    return nil
  end
  -- Span, not raw HTML. The cover stringifies these same inlines, and
  -- stringify drops raw HTML (which was deleting 32, 153,184, and the date).
  local text = el.text
  local inlines = pandoc.Inlines({})
  local pos = 1
  local changed = false
  while pos <= #text do
    local s, e, num = text:find("(%d[%d,]*(%.%d+)?%%?)", pos)
    if not s then
      inlines:insert(pandoc.Str(text:sub(pos)))
      break
    end
    changed = true
    if s > pos then
      inlines:insert(pandoc.Str(text:sub(pos, s - 1)))
    end
    inlines:insert(pandoc.Span({ pandoc.Str(num) }, pandoc.Attr("", { "num" })))
    pos = e + 1
  end
  if not changed then
    return nil
  end
  return inlines
end

local function collect_html_table(blocks, start)
  local chunk = pandoc.List()
  local i = start
  local first = blocks[i]
  if first.t == "RawBlock" and first.text:find("<table", 1, true) and first.text:find("</table>", 1, true) then
    chunk:insert(first)
    return chunk, i + 1
  end
  while i <= #blocks do
    local block = blocks[i]
    chunk:insert(block)
    i = i + 1
    if block.t == "RawBlock" and block.text:match("^</table") then
      break
    end
  end
  return chunk, i
end

local function native_table(chunk)
  local html = pandoc.write(pandoc.Pandoc(chunk), "html")
  local ok, parsed = pcall(pandoc.read, html, "html")
  if not ok or parsed == nil then
    return nil
  end
  local tables = pandoc.List()
  for _, block in ipairs(parsed.blocks) do
    if block.t == "Table" then
      tighten_table(block)
      tables:insert(block)
    end
  end
  if #tables == 0 then
    return nil
  end
  return tables
end

local function restore_html_tables(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    if is_typst() and block.t == "RawBlock" and block.text:match("^<table") then
      local chunk, next_i = collect_html_table(blocks, i)
      local tables = native_table(chunk)
      if tables then
        for _, table_block in ipairs(tables) do
          out:insert(table_block)
        end
      else
        for _, piece in ipairs(chunk) do
          out:insert(piece)
        end
      end
      i = next_i
    elseif block.t == "Div" then
      block.content = restore_html_tables(block.content)
      out:insert(block)
      i = i + 1
    else
      out:insert(block)
      i = i + 1
    end
  end
  return out
end

function Pandoc(doc)
  doc.blocks = restore_html_tables(doc.blocks)
  local fields = magazine_fields(doc.meta)
  if fields.issue == "" then
    fields.issue = "01"
  end
  if is_typst() then
    local cover, back = typst_front(fields)
    local blocks = pandoc.List()
    blocks:insert(pandoc.RawBlock("typst", cover))
    for _, block in ipairs(doc.blocks) do
      blocks:insert(block)
    end
    blocks:insert(pandoc.RawBlock("typst", back))
    doc.blocks = group_columns(blocks)
    return doc
  end
  if is_html() then
    local cover, back = html_front(fields, doc.blocks)
    local blocks = pandoc.List()
    blocks:insert(pandoc.RawBlock("html", cover))
    for _, block in ipairs(doc.blocks) do
      blocks:insert(block)
    end
    blocks:insert(pandoc.RawBlock("html", back))
    doc.blocks = group_columns(blocks)
    return doc
  end
  return doc
end
