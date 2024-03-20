<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';
  import WorkflowIndicator from "$lib/components/WorkflowIndicator.svelte";
  import {Badge} from "$lib/components/ui/badge"

  type $$Props = NodeProps;

  export let data: $$Props['data'];

  $: {
    console.log(data)
  }
</script>

<Badge
    variant={data.active ? "default" : "outline"}
    class="p-3 border-2 rounded w-[120px] flex justify-center gap-2 px-8 text-sm">
  <Handle type="source" position={Position.Top} id="top"/>
  <WorkflowIndicator opacity={data.active ? "normal" : "muted"} workflow={{ metadata: { status: "training"} }} />
</Badge>