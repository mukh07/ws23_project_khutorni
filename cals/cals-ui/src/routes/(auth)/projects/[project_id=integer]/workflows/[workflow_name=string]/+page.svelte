<script lang="ts">
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import {Card} from '$lib/components/ui/card';
	import {Separator} from '$lib/components/ui/separator';
	import {Button, buttonVariants} from '$lib/components/ui/button';
	import {Badge} from '$lib/components/ui/badge';
	import {Skeleton} from '$lib/components/ui/skeleton';
	import * as Popover from "$lib/components/ui/popover";
	import Reload from "svelte-radix/Reload.svelte";
	import ArrowRight from "svelte-radix/ArrowRight.svelte";
	import {cvatBaseUrl, slugify, getRandomIntBetween} from "$lib/utils.js";
    import { toast } from "svelte-sonner";
	import WorkflowIndicator from "$lib/components/WorkflowIndicator.svelte";
	import {notificationsStore} from "$lib/stores/notificationsStore";
	import {trainingCompletedStore} from "$lib/stores/trainingCompletedStore";

	export let data;
	let { project, workflow }: { project: Project; workflow: Workflow }  = data;
	$: ({ project, workflow } = data);
	$: workflowDouble = { ...workflow };
	$: completedPct = Number(workflow.completed / (workflow.completed + workflow.queued + (workflow.selected ? 1 : 0)))
                            .toLocaleString(undefined, {style: 'percent', minimumFractionDigits: 1})


	function formatDate(date) {
	  // Padding function to ensure single digits are preceded by a 0
	  const pad = (number, length = 2) => number.toString().padStart(length, '0');

	  const year = date.getFullYear();
	  const month = pad(date.getMonth() + 1); // getMonth() returns month from 0-11
	  const day = pad(date.getDate());
	  const hours = pad(date.getHours());
	  const minutes = pad(date.getMinutes());
	  const seconds = pad(date.getSeconds());
	  const milliseconds = pad(date.getMilliseconds(), 3); // Ensure milliseconds are three digits

	  // Combining the parts into the desired format
	  return `[${year}-${month}-${day} ${hours}:${minutes}:${seconds},${milliseconds}]`;
	}

	const nextActionMap = {
		ready: {
			action: "select-next-batch",
			btn: "Initialize and select next batch",
			below: ["ready", "annotating"],
			confirm: "Confirm initialization",
			confirmContent: "Running this will select a new batch, perform inference and select samples for annotation.",
			logs: [
				["Initializing workflow from metadata ...", [400, 600]],
				["Loading annotations into memory ...", [300, 600]],
				["Selecting batch ...", [1000, 1500]],
				["Uploading batch to CVAT ...", [1200, 2200]],
			]
		},
		busy: {
			action: "retrain",
			btn: "Mark annotation as completed",
			below: ["annotating", "training"],
			confirm: "Confirm completing annotating",
			confirmContent: "Running this will mark the selected batch as completed and retrain the model.",
			logs: [
				["Initializing workflow from metadata ...", [400, 600]],
				["Loading annotations into memory ...", [300, 600]],
				["Starting training script ...", [1000, 1500]],
				["Training - this might take a while ...", [1200, 2200]],
			]
		},
		training: {
			action: "select-next-batch",
			btn: "Waiting for training completion ...",
			below: ["training", "annotating"],
			confirm: "Confirm initialization",
			confirmContent: "Running this will select a new batch, perform inference and select samples for annotation.",
			logs: [
				["Initializing workflow from metadata ...", [400, 600]],
				["Loading annotations into memory ...", [300, 600]],
				["Selecting batch ...", [1000, 1500]],
				["Uploading batch to CVAT ...", [1200, 2200]],
			]
		}
	}
	$: statusActions = nextActionMap[workflow.metadata.status]


	let loading;
	let loadingMessage;
	let logLines = [];


	let name: string;
	let description: string;
	let batch_size: number;
	let model: Model;
	let query_strategy: QueryStrategy;


	function displayLoadingMessages(messages, currentIndex = 0) {
	  if (loading && currentIndex < messages.length) {
		logLines = [...logLines, [new Date(), messages[currentIndex][0]]];

		// Calculate the duration for the current message
		const duration = getRandomIntBetween(...messages[currentIndex][1]);

		// Set a timeout for the next message
		setTimeout(() => {
		  // Recursively call this function with the next index
		  displayLoadingMessages(messages, currentIndex + 1, loading);
		}, duration);
	  } else if (loading) {
		// If there are no more messages but loading is still true, show a default message
		loadingMessage = "Please wait";
	  } else if (!loading && currentIndex < messages.length) {
		logLines = [...logLines, ...messages.slice(currentIndex + 1).map(m => [new Date(), m[0]])]
	  }
	}

	$: formValid = name && batch_size && model && query_strategy;
</script>

