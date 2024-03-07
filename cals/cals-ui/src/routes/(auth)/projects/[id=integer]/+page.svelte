<script lang="ts">
	import { page } from '$app/stores';
	import Card from '$lib/components/Card.svelte';
	import MdFilledButton from "$lib/components/MdFilledButton.svelte";

	const workflows: Workflow[] = [
		{
			id: 12,
			name: 'Annotate',
			description: 'Annotate with love',
			batches: 100,
			created_by: 123
		},
		{
			id: 15,
			name: 'Annotate 2',
			batches: 50,
			created_by: 123
		}
	];

	$: projectId = $page.url.pathname.split("/").at(-1);
</script>

<div class="container">
	<div class="info">
		<p style="flex-grow: 1">Your workflows for project {projectId}</p>
<!--		<MdFilledButton href={`${projectId}/workflows/edit`}>-->
<!--			New Workflow-->
<!--		</MdFilledButton>-->
		<a class="link-btn" href={`${projectId}/workflows/edit`}>
			New Workflow
		</a>
	</div>
	<nav>
		<ul>
			{#each workflows as { id, name, description, batches, created_by }}
				<li class="project-listing">
					<Card padding={0} shadowOnHover={true}>
						<a href={`${projectId}/workflows/${id}`}>
							<div class="description-card">
								<div class="description-left">
									<h3>{name}</h3>
									<p>{description}</p>
								</div>
								<div class="description-right">
									<span style="white-space: nowrap;">ID: <b>{id}</b></span>
									<span style="white-space: nowrap;">Created by: <b>{created_by}</b></span>
								</div>
							</div>
						</a>
					</Card>
				</li>
			{/each}
		</ul>
	</nav>
</div>

<style>
	a {
		padding-left: 16px;
		all: unset;
		display: flex;
		gap: 16px;
		cursor: pointer;
		width: 100%;
	}

	.container {
		padding: 16px 24px 24px 24px;
		display: flex;
		flex-direction: column;
		width: 100%;
	}

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
		gap: 12px;
		padding: 0 24px 0 16px;
	}

	.info {
		display: flex;
		max-width: 680px;
	}

	.info p {
		flex-grow: 1;
	}

	a.link-btn {
		display: inline-flex;
		border-radius: 32px;
		background-color: #5c3791;
		justify-content: center;
		align-items: center;
		color: white;
		flex-shrink: 1;
		max-width: 180px;
	}
</style>
