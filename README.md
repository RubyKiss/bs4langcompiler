# bs4langcompiler
package bs4 to run script fetch a html 

anysl:
```
match [label] [class] [(^$%/)attr(^$%/)="str"]  [!text(^$%)="str"]
list [var]
print [var]

``` 
str cant not be use mulit line

inside the str you can use /" 

html:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div class="a">1234<a>666</a></div>
    <ul>
        <li>abc</li>
        <li>ddd</li>
        <li class="li">eeeeeeee111</li>
        <li>8882222eeee666</li>
        <li class="active">777777888</li>
    </ul>
    <ul open="789">
        <li>abc</li>
        <li>ddd</li>
        <li>eeeeeeee111</li>
        <li class="li">8882222eeee666</li>
        <li class="active">7777778881</li>
    </ul>
    <span>2333 yes i do</span>
    <div class="a">change you home</div>

</body>
</html>
```


scripts:
```

list hello
    match ul:
        match li .li

list abc
    match div .a !text^="change"
    match div !text^="233"

list cccc
    match div .a

list qqqq
    match span !text^="233"

list ddd
    match ul ^op^="7":
        match li .active

list dv
    match ul
        list qq
            match li .li
            match li .active

print abc
print cccc
print qqqq
print hello
print ddd
print dv
print qq

```
just run it

output:
```

abc print> [<div class="a">change you home</div>]
 cccc print> [<div class="a">1234<a>666</a></div>, <div class="a">change you home</div>]
 qqqq print> [<span>2333 yes i do</span>]
 hello print> [<li class="li">eeeeeeee111</li>, <li class="li">8882222eeee666</li>]
 ddd print> [<li class="active">7777778881</li>]
 dv print> [<ul>
<li>abc</li>
<li>ddd</li>
<li class="li">eeeeeeee111</li>
<li>8882222eeee666</li>
<li class="active">777777888</li>
</ul>, <ul open="789">
<li>abc</li>
<li>ddd</li>
<li>eeeeeeee111</li>
<li class="li">8882222eeee666</li>
<li class="active">7777778881</li>
</ul>]
 qq print> [<li class="li">eeeeeeee111</li>, <li class="li">8882222eeee666</li>, <li class="active">777777888</li>, <li class="active">7777778881</li>]
```
