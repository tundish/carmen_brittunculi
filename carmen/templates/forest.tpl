<!DOCTYPE html>
<html>
<head></head>
<body>
<p>Leaf</p>
<svg xmlns="http://www.w3.org/2000/svg">
<defs>
<path id="svg-leaf"
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="green"
    fill-rule="evenodd"
/>
</defs>
% for leaf in leaves:
<use x="{{leaf.x}}" y="{{leaf.y}}" xlink:href="#{{leaf.ref}}" />
% end
</svg>
</body>
</html>
