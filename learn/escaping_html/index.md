# Escaping HTML

Escaping HTML is where text is converted from tags and script that will interact with the DOM to representations of those things. For example:

Unscaped HTML:

```
<h1>Hello, World!</h1>
```

Escaped HTML:

```
&lt;h1&gt;Hello, World!&lt;/h1&gt;
```

This is useful for preventing security issues like code injection by malignant users who have access to text fields that display text they enter. Escaping blocks the addition of tags, JavaScript, and CSS.

## Jinja2 doesn't play it safe

By default, Jinja2 escapes nothing. It puts the burden of safety on the developer. To make Jinja2 escape text, use the `e` filter.

```
{% set h1 = '<h1>Hello, World!</h1>' %}
{{ h1|e }}
```

> ## "Jinja2 not playing it safe isn't a bad thing"
>
> We want to make it clear that Jinja2 not playing it safe isn't wrong. It can expedite development. However, it is important to note that the default can open the door to trouble. The design of Jinja2 accommodates this by making the `e` filter be so short - so it is easy and quick to use.

## Air Tags plays it safe

In contrast, by default Air Tags escapes everything.

```
air.H1("<h1>Hello, World!</h1>")
```

renders as:

```
&lt;h1&gt;Hello, World!&lt;/h1&gt;
```

To provide unescaped code, Air Tags provides three options: the `Style`, `Script`, and `Raw` tags - which are described below.

### `Style`: Unescaped CSS

To avoid escaping CSS, use the `Style` tag:

```
air.Style("""
p {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #333;
  max-width: 60ch;
  margin: 1em auto;
}
""")
```

Renders as:

```
<style>
p {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #333;
  max-width: 60ch;
  margin: 1em auto;
}
</style>
```

### `Script`: Unescaped JavaScript

To avoid escaping JavaScript, use the `Script` tag:

```
air.Script("""
function capitalize(str) {
  if (!str) return '';
  return str[0].toUpperCase() + str.slice(1);
}
""")
```

Renders as:

```
<script>
function capitalize(str) {
  if (!str) return '';
  return str[0].toUpperCase() + str.slice(1);
}
</script>
```

### `Raw`: Unescaped text

To avoid escaping anything and everything, use the `Raw` tag:

```
air.Raw("<h1>Hello, World<h1>")
```

Renders as:

```
<h1>Hello, World<h1>
```
