<script lang="ts">
    export let workflow: Workflow;
    export let opacity: string;

    const statusMap = {
        busy: "annotating",
        ready: "ready",
        training: "training"
    }
</script>

<div class="whitespace-nowrap flex gap-3 items-center">
    <span
        style={`opacity: ${opacity === "normal" ? 1 : 0.6};`}
        class="text-md">{statusMap[workflow.metadata.status]}</span>
    <div
        class="indicator-dot"
        class:muted={opacity === "muted"}
        class:indicator-dot-annotating={workflow.metadata.status === 'busy'}
        class:indicator-dot-initial={workflow.metadata.status === 'ready'}
        class:indicator-dot-training={workflow.metadata.status === 'training'}>
    </div>
</div>

<style>
    .indicator-dot {
        width: 10px; /* Size of the dot */
		height: 10px; /* Size of the dot */
		border-radius: 50%; /* Make it round */
    }

	.indicator-dot-initial {
		background-color: #00FF00; /* Green color */
		box-shadow: 0 0 8px #00FF00; /* Glowing effect */
	}

    .indicator-dot-initial.muted {
		background-color: #00FF0077; /* Green color */
		box-shadow: 0 0 8px #00FF0077; /* Glowing effect */
	}

	.indicator-dot-annotating {
		background-color: #ff9100; /* Orange color */
		box-shadow: 0 0 8px #ff9100; /* Glowing effect */
	}

    .indicator-dot-annotating.muted {
		background-color: #ff910077; /* Orange color */
		box-shadow: 0 0 8px #ff910077; /* Glowing effect */
	}

    .indicator-dot-training {
		background-color: #6600ff; /* Purple color */
		box-shadow: 0 0 8px #6600ff; /* Glowing effect */
	}

    .indicator-dot-training.muted {
		background-color: #6600ff77; /* Purple color */
		box-shadow: 0 0 8px #6600ff77; /* Glowing effect */
	}
</style>