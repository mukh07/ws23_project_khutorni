<script lang="ts">
	import {Card} from '$lib/components/ui/card';
	import {Badge} from '$lib/components/ui/badge';
	import {Separator} from '$lib/components/ui/separator';

	export let data;
</script>

<div class="container py-8">
	<p class="pb-4">Found {data.projects.length} projects</p>
	<nav>
		<ul>
			{#each data.projects as { id, name, owner, status, updated_date }}
				<li class="project-listing">
					<Card padding={0} shadowOnHover={true} class="hover:shadow-lg transition-shadow">
						<a href={`/projects/${id}`}>
							<img src="/coco.jpeg" alt="" class="rounded-md min-w-[140px]"/>
							<div class="description-card p-3 px-1 w-full pr-8">
								<div class="flex justify-between items-center pb-3">
									<h3 class="text-xl">{name}</h3>
									<span class="text-slate-500">ID: {id}</span>
								</div>
								<p class="status-indicator flex !gap-2 pb-2 items-center !text-slate-600">Status: <Badge variant="secondary">{status}</Badge></p>
								<div class="description-lower pt-1">
									<span class="text-slate-600">Owner: <span class="font-bold">{owner.username}</span></span>
									<Separator orientation="vertical"/>
									<span class="text-slate-600">Updated: <span class="font-bold">{updated_date.slice(0, 10)}</span></span>
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
		width: 140px;
		height: 140px;
		border-radius: 15px 0 0 15px;
	}

	h3 {
		padding-top: 8px;
		padding-bottom: 4px;
	}

	p {
		color: #282828;
	}

	.description-lower, .status-indicator {
		font-size: 0.8615rem;
		/*color: #4b4b4bff;*/
		display: flex;
		gap: 12px;
	}
</style>
