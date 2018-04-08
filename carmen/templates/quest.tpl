%rebase("top.tpl")
<form role="form" action="/" method="POST" name="quest" >
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
