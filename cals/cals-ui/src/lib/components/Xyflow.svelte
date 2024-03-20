<script lang="ts">
    export const ssr = false;

  import { writable } from 'svelte/store';
  import type { Edge } from '@xyflow/svelte'
  import {
    SvelteFlow,
    Position,
    MarkerType,
    ConnectionMode,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap,
  } from '@xyflow/svelte';
	import { useNodes } from '@xyflow/svelte';

  // you need to import the styles for Svelte Flow to work
  // if you just want to load the basic styleds, you can import '@xyflow/svelte/dist/base.css'
  import '@xyflow/svelte/dist/style.css'

  import BiDirectionalEdge from '$lib/components/flow/BiDirectionalEdge.svelte';
  import ReadyNode from '$lib/components/flow/ReadyNode.svelte';
  import AnnotationNode from '$lib/components/flow/AnnotationNode.svelte';
  import TrainingNode from '$lib/components/flow/TrainingNode.svelte';

  // nodes.update(ns => ns.map(n => ({...n, data: { ...n.data, active: workflow.metadata.status === (n.data.label === "annotating" ? "busy" : n.data.label) }})))


  export let workflow: Workflow;
  $: activeName = workflow.metadata.status;

  const nodeTypes = {
    ready: ReadyNode,
    training: TrainingNode,
    annotating: AnnotationNode,
  };

  const edgeTypes = {
    bidirectional: BiDirectionalEdge,
  };

  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position. This also makes it easier to update nodes in user land.
  const nodes = writable([
    {
      id: '1',
      type: 'ready',
      data: { label: 'ready', active: workflow.metadata.status === 'ready' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2',
      type: 'annotating',
      data: { label: 'annotating', active: workflow.metadata.status === 'busy' },
      position: { x: -85, y: 100 },
      sourcePosition: Position.Bottom,
      targetPosition: Position.Top
    },
    {
      id: '3',
      type: 'training',
      data: { label: 'training', active: workflow.metadata.status === 'training' },
      position: { x: 0, y: 200 },
      sourcePosition: Position.Bottom,
      targetPosition: Position.Top
    },
  ]);

  // same for edges
  const edges = writable([
    {
      id: '1-2',
      type: 'default',
      source: '1',
      target: '2',
      sourceHandle: 'bottom',
      targetHandle: 'top',
      animated: true,
      style: "stroke-width: 2px;",
      markerEnd: {
        type: MarkerType.ArrowClosed,
        strokeWidth: 1,
        width: 10
      },
    },
    {
      id: '2-3',
      type: 'bidirectional',
      source: '2',
      target: '3',
      sourceHandle: 'bottom',
      targetHandle: 'top',
      animated: true,
      style: "stroke-width: 2px;",
      markerEnd: {
        type: MarkerType.ArrowClosed,
        strokeWidth: 1,
        width: 10
      },
    },
    {
      id: '3-2',
      type: 'bidirectional',
      source: '3',
      target: '2',
      sourceHandle: 'top',
      targetHandle: 'bottom',
      animated: true,
      style: "stroke-width: 2px;",
      markerEnd: {
        type: MarkerType.ArrowClosed,
        strokeWidth: 1,
        width: 10
      },
    },
  ]);

  $: {
    console.log("ACTIVENAME", activeName);
    nodes.update(ns => ns.map(n => ({...n, data: { ...n.data, active: workflow.metadata.status === (n.data.label === "annotating" ? "busy" : n.data.label) }})))
  }
</script>

<SvelteFlow
  {nodeTypes}
  {edgeTypes}
  {nodes}
  {edges}
  connectionMode={ConnectionMode.Loose}
  panOnDrag={false}
  fitView
  maxZoom={1.5}
  nodesDraggable={false}
  nodesSelectable={false}
  on:nodeclick={(event) => console.log('on node click', event)}
>
  <Background variant={BackgroundVariant.Dots} />
</SvelteFlow>