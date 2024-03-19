<script lang="ts">
	import { AspectRatio } from "$lib/components/ui/aspect-ratio";
	import {Button} from "$lib/components/ui/button";
	import {Separator} from "$lib/components/ui/separator";
	import * as Avatar from "$lib/components/ui/avatar";
	import * as Popover from "$lib/components/ui/popover";
	import EnvelopeClosed from 'svelte-radix/EnvelopeClosed.svelte'
	import InfoCircled from 'svelte-radix/InfoCircled.svelte'
	import { notificationsStore } from '$lib/stores/notificationsStore'

	$: {
		console.log($notificationsStore)
	}
</script>

<div class="flex gap-12 items-center justify-between outer-container">
	<div class="flex gap-12 items-center justify-between">
		<span class="font-bold p-1 px-5">CALS</span>
		<slot />
	</div>
	<div class="flex items-center gap-3">
		<Popover.Root class="shadow-lg">
		  <Popover.Trigger asChild let:builder>
			<Button builders={[builder]} variant="outline" size="icon" class="relative">
				{#if $notificationsStore.length}
					<span class="indicator-dot-training absolute -top-0.5 -right-0.5"></span>
				{/if}
				<EnvelopeClosed class="h-4 w-4" />
			</Button>
		  </Popover.Trigger>
		  <Popover.Content class="w-80">
			<div class="grid gap-4">
			  <div class="space-y-2">
				<h3 class="font-medium leading-none text-md pb-2">
					Notifications ({$notificationsStore.length})
				</h3>
			  <div class="flex flex-col gap-2">
				{#if $notificationsStore.length}
					{#each $notificationsStore as { id, message, link }}
						<Separator />
						<div class="w-full">
						  <Button variant="link" class="!whitespace-normal w-full flex gap-3 pl-1 justify-start" on:click={() => {
							  notificationsStore.update(ns => ns.filter(n => n.id !== id));
						  }} href={link}>
							  <InfoCircled class="h-5 w-5"/>
							  {message}
						  </Button></div>
					{/each}
					<div class="pt-3">
						<Button variant="ghost" on:click={() => notificationsStore.set([])}>Clear all</Button>
					</div>
				{:else}
					<span class="text-gray-500 text-sm">All cleared!</span>
				{/if}
			  </div>
			  </div>
			</div>
		  </Popover.Content>
		</Popover.Root>
		<Button variant="ghost" class="flex items-center gap-3 justify-center p-5">
			<div>
				khutorni
			</div>
			<Avatar.Root class="bg-[#794EC4] flex justify-center items-center text-white font-bold">
				K
			</Avatar.Root>
		</Button>
	</div>
</div>

<style>
	div.outer-container {
		padding: 16px;
		border-bottom: 1px solid rgba(128, 128, 128, 0.2);
		border-bottom: 1px solid rgba(83, 37, 37, 0.2);
	}

	h3 {
		margin: 8px 0;
	}

	.indicator-dot-training {
	 	width: 7px; /* Size of the dot */
		height: 7px; /* Size of the dot */
		border-radius: 50%; /* Make it round */
		background-color: #6600ff; /* Purple color */
		box-shadow: 0 0 5px #6600ff; /* Glowing effect */
	}
</style>
