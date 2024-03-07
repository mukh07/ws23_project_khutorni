<script lang="ts">
	import DragAndDropFileInput from "$lib/components/DragAndDropFileInput.svelte";

	let name: string;
	let batch_size: number;
	let images: File;
	let annotations: File

	$: formValid = name && batch_size && batch_size > 0 && images && images.length > 0;

	$: console.log(images)
</script>

<div class="container">
	<h1>Create a new workflow</h1>
	<div>
		<form method="POST" enctype="multipart/form-data" action="/upsert">
			<div class="form-block form-block-oneline" style="gap: 48px;">
				<label>
					<span>Name*</span>
					<input
						bind:value={name}
						style="width: 100%"
						name="name"
						type="text"
					>
				</label>
				<label>
					<span>Batch size*</span>
					<input
						bind:value={batch_size}
						min={1}
						name="batch_size"
						type="number"
					>
				</label>
			</div>
			<div style="padding-bottom: 24px">
				<p>Images*</p>
				<DragAndDropFileInput bind:files={images}/>
			</div>
			<div>
				<p>Annotations</p>
			</div>
			<div class="form-block" style="padding: 0">
				<DragAndDropFileInput bind:files={annotations} acceptedFileTypes={[".json"]} />
			</div>
			<div class="form-block" style="padding-top: 48px">
				<button type="submit" style="font-size: 1.125rem; font-weight: bold; padding: 12px;" disabled={!formValid}>
					Create workflow
				</button>
			</div>
		</form>
	</div>
</div>

<style>
	form {
		padding: 16px;
	}
	.form-block {
		display: flex;
		flex-direction: column;
		gap: 16px;
		padding: 24px 0;
	}

	.form-block-oneline {
		flex-direction: row;
	}

	label {
		display: flex;
		flex-direction: column;
	}

	input {
		padding: 8px;
		display: inline-block;
	}
</style>