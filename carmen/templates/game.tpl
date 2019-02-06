%rebase("_page.tpl")
<form role="form" action="/" method="POST" name="quest" class="grid-front mod-titles">
  <legend>Start a new story.</legend>
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
    <small id="player-name-tip">at least 2 letters long</small>
    </fieldset>
    <!-- <fieldset>
    <label for="email">Email</label>
    <input
    name="email"
    id="email"
    placeholder="@"
    aria-describedby="email-tip"
    pattern="{{ validation["email"].pattern }}"
    >
    <small id="email-tip">optional</small>
    </fieldset> -->
  <button type="submit">Enter</button>
</form>

