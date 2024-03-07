<script>
	import Card from '$lib/components/Card.svelte';
	// import MdOutlinedTextField from "$lib/components/MdOutlinedTextField.svelte";
	// import MdFilledButton from "$lib/components/MdFilledButton.svelte";
</script>

<div class="container">
	<Card>
		<form method="POST">
			<h2>Welcome!</h2>
			<label>
				<span>Username</span>
				<input name="username" type="text" />
			</label>
			<label>
				<span>Password</span>
				<input name="password" type="password" />
			</label>
			<div class="submit-container">
				<button type="submit">Log in</button>
			</div>
<!--			<MdOutlinedTextField name="username" type="text" label="Username"/>-->
<!--			<MdOutlinedTextField name="password" type="password" label="Password"/>-->
<!--			<div class="submit-container">-->
<!--				<MdFilledButton type="submit">Log in</MdFilledButton>-->
<!--			</div>-->
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

	.submit-container {
		padding: 16px;
		width: 100%;
		display: flex;
	}

	label {
		display: flex;
		flex-direction: column;
	}

	input {
		padding: 8px;
	}

	button {
		padding: 8px 16px;
		cursor: pointer;
		width: 100%;
	}
</style>
