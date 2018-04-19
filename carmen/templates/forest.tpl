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
    fill="currentColor"
    fill-rule="evenodd"
    transform="scale(1.4) rotate(45 16 16)"
/>
</symbol>
<symbol id="svg-leaf-02">
<path
    d="M 12 11 C 21,2 17,22 23,27 C 8,25 3,11 12,11 z M 18,16 C 16,14 17,22 20,24 z"
    stroke-width="0.2"
    stroke="yellow"
    fill="currentColor"
    fill-rule="evenodd"
    transform="scale(3.6) rotate(12 16 16)"
/>
</symbol>

<svg width="100" height="100" x="200" y="200">
<image
xmlns:xlink="http://www.w3.org/1999/xlink"
xlink:href="/svg/coin.svg"
x="0" y="0"
width="100%" height="100%">
</image>

<!-- x, y half of width of parent -->
<text x="50" y="50" fill="currentColor" font-size="10" text-anchor="middle">THIS IS A COIN</text>
</svg>

% for leaf in leaves:
<use class="leaf {{leaf.ref}}" x="{{leaf.x}}" y="{{leaf.y}}" xlink:href="#{{leaf.ref}}" />
% end
</svg>
