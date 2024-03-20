<!--Material UI web 3 does not provide cards yet, so we have to make our own-->
<script lang="ts">
	type CardPaddingSize = 0 | 8 | 16 | 32;
	type ShadowSize = "sh-small" | "sh-medium" | "sh-large"

	export let padding: CardPaddingSize = 32;
	export let shadow: ShadowSize = "sh-small";
	export let shadowOnHover: boolean = false;
</script>

<div
	style={`padding: ${padding}px`}
	class:sh-small={shadow === "sh-small"}
	class:sh-medium={shadow === "sh-medium"}
	class:sh-large={shadow === "sh-large"}
	class:hover-shadow={shadowOnHover}
>
	<slot />
</div>

<style>
	div {
		display: flex;
		padding: 32px;
		border-radius: 16px;
		border: 1px solid rgba(37, 9, 61, 0.18);
		transition: box-shadow 50ms;
	}

	div.sh-small {
		box-shadow:
			rgba(0, 0, 0, 0) 0px 0px 0px 0px,
			rgba(0, 0, 0, 0) 0px 0px 0px 0px,
			rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
	}

	div.sh-medium, div.hover-shadow:hover {
		box-shadow:
			rgba(0, 0, 0, 0.12) 0px 1px 3px,
			rgba(0, 0, 0, 0.24) 0px 1px 2px;
	}

	div.sh-large {
		box-shadow:
			rgba(0, 0, 0, 0.19) 0px 10px 20px,
			rgba(0, 0, 0, 0.23) 0px 6px 6px;
	}

</style>
