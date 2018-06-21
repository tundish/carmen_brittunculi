%rebase("top.tpl")
<main class="events">
% if lines:
<h1>{{ lines[0].scene.capitalize() }}</h1>
% end

<ul class="turberfield-dialogue-frame">
% for line in lines:
% if hasattr(line, "persona"):
<li style="animation-duration: 4s; animation-delay: 0s">
<blockquote class="line">
% if hasattr(line.persona, "name"):
<header class="persona">{{ line.persona.name.fullname }}</header>
% end
<p class="speech">{{ line.text }}</p>
</blockquote>
</li>
% end
% end
</ul>

</main>
<aside class="diorama">
<img src="/svg/poisson.svg"/>
<!-- %include("forest.tpl", extent=extent, leaves=leaves, coin=coin, marker=marker) -->
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
