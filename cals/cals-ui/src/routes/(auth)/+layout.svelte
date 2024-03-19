<script lang="ts">
	import { page } from '$app/stores';
	import AppBar from './AppBar.svelte';
	import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";
  	import { Toaster } from "$lib/components/ui/sonner";
	import { ModeWatcher } from 'mode-watcher';


	function makeTitle(pathName: string) {
		return pathName
			.slice(1)
			.split('/')
			.filter((t) => t !== '/')
			.reduce((arr, word, currentIndex) => {
				return arr.concat([[
					word[0].toUpperCase() + word.slice(1),
					arr.length > 0 ? `${arr[currentIndex - 1][1]}/${word}` : `/${word}`
				]])
			}, [])
	}

	$: subpageTitle = makeTitle($page.url.pathname);
</script>

<Toaster theme="light" />

<ModeWatcher defaultMode="light"/>
<div>
	<AppBar>
		<Breadcrumb.Root>
			<Breadcrumb.List>
				{#each subpageTitle as [word, path], index}
					<Breadcrumb.Item>
						<Breadcrumb.Link href={path}>
							<span class="min-w-[80px]">{word}</span>
						</Breadcrumb.Link>
					</Breadcrumb.Item>
					{#if index < subpageTitle.length - 1}
						<Breadcrumb.Separator />
					{/if}
				{/each}
			</Breadcrumb.List>
		</Breadcrumb.Root>
	</AppBar>
	<div class="container pl-[48px] sm:pl-[96px]">
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
