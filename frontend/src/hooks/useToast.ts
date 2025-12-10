// src/hooks/useToast.ts
import { useToastContext } from '../components/ToastProvider';

type Level = 'info' | 'success' | 'error' | 'warn';

export function useToast() {
  const ctx = useToastContext();

  function info(message: string, title?: string, ttl = 4000) {
    return ctx.push({ level: 'info', message, title, ttl });
  }
  function success(message: string, title?: string, ttl = 4000) {
    return ctx.push({ level: 'success', message, title, ttl });
  }
  function error(message: string, title?: string, ttl = 6000) {
    return ctx.push({ level: 'error', message, title, ttl });
  }
  function warn(message: string, title?: string, ttl = 5000) {
    return ctx.push({ level: 'warn', message, title, ttl });
  }

  return { info, success, error, warn, rawPush: ctx.push, remove: ctx.remove };
}
