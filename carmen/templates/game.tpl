%rebase("_page.tpl")
<form role="form" action="/" method="POST" name="quest" class="grid-front mod-titles">
  <h1>Start a new story.</h1>
    <fieldset>
    <label for="player-name" id="player-name-tip">Choose a Roman or Brythonic name</label>
    <input
    name="playername"
    type="text"
    id="player-name"
    required="required"
    aria-describedby="player-name-tip"
    placeholder="?"
    pattern="{{ validation["name"].pattern }}"
    >
    <button type="submit">Enter</button>
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
    <a href="/about">About Carmen Brittunculi</a>
</form>

