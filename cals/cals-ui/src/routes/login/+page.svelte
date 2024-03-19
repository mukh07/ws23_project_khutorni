<script>
	import { enhance } from '$app/forms';
	import { Card } from '$lib/components/ui/card';
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import { Button } from "$lib/components/ui/button";
  	import Reload from "svelte-radix/Reload.svelte";

	let loading = false;
</script>

<div class="container">
	<Card class="p-7 px-8">
		<form method="POST" use:enhance={() => {
			loading = true;
			return async ({ update }) => {
				loading = false;
				update();
			}
		}}>
			<h2 class="scroll-m-20 pb-7 text-4xl font-extrabold tracking-tight lg:text-3xl">
				Welcome to CALS!
			</h2>
			<div class="flex flex-col gap-4">
				<Label class="flex flex-col gap-2">
					<span class="text-primary-muted">Username</span>
					<Input name="username" type="text" />
				</Label>
				<Label class="flex flex-col gap-2">
					<span class="text-primary-muted">Password</span>
					<Input name="password" type="password" />
				</Label>
			</div>
			<div class="pt-7">
				<Button
					disabled={loading}
					type="submit" class="min-w-[240px] !w-full font-bold">
					{#if loading}
						<div class="flex gap-3 items-center justify-center">
							<Reload class="h-4 w-4 animate-spin" />
							Please wait
						</div>
					{:else}
						Log in
					{/if}
				</Button>
			</div>
		</form>
	</Card>
</div>

<style>
	.container {
		width: 100%;
		height: 95vh;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	form {
		padding: 8px 16px;
		display: flex;
		flex-direction: column;
		gap: 16px;
		justify-content: center;
		align-items: center;
	}

	/*.submit-container {*/
	/*	padding: 16px;*/
	/*	width: 100%;*/
	/*	display: flex;*/
	/*}*/

	/*label {*/
	/*	display: flex;*/
	/*	flex-direction: column;*/
	/*}*/

	/*input {*/
	/*	padding: 8px;*/
	/*}*/

	/*button {*/
	/*	padding: 8px 16px;*/
	/*	cursor: pointer;*/
	/*	width: 100%;*/
	/*}*/
</style>
