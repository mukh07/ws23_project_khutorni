<script lang="ts">
    import {Card} from "$lib/components/ui/card";
    import type {Workflow} from "../../types";
    import WorkflowIndicator from "$lib/components/WorkflowIndicator.svelte";

    export let workflow: Workflow;
</script>

<a class="" href={`${workflow.project_id}/workflows/${workflow.name}`}>
    <Card class="p-4 hover:shadow-md transition-shadow w-full">
        <div class="description-card w-full">
            <div class="description-left !gap-10">
                <h3 class="-mr-1 text-lg text-black w-[196px]">{workflow.name}</h3>
                <span class="max-w-[240px] truncate text-gray-600">{workflow.description}</span>
            </div>
            <div class="description-right gap-16">
                <WorkflowIndicator workflow={workflow}/>
                <span class="whitespace-nowrap">
                    Progress: <span class="font-bold inline-block min-w-[44px]">
                        {Number(workflow.completed / (workflow.queued + workflow.completed))
                            .toLocaleString(undefined, {style: 'percent', minimumFractionDigits: 1})}
                    </span>
                </span>
            </div>
        </div>
    </Card>
</a>

<style>
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
</style>