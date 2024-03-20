import { persist, createCookieStorage } from "@macfja/svelte-persistent-store"
import { writable } from "svelte/store"

export const tokenStore = persist(writable(null), createCookieStorage(), "token")