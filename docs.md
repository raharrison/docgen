# h1 Heading

## h2 Heading

### h3 Heading

#### h4 Heading

##### h5 Heading

###### h6 Heading

## Horizontal Rules

---

---

## Emphasis

**This is bold text**

**This is bold text**

_This is italic text_

_This is italic text_

~~Strikethrough~~

## Blockquotes

> Blockquotes can also be nested...
>
> > ...by using additional greater-than signs right next to each other...
> >
> > > ...or with spaces between arrows.

## Lists

Unordered

- Create a list by starting a line with `+`, `-`, or `*`
- Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    - Ac tristique libero volutpat at
    * Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
- Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa

1) You can use sequential numbers...
1) ...or keep all the numbers as `1.`

## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code

Block code "fences"

```
Sample text here...
```

Syntax highlighting

```js
var foo = function(bar) {
  return bar++;
};

console.log(foo(5));
```

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="github-markdown.css" />
<style>
  .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }

  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }
</style>
<article class="markdown-body">
  <h1>Unicorns</h1>
  <p>All the things</p>
</article>
```

```python
# score net worth - NET WORTH
networth_score = {'$250,000-$499,999': 1, 'Greater than $499,999': 2}

# score education - on EDUCATION
education_score = {'Completed College': 1, 'Graduate School': 2, 'High School': -2, 'Some College': -1, 'Unknown': 0}

# on FAMILY POSITION
marriage_score = {'Husband': 1, 'Wife': 1}

# score occupation - OCCUPATION
occup_score = {'Dentist/Dental Hygienist': 2, 'Doctors/Physicians/Surgeons': 2, 'Nurses': 2, 'Pharmacist': 2, 'Sales/Marketing': 1}

# estates buyers are often renting before purchase - HOMEOWNER/RENTER
renter_score = {'Definite Renter': 1}

# most buyers 35-44, then 45-54 and 55-64 - AGE - INDIVIDUAL 2-YEAR AGE BANDS
age_score = {'35-36 Years Old': 2, '37-38 Years Old': 2, '39-40 Years Old': 2, '41-42 Years Old': 2, '43-44 Years Old': 2,
             '45-46 Years Old': 1, '47-48 Years Old': 1, '49-40 Years Old': 1, '41-42 Years Old': 1, '43-44 Years Old': 1,
             '55-56 Years Old': 1, '57-58 Years Old': 1, '59-50 Years Old': 1, '51-52 Years Old': 1, '43-54 Years Old': 1}

# child score - PRESENCE OF CHILDREN
child_score = {'Children Absent': 1}
```

## Tables

| Option | Description                                                               |
| ------ | ------------------------------------------------------------------------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default.    |
| ext    | extension to be used for dest files.                                      |

Right aligned columns

| Option |                                                               Description |
| -----: | ------------------------------------------------------------------------: |
|   data | path to data files to supply the data that will be passed into templates. |
| engine |    engine to be used for processing templates. Handlebars is the default. |
|    ext |                                      extension to be used for dest files. |

## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica

## Images

![Minion](https://octodex.github.com/images/minion.png)

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg "The Dojocat"
