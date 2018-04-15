%rebase("top.tpl")
<main class="air">
<h1>{{ here.label }}</h1>
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