<div class="container py-8 pt-10" id="outer-container">
	<div class="flex flex-col">
		<div class="flex items-center gap-3 pb-2 justify-between">
			<div class="flex items-center gap-7">
				<div class="flex flex-col gap-2">
					<h2 class="text-3xl">{workflow.name}</h2>
				</div>
				<span><Badge variant="outline" class="py-1 px-3">
					<WorkflowIndicator workflow={workflow}/>
				</Badge></span>
			</div>
			<div class="flex items-center gap-6">
				<div class="text-slate-500 text-sm">Created: <span class="font-bold">{workflow?.created_at?.slice(0, 10) ?? "Not given"}</span></div>
				<Button href={`${cvatBaseUrl}/projects/${project.id}/tasks/${workflow?.metadata?.current_task}`} target="_blank" class="font-bold" variant="outline" disabled={!workflow?.metadata?.current_task}}>Open current task in CVAT</Button>
			</div>
		</div>
		<div class="pb-8 text-slate-400">{workflow?.description ?? "No description"}</div>
		<div class="flex gap-4 pb-3">
			<div class="text-slate-600">Owner: <span class="font-bold">{project.owner.username}</span></div>
			<Separator orientation="vertical"/>
			<div class="text-slate-600">Current task ID: <span class="font-bold">{workflow?.metadata?.current_task ?? "No task"}</span></div>
			<Separator orientation="vertical"/>
		</div>
		<div class="flex gap-4 items-center pb-12">
			<div class="text-slate-600">Batch size: <span class="font-bold">{workflow.batch_size}</span></div>
			<Separator orientation="vertical"/>
			<div class="text-slate-600">Model: <span class="font-bold">{workflow.model}</span></div>
			<Separator orientation="vertical"/>
			<div class="text-slate-600">Query strategy: <span class="font-bold">{workflow.query_strategy ?? "aggregate-threshold-uncertainty-sampling"}</span></div>
			<Separator orientation="vertical"/>
		</div>
	</div>
		<div class="pb-3 flex justify-between items-end pt-2">
		<span>Workflow control</span>
	</div>
	<Separator />
	<div class="flex gap-12 flex-shrink-0 pt-2">
		<div class="h-[400px] w-[400px] min-w-[240px]">
			{#await import('$lib/components/Xyflow.svelte')}
				<div class="flex flex-col gap-3 items-center justify-center h-full">
					{#each new Array(4) as _}
						<Skeleton class="h-16 w-[260px]" />
					{/each}
				</div>
			{:then c}
				<svelte:component this={c.default} workflow={workflowDouble}/>
			{/await}
		</div>
		<div class="flex flex-col p-8 py-4 w-full gap-3 pt-5">
			<Popover.Root>
			  <Popover.Trigger asChild let:builder>
				<Button builders={[builder]} disabled={loading || workflow.metadata.status === 'training' && !$trainingCompletedStore?.[workflow.name]} class="font-bold text-lg py-5 flex gap-3">
					{#if loading}<Reload class="h-4 w-4 animate-spin" />{/if}
					{#if workflow.metadata.status === 'training' && $trainingCompletedStore?.[workflow.name]}
						Select next batch
					{:else}
						{statusActions.btn}
					{/if}
				</Button>
			  </Popover.Trigger>
			  <Popover.Content class="w-80">
				<div class="grid gap-4 pb-3">
				  <div class="space-y-3">
					<h3 class="font-medium leading-none pb-3 text-lg">{statusActions.confirm}</h3>
					<p class="text-md text-black">
						{statusActions.confirmContent}
					</p>
				  </div>
				</div>
				<Popover.Close class="w-full pt-2">
					<form method="POST" use:enhance={() => {
						const currentStatus = workflow.metadata.status;
						if (currentStatus === "busy") {
							trainingCompletedStore.update(s => ({...s, [workflow.name]: false }));
						}
						loading = true;
						displayLoadingMessages(statusActions.logs);
						return async ({ result, update }) => {
							loading = false;
							console.log(result)
							if (result.type === 'success' && result?.data?.task_id) {
								toast.success("New task in CVAT created", {
								  description: `Task with ID ${result.data.task_id} has been created.`,
								  action: {
									label: "Open task in CVAT",
									onClick: () => window.open('http://mindgarage26.cs.uni-kl.de:8080/tasks/' + result.data.task_id, '_blank')
								  }});
							} else if (result.type === 'success' && currentStatus === 'busy') {
								loading = true
								setTimeout(() => {
									loading = false
									trainingCompletedStore.update(s => ({...s, [workflow.name]: true }));
									notificationsStore.update(ns => [...ns, {
										id: Math.max(...ns.map(m => m.id), 0) + 1,
										message: `Training finished for workflow '${workflow.name}'.`,
										link: `/projects/${project.id}/workflows/${workflow.name}`
									}])
								}, 20000)
							}

							logLines = [...logLines, [new Date(), "Completed!"]]
	  						update();
						  }
						}}>
						<input type="hidden" name="project_id" value={project.id}>
						<input type="hidden" name="workflow_name" value={workflow.name}>
						<input type="hidden" name="action" value={statusActions.action}>
						<Button class="font-bold w-full" type="submit">Confirm</Button>
					</form>
				</Popover.Close>
			  </Popover.Content>
			</Popover.Root>
			<div class="flex text-slate-500 justify-center gap-2 w-full pt-1 pb-2 text-xs">{statusActions.below[0]} <span class="scale-75 inline-block -mt-1"><ArrowRight /></span> {statusActions.below[1]}</div>
			<div class="max-h-[240px] border border-1 h-full bg-gray-50 rounded !border-gray-300 text-xs flex flex-col gap-1 px-3 py-3 overflow-auto text-gray-600">
				{#if logLines.length > 0}
					{#each logLines as [time, log]}
						<div><span class="font-medium">{formatDate(time)}</span> -- {log}</div>
					{/each}
				{:else}
					<div class="text-sm text-gray-400 pl-4 pt-4 ">No logs</div>
				{/if}
			</div>

			<div class="flex flex-col gap-0.5 pt-2 pb-2">
				<div><span class="inline-block w-[160px]">Selected batch ID:</span><span class="font-bold pl-2">{workflow.selected}</span></div>
				<div class="flex "><span class="inline-block w-[160px]">Completed batches:</span> <span class="flex gap-3 font-bold pl-2">
					{workflow.completed} / {workflow.queued + workflow.completed + (workflow.selected ? 1 : 0)}
					<Separator orientation="vertical"/>
					<span>{completedPct}</span>
				</span></div>
			</div>

		</div>
	</div>

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

	.description-left h3 {
		min-width: 120px;
	}

	.info p {
		flex-grow: 1;
	}

</style>
