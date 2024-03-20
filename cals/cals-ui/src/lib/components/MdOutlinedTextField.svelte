<script lang="ts">
  import {browser} from "$app/environment";
  import { bindMwcValue } from "$lib/actions/bindMwcValue";

  export let value;

  console.log("THE VALUE")

  const component = browser
    ? import('@material/web/textfield/outlined-text-field')
    : new Promise(() => {})
</script>

{#await component}
{:then c}
  <md-outlined-text-field
    use:bindMwcValue={{ value }}
    {...$$restProps}
  >
    <slot/>
  </md-outlined-text-field>
{/await}