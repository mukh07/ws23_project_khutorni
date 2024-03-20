import { persisted } from 'svelte-persisted-store'

export const trainingCompletedStore = persisted(
    "trainingCompleted",
    {}
);