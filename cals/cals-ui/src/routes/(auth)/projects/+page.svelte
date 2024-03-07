<script lang="ts">
	import Card from '$lib/components/Card.svelte';

	const projects: Project[] = [
		{
			id: 0,
			name: 'COCO Extended',
			description: 'Labeling COCO keypoints until your eyes bleed',
			owner_id: 123,
			assignee_id: 1234
		},
		{
			id: 1,
			name: 'Cats dataset',
			description: 'Largest-ever cat dataset',
			owner_id: 123
		},
		{
			id: 2,
			name: 'Limadication 1.0',
			description: 'Do I really need to explain?',
			owner_id: 123,
			assignee_id: 1234
		}
	];
</script>

<div class="container">
	<p>Your projects in CVAT</p>
	<nav>
		<ul>
			{#each projects as { id, name, description, owner_id, assignee_id }}
				<li class="project-listing">
					<Card padding={0} shadowOnHover={true}>
						<a href={`/projects/${id}`}>
							<img src="" alt="" />
							<div class="description-card">
								<h3>{name}</h3>
								<p>{description}</p>
								<div class="description-lower">
									<span>ID: {id}</span>
									<span>Owner: {owner_id}</span>
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
		all: unset;
		display: flex;
		gap: 24px;
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
		gap: 24px;
	}

	li {
		max-width: 640px;
	}

	img {
		background-color: darkred;
		width: 160px;
		height: 160px;
		border-radius: 16px 0 0 16px;
	}

	h3 {
		padding-top: 8px;
		padding-bottom: 4px;
	}

	p {
		color: #282828;
	}

	.description-lower {
		font-size: 0.8615rem;
		color: #4b4b4bff;
		display: flex;
		gap: 12px;
	}
</style>
