%rebase("_page.tpl")
<main class="grid-front">
<!-- <h1>{{ frame[0].shot.scene.capitalize() }}</h1> -->
<h1>{{ here.label.capitalize() }}</h1>

<ul class="mod-dialogue">
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
% elif hasattr(element.dialogue, "loop"):
<li>
<audio
    src="/audio/{{ element.dialogue.resource }}"
    autoplay="autoplay" preload="auto"
>
</audio>
</li>
% end
% end
</ul>

</main>
<aside class="grid-roof vista">
<img src="/svg/poisson.svg"/>
</aside>

<aside class="grid-rear diorama">
<ul>
  % for entity in entities:
    % if hasattr(entity, "name") and entity is not player:
        <li>{{ entity.name.firstname[0].upper() }}</li>
    % end
  % end
</ul>
</aside>

<aside class="grid-wing vista">
<img src="/svg/poisson.svg"/>
<!-- %include("forest.tpl", leaves=leaves) -->
</aside>
<nav class="grid-steer">
<ul>
  % for legend, locn in moves:
    <li>
        <form role="form" action="/{{ session.uid.hex }}/move/{{ locn.id.hex }}" method="post" name="move-{{ legend }}" >
    % if session.cache["visits"][locn]:
        <button type="submit">{{ locn.label }}</button>
    % else:
        <button type="submit">Go {{ legend }}</button>
    % end
        </form>
    </li>
  % end
</ul>
</nav>
<section class="grid-dash">
<dl class="mod-stats">
<dt>Items</dt>
<dd>{{ items }}<dd>
<dt>Frame</dt>
<dd>{{ ordinal }}<dd>
</dl>
</section>
