import { persisted } from 'svelte-persisted-store'

interface Notification {
    id: number;
    message: string;
    link: string;
}

export const notificationsStore = persisted<Notification[]>(
    "notifications",
    [
    ]
);