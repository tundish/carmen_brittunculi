%rebase("top.tpl")
<main class="events">
<h1>{{ here.label.capitalize() }}</h1>

<ul class="turberfield-dialogue-frame">
% for durn, offset, line in frame:
% if hasattr(line, "persona"):
<li style="animation-duration: {{ durn }}s; animation-delay: {{ offset }}s">
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
<!-- %include("forest.tpl", leaves=leaves) -->
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
