<script lang="ts">
	import { page } from '$app/stores';
	import AppBar from './AppBar.svelte';

	function makeTitle(pathName: string) {
		return pathName
			.slice(1)
			.split('/')
			.filter((t) => t !== '/')
			.map((word) => word[0].toUpperCase() + word.slice(1))
			.join(' > ');
	}

	$: subpageTitle = makeTitle($page.url.pathname);
</script>

<div>
	<AppBar title={subpageTitle}></AppBar>
	<div class="container">
		<slot />
	</div>
</div>

<style>
	.container {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
