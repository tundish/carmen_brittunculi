<!DOCTYPE html>
<html>
<head>
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg"
width="{{extent[0]}}" height="{{extent[1]}}"
viewBox="0 0 {{extent[0]}} {{extent[1]}}"
preserveAspectRatio="none"
>
<defs>
<path id="svg-leaf-00"
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="green"
    fill-rule="evenodd"
/>
<path id="svg-leaf-01"
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="green"
    fill-rule="evenodd"
    transform="rotate(45 16 16)"
/>
</defs>
% for leaf in leaves:
<use x="{{leaf.x}}" y="{{leaf.y}}" xlink:href="#{{leaf.ref}}" />
% end
</svg>
</body>
</html>
