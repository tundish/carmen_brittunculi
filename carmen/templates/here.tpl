%rebase("top.tpl")
<main>
<h1>{{ here.label }}</h1>
</main>
<aside>
%include("forest.tpl", extent=extent, leaves=leaves, coin=coin, marker=marker)
</aside>
<aside>
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
