%rebase("top.tpl")
<main class="air">
% if lines:
<h1>{{ lines[0].scene.capitalize() }}</h1>
% end

% for line in lines:
% if hasattr(line, "persona"):
<blockquote class="line">
% if hasattr(line.persona, "name"):
<header class="persona">{{ line.persona.name.fullname }}</header>
% end
<p class="speech">{{ line.text }}</p>
</blockquote>
% end
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
