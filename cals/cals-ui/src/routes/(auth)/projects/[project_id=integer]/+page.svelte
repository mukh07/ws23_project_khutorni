<script lang="ts">
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import {Card} from '$lib/components/ui/card';
	import {Separator} from '$lib/components/ui/separator';
	import {Textarea} from '$lib/components/ui/textarea';
	import {Button, buttonVariants} from '$lib/components/ui/button';
	import {Badge} from '$lib/components/ui/badge';
    import { ScrollArea } from "$lib/components/ui/scroll-area";
	import Reload from "svelte-radix/Reload.svelte";
	import * as Dialog from "$lib/components/ui/dialog";
  	import * as Select from "$lib/components/ui/select";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import {cvatBaseUrl, slugify, getRandomIntBetween} from "$lib/utils.js";
	import WorkflowCard from "$lib/components/WorkflowCard.svelte";

	export let data;
	let { project, workflows }: { project: Project; workflows: Workflow[] }  = data;
	$: ({ project, workflows } = data);

	const models = ["rtmpose-l_8xb256-420e_coco_extended-256x192", "rtmpose-m_8xb256-420e_coco_extended-256x192"]
	type Model = typeof models[number];

	const query_strategies = ["aggregated-threshold-uncertainty-sampling"]
	type QueryStrategy = typeof query_strategies[number];

		const messages = [
		{
			content: "Initializing COCO dataset",
			duration: [2000, 3000]
		},
		{
			content: "Setting up directories",
			duration: [1500, 2400],
		},
		{
			content: "Saving metadata",
			duration: [600, 1500]
		}
	];
	let loading;
	let loadingMessage;

	let name: string;
	let description: string;
	let batch_size: number;
	let model: Model;
	let query_strategy: QueryStrategy;

	function clickOutside() {
		loadingMessage = null;
		const overlay = document.querySelector("[data-melt-dialog-overlay]");
		overlay.setAttribute("data-state", "closed")
		overlay.style.display = "none";
		const content = document.querySelector("[data-melt-dialog-content]");
		content.setAttribute("data-state", "closed");
		content.style.display = "none";
	}

	function sortDescendingByDate(list) {
	  return list.sort((a, b) => new Date(b.date) - new Date(a.date));
	}

	$: formValid = name && batch_size && model && query_strategy;
</script>

