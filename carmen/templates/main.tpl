%rebase("_page.tpl")
<main class="grid-front">
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
<aside class="grid-roof mod-vista">
<!-- <img src="/svg/poisson.svg"/> -->
</aside>

<aside class="grid-rear mod-diorama">
<ul>
  % for entity in entities:
    % if hasattr(entity, "name") and entity is not player:
        <li>{{ entity.name.firstname[0].upper() }}
            <!--<svg viewBox="0 0 64 64" class="mod-diorama">
            <text x="0" y="64">{{ entity.name.firstname[0].upper() }}</text>
            </svg>-->
        </li>
    % end
  % end
</ul>
</aside>

<aside class="grid-wing mod-vista">
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
