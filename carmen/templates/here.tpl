%rebase("top.tpl")
<main class="air">
% if lines:
<h1>{{ lines[0] }}</h1>
% end

% for line in lines:
<blockquote class="line">
<header class="persona"></header>
<p class="speech"></p>
</blockquote>
% end

</main>
<aside class="floor">
%include("forest.tpl", extent=extent, leaves=leaves, coin=coin, marker=marker)
</aside>
<aside class="inventory">
<h1>Pouch</h1>
</aside>
<nav>
<ul>
  % for legend, locn in moves:
    <li>
        <form role="form" action="/{{ quest.hex }}/move/{{ locn.id.hex }}" method="post" name="move-{{ legend }}" >
        <button type="submit">Go {{ legend }}</button>
        </form>
    </li>
  % end
</ul>
</nav>