<div class="container py-8 pt-10" id="outer-container">
	<div class="flex flex-col">
		<div class="flex items-center gap-3 pb-8 justify-between">
			<div class="flex items-center gap-6">
				<h2 class="text-3xl">{project.name}</h2>
				<span><Badge variant="secondary">{project.status}</Badge></span>
			</div>
			<div class="flex items-center gap-6">
				<div class="text-slate-500 text-sm">last update: <span class="font-bold">{project.updated_date.slice(0, 10)}</span></div>
				<Button href={`${cvatBaseUrl}/projects/${project.id}`} target="_blank" class="font-bold" variant="outline">Open project in CVAT</Button>
			</div>
		</div>
		<div class="flex gap-3 pb-2">
			<div class="text-slate-600">Owner: <span class="font-bold">{project.owner.username}</span></div>
			<Separator orientation="vertical"/>
			{#if project.assignee}
				<div class="text-slate-600">Assignee: <span class="font-bold">{project.assignee.username}</span></div>
				<Separator orientation="vertical"/>
			{/if}
			<div class="text-slate-600">Created: <span class="font-bold">{project.created_date.slice(0, 10)}</span></div>
			<Separator orientation="vertical"/>
		</div>
		<div class="flex gap-3 items-center pb-12">
			<div class="text-slate-600">Tasks: <span class="font-bold">{project.tasks_count}</span></div>
			<Separator orientation="vertical"/>
			<div class="text-slate-600">Splits: <span class="font-bold">{project.task_subsets}</span></div>
			<Separator orientation="vertical"/>
			<div><Button variant="link" href={`${cvatBaseUrl}/api/labels?project_id=${project.id}`} class="font-bold">View skeleton</Button></div>
			<Separator orientation="vertical"/>
		</div>
	</div>

	<div class="pb-3 flex justify-between items-end">
		<span>Found {workflows.length} workflow{#if data.workflows.length !== 1}s{/if}</span>
		<Dialog.Root state="closed">
		  <Dialog.Trigger class={buttonVariants({ variant: "default" })}
		  ><span class="px-6 inline-block font-bold text-white">New AL Workflow</span></Dialog.Trigger
		  >
		  <Dialog.Content class="sm:max-w-[425px]">
			<Dialog.Header>
			  <Dialog.Title class="text-2xl">Create a new workflow</Dialog.Title>
			  <Dialog.Description>
				Create a new workflow. Click submit when you're done.
			  </Dialog.Description>
			</Dialog.Header>
				<div class="grid gap-4 py-4">
				  <div class="grid grid-cols-4 items-center gap-4">
					<Label for="name" class="text-right">Name</Label>
					<Input
						id="name"
						bind:value={name}
					    on:change={(e) => {
							const updated = slugify(e.target.value);
							e.target.value = updated;
							name = updated;
						}}

						class="col-span-3"
					/>
				  </div>
				<div class="grid gap-4 py-4">
				  <div class="grid grid-cols-4 items-center gap-4">
					<Label for="description" class="text-right">Description</Label>
					<Textarea
						id="description"
						placeholder="Describe the purpose of this workflow"
						bind:value={description}
					    on:change={(e) => {
							const updated = e.target.value;
							e.target.value = updated;
							description = updated;
						}}

						class="col-span-3"
					/>
				  </div>
				  <div class="grid grid-cols-4 items-center gap-4">
					<Label for="batch_size" class="text-right">Batch size</Label>
					<Input
						id="batch_size"
						type="number"
						min="1"
						bind:value={batch_size}
						on:change={(e) => {
							const updated = Math.min(1000, Math.max(1, e.target.value));
							e.target.value = updated;
							batch_size = updated;
						}}
						class="col-span-3"
					/>
				  </div>
				  <div class="grid grid-cols-4 items-center gap-4">
					<Label for="model" class="text-right">Model</Label>
				  	<Select.Root onSelectedChange={({ value }) => {
						  model = value;
				  	}}>
					  <Select.Trigger class="w-[280px]">
						<Select.Value placeholder="Choose a model" />
					  </Select.Trigger>
						<Select.Content>
							<Select.Group>
							  <Select.Label>Model</Select.Label>
							  {#each models as m}
								<Select.Item value={m} label={m}
								  >{m}</Select.Item
								>
							  {/each}
							</Select.Group>
						</Select.Content>
					  	<Select.Input/>
					</Select.Root>
				  </div>
				  <div class="grid grid-cols-4 items-center gap-4">
					<Label for="model" class="text-right">Query strategy</Label>
				  	<Select.Root onSelectedChange={({ value }) => {
						  query_strategy = value;
				  	}}>
					  <Select.Trigger class="w-[280px]">
						<Select.Value placeholder="Choose a query strategy" />
					  </Select.Trigger>
						<Select.Content>
							<Select.Group>
							  <Select.Label>Query strategy</Select.Label>
							  {#each query_strategies as qs}
								<Select.Item value={qs} label={qs}
								  >{qs}</Select.Item
								>
							  {/each}
							</Select.Group>
						</Select.Content>
					  	<Select.Input/>
					</Select.Root>
				  </div>
				</div>
			<Dialog.Footer>
			<form method="POST"
			  use:enhance={() => {
				loading = true;
				loadingMessage = messages[0].content
				setTimeout(() => {
					if (loading) {
						loadingMessage = messages[1].content;
						setTimeout(() => {
							if (loading) {
								loadingMessage = messages[2].content;
								setTimeout(() => {
									if (loading) {
										loadingMessage = "Please wait"
									}
								}, getRandomIntBetween(...messages[2].duration))
							}
						}, getRandomIntBetween(...messages[1].duration))
					}
				}, getRandomIntBetween(...messages[0].duration))
				return async ({ update }) => {
					loading = false;
					batch_size = null;
					name = null;
					model = null;
					description = null;
					query_strategy = null;

					loadingMessage = "Success!";
					setTimeout(clickOutside, 200)

					update();
			}}}>
			  <input type="hidden" name="name" bind:value={name}>
			  <input type="hidden" name="model" bind:value={model}>
			  <input type="hidden" name="project_id" value={project.id}>
			  <input type="hidden" name="batch_size" bind:value={batch_size}>
			  <input type="hidden" name="description" bind:value={description}>
			  <input type="hidden" name="query_strategy" bind:value={query_strategy}>
			  <Button
				  on:click={() => console.log("clicked")}
				  disabled={!formValid || loading} type="submit"
				  class={"font-bold flex items-center gap-3" + (loadingMessage === "Success!" ? " bg-green-500" : "")}>
				  {#if loading}
					    <Reload class="h-4 w-4 animate-spin" />
					  {loadingMessage}
				  {:else}
					  Submit
				  {/if}
			  </Button>
			</form>

			</Dialog.Footer>
		  </Dialog.Content>
		</Dialog.Root>
	</div>
	<Separator />
	<ScrollArea class="pt-6 h-[400px] pr-6">
		<nav class="w-full flex flex-col gap-4">
			{#each workflows.filter(w => w.metadata.status === "ready") as workflow }
				<WorkflowCard workflow={workflow} />
			{/each}
		</nav>
		<nav class="w-full flex flex-col gap-4 pt-9">
			{#each sortDescendingByDate(workflows.filter(w => w.metadata.status === "busy" || w.metadata.status === "training")) as workflow }
				<WorkflowCard workflow={workflow} />
			{/each}
		</nav>

	</ScrollArea>
</div>

<style>
	ul {
		list-style-type: none;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	li {
		max-width: 640px;
	}

	p {
		color: #282828;
	}

	.description-card {
		padding-left: 16px;
		gap: 16px;
		display: flex;
		align-items: center;
		width: 100%;
	}

	.description-left {
		font-size: 0.8615rem;
		display: flex;
		flex-grow: 1;
		gap: 16px;
		align-items: center;
		width: 100%;
	}

	.description-left h3 {
		min-width: 120px;
	}

	.description-right {
		font-size: 0.8615rem;
		color: #4b4b4bff;
		display: flex;
		flex-shrink: 1;
		padding: 0 24px 0 16px;
	}

	.info {
		display: flex;
		max-width: 680px;
	}

	.info p {
		flex-grow: 1;
	}

	/*a.link-btn {*/
	/*	display: inline-flex;*/
	/*	!*border-radius: 32px;*!*/
	/*	background-color: #5c3791;*/
	/*	justify-content: center;*/
	/*	align-items: center;*/
	/*	color: white;*/
	/*	flex-shrink: 1;*/
	/*	max-width: 180px;*/
	/*}*/
</style>
