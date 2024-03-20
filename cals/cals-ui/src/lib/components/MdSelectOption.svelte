<script lang="ts">
  import {browser} from "$app/environment";

  const component = browser
    ? import('@material/web/select/select-option')
    : new Promise(() => {})
</script>

{#await component}
{:then c}
  <md-select-option
    {...$$restProps}
  >
    <slot/>
  </md-select-option>
{/await}