<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="/css/base.css" />
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{{extent[0]}}" height="{{extent[1]}}"
viewBox="0 0 {{extent[0]}} {{extent[1]}}"
preserveAspectRatio="none"
>
<symbol id="svg-leaf-00">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="currentColor"
    fill-rule="evenodd"
/>
</symbol>
<symbol id="svg-leaf-01">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="green"
    fill-rule="evenodd"
    transform="rotate(45 16 16)"
/>
</symbol>

<svg>

<image
xmlns:xlink="http://www.w3.org/1999/xlink"
xlink:href="/svg/milliarium.svg"
x="0" y="0" width="100%" height="100%">
</image>

<text x=173" y="50">THIS IS A ROCK</text>
</svg>

% for leaf in leaves:
<use class="leaf" x="{{leaf.x}}" y="{{leaf.y}}" xlink:href="#{{leaf.ref}}" />
% end
</svg>
</body>
</html>
