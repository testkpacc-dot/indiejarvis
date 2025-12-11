// src/components/ToastProvider.tsx
import React, { createContext, useContext, useCallback, useMemo, useState } from 'react';

type ToastLevel = 'info' | 'success' | 'error' | 'warn';
type Toast = { id: string; title?: string; message: string; level: ToastLevel; ttl?: number };

type ToastContextValue = {
  push: (t: Omit<Toast, 'id'>) => string;
  remove: (id: string) => void;
};

const ToastContext = createContext<ToastContextValue | null>(null);

export function useToastContext() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToastContext must be used within ToastProvider');
  return ctx;
}

function makeId() {
  return Math.random().toString(36).slice(2, 9);
}

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const push = useCallback((t: Omit<Toast, 'id'>) => {
    const id = makeId();
    const toast: Toast = { id, ...t };
    setToasts((s) => [...s, toast]);
    if (toast.ttl && toast.ttl > 0) {
      setTimeout(() => setToasts((s) => s.filter((x) => x.id !== id)), toast.ttl);
    }
    return id;
  }, []);

  const remove = useCallback((id: string) => {
    setToasts((s) => s.filter((t) => t.id !== id));
  }, []);

  const value = useMemo(() => ({ push, remove }), [push, remove]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      {/* Toast container (bottom-right) */}
      <div className="fixed right-4 bottom-6 z-50 flex flex-col gap-3 max-w-sm">
        {toasts.map((t) => (
          <ToastItem key={t.id} toast={t} onClose={() => remove(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

function ToastItem({ toast, onClose }: { toast: Toast; onClose: () => void }) {
  const color = {
    info: 'bg-blue-50 border-blue-200',
    success: 'bg-green-50 border-green-200',
    error: 'bg-rose-50 border-rose-200',
    warn: 'bg-yellow-50 border-yellow-200',
  }[toast.level];

  return (
    <div className={`border ${color} rounded-md p-3 shadow-sm`}>
      <div className="flex items-start gap-3">
        <div className="flex-1">
          {toast.title && <div className="font-medium text-sm mb-1">{toast.title}</div>}
          <div className="text-sm text-gray-700">{toast.message}</div>
        </div>
        <div className="ml-2 shrink-0">
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-sm px-2 py-1"
            aria-label="dismiss toast"
          >
            ×
          </button>
        </div>
      </div>
    </div>
  );
}
