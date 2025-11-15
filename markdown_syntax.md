# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2
###### This is a Heading h6
####### This is a Heading h7 ("There's no h7)

## Emphasis

*This text will be italic*  
_This will also be italic_

**This text will be bold**  
__This will also be bold__

_You **can** combine them_
**You *can* combine them**

## Lists

### Unordered

* Item 1
* Item 2
        * Item 2a
    * Item 2b
    * Item 2c
        * Item 2c.a
        * Item 2c.b
            * Item 2c.b.a
        * Item 2c.c
* Item 3

### Ordered

1. Item 1
2. Item 2
3. Item 3
    1. Item 3a
    2. Item 3b
        1. Item 3b.a
        2. Item 3b.b
            1. Item 3b.b.a
        3. Item 3b.c
4. Item 4

## Images

![This is an alt text.](/image/sample.webp "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
> Yep one more
>
> One more sentences
>> Nested sentence.
Combine with nested sentence

> Testing
 this supposed to be included
 in the blockquote

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

`inline code is here`
This web site is using `markedjs/marked`.
