<script lang="ts">
  type AcceptedFileType = ".zip" | ".json" | ".jpeg" | ".png"
  export let acceptedFileTypes: AcceptedFileType[] = [".zip"]
  export let minHeight: undefined | number = undefined

  export let files;

  let draggedOver = false;

  // Function to handle file drop
  function handleDrop(event) {
    event.preventDefault();
    draggedOver = false;
    const uploadedFiles = event.target.files;
    console.log(uploadedFiles)
    files = uploadedFiles;
    const file = uploadedFiles[0];
    if (file && (file.name.endsWith('.zip') || file.name.endsWith('.json'))) {
      // Process the file here
      console.log(file);
    } else {
      // Handle wrong file type
      alert('Only .zip or .json files are allowed.');
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
    draggedOver = true;
  }

  function handleDragLeave(event) {
    event.preventDefault();
    draggedOver = false;
  }

</script>


<div
  class="drop-zone {draggedOver ? 'dragged-over' : ''}"
  on:drop={handleDrop}
  on:dragover={handleDragOver}
  on:dragleave={handleDragLeave}
>
  <label>
  {#if !files || files.length === 0}
    <span>
      Drag and drop a file here, or click to select a file.
    </span><br>
    <span style="padding-top: 32px; color: #4d758c"><b>{acceptedFileTypes.join(", ")}</b></span>
  {:else}
    <div class="filelist">
      {#each files as f}
        <span class="filename">{f.name}</span>
      {/each}
    </div>
  {/if}
  <input
    type="file"
    on:change="{handleDrop}"
    hidden
    accept={acceptedFileTypes}
  />
  </label>
</div>


<style>
  .drop-zone {
    border: 2px dashed #90a4ae;
    border-radius: 4px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    color: #8fa4af;
    background-color: #eceff1;
    transition: background-color 0.3s;
    /*pointer-events: none;*/
  }

  .drop-zone.dragged-over {
    background-color: #cfd8dc;
  }

  label span {
    cursor: pointer;
    user-select: none;
  }

  .filelist {
    display: flex;
    justify-content: center;
    gap: 8px;
  }

  .filename {
    padding: 4px;
    border: 1px solid #27536e;
    color: #27536e;
    border-radius: 4px;

  }
</style>