// src/components/ErrorBoundary.tsx
import React from 'react';

type Props = { children: React.ReactNode };
type State = { hasError: boolean; error?: Error | null };

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: any) {
    // send to logging endpoint if you have one
    // console.error('Captured by ErrorBoundary', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[200px] flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow-sm border border-gray-100 max-w-xl text-center">
            <h3 className="text-lg font-semibold mb-2">Something went wrong</h3>
            <p className="text-sm text-gray-600 mb-4">An unexpected error occurred in the UI.</p>
            <div className="flex items-center justify-center gap-3">
              <button
                className="px-4 py-2 bg-teal-600 text-white rounded"
                onClick={() => window.location.reload()}
              >
                Reload
              </button>
              <button
                className="px-4 py-2 border rounded"
                onClick={() => this.setState({ hasError: false, error: null })}
              >
                Dismiss
              </button>
            </div>
            <details className="mt-4 text-xs text-gray-500 text-left">
              <summary className="cursor-pointer">Error details</summary>
              <pre className="whitespace-pre-wrap mt-2 text-xs">{String(this.state.error)}</pre>
            </details>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
