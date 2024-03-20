<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';
  import WorkflowIndicator from "$lib/components/WorkflowIndicator.svelte";
  import { badgeVariants } from "$lib/components/ui/badge";
  import {Badge} from "$lib/components/ui/badge";

  type $$Props = NodeProps;

  export let data: $$Props['data'];
</script>

<Badge
    variant={data.active ? "default" : "outline"}
    class="p-3 border-2 rounded w-[120px] flex justify-center gap-2 px-8 text-sm">
  <WorkflowIndicator opacity={data.active ? "normal" : "muted"} workflow={{ metadata: { status: "ready"} }} />
  <Handle type="source" position={Position.Bottom} id="bottom"/>
</Badge>