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
        <li>
            <svg
                xmlns="http://www.w3.org/2000/svg" version="1.1"
                viewBox="0 0 12 12"
                preserveAspectRatio="none"
                class="mod-symbol">
            <text x="6" y="6">{{ entity.name.firstname[0].upper() }}</text>
            </svg>
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
<dt>Frame</dt>
<dd>{{ ordinal }}</dd>
<dt>Hour</dt>
<dd>{{ time.name.split("_")[-1] }}</dd>
<dt>Source</dt>
<dd>{{ frame[0].source }}</dd>
<dt>Items</dt>
<dd>{{ items }}</dd>
</dl>
</section>
