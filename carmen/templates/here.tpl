%rebase("top.tpl")
<main class="events">
<h1>{{ frame[0].shot.scene.capitalize() }}</h1>

<ul class="turberfield-dialogue-frame">
% for element in frame:
% if hasattr(element.dialogue, "persona"):
<li style="animation-duration: {{ element.duration }}s; animation-delay: {{ element.offset }}s">
<blockquote class="line">
% if hasattr(element.dialogue.persona, "name"):
<header class="persona">
{{ element.dialogue.persona.name.firstname }}
{{ element.dialogue.persona.name.surname }}
</header>
% end
<p class="speech">{{ element.dialogue.text }}</p>
</blockquote>
</li>
% end
% end
</ul>

</main>
<aside class="diorama">
<img src="/svg/poisson.svg"/>
<!-- %include("forest.tpl", leaves=leaves) -->
<dl>
<dt>Items</dt>
<dd>{{ items }}<dd>
</dl>
</aside>
<nav>
<ul>
  % for legend, locn in moves:
    <li>
        <form role="form" action="/{{ session.uid.hex }}/move/{{ locn.id.hex }}" method="post" name="move-{{ legend }}" >
        <button type="submit">Go {{ legend }}</button>
        </form>
    </li>
  % end
</ul>
</nav>
