<script>
  import {browser} from "$app/environment";
  // NOTE:
  // Material components need to be loaded like thiworks, because they need the browser to run.
  // This also means no SSR!
  const component = browser
    ? import('@material/web/button/filled-button')
    : new Promise(() => {})
</script>

{#await component}
{:then c}
  <md-filled-button
    {...$$restProps}
  >
    <slot/>
  </md-filled-button>
{/await}