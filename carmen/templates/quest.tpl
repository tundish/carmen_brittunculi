%rebase("top.tpl")
<form role="form" action="/" method="POST" name="quest" class="titles">
  <legend>Start a new game.</legend>
    <fieldset>
    <label for="player-name">Player</label>
    <input
    name="playername"
    type="text"
    id="player-name"
    required="required"
    aria-describedby="player-name-tip"
    placeholder="?"
    pattern="{{ validation["name"].pattern }}"
    >
    <small id="player-name-tip">Choose your player name (2 - 32 characters).</small>
    </fieldset>
    <fieldset>
    <label for="email">Email</label>
    <input
    name="email"
    id="email"
    aria-describedby="email-tip"
    pattern="{{ validation["email"].pattern }}"
    >
    <small id="email-tip">Leave an email address if you'd like to stay in touch.</small>
    </fieldset>
  <button type="submit">Enter</button>
</form>
<aside class="floor">
<p><em>Carmen Brittunculi</em> is a short adventure game.</p>
<p>I wrote it in 2018 for the <a href="https://itch.io/jam/roman-mytholojam">Roman Mytholojam</a>.</p>
<p>It's an example of a Web Native game. It uses only Python, SVG, HTML5 and CSS3.</p>
<dl>
<dt>Copyright</dt>
<dd>D Haynes</dd>
<dt>Licence</dt>
<dd><a href="http://www.gnu.org/licenses/agpl.html">GNU Affero GPL</a></dd>
<dt>Project details</dt>
<dd>See the <a href="https://tundish.itch.io/carmen-brittunculi">Itch.io project page</a>.<dd>
<dt>Source code</dt>
<dd>You can download the game from the <a href="https://github.com/tundish/carmen_brittunculi">code repository on Github</a>.</dd>
</dl>
</aside>
